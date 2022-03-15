import os

import gradio as gr
import numpy as np
import requests
import torch
import yaml
from PIL import Image
from torchvision import transforms

from segmenter_model import utils
from segmenter_model.factory import create_segmenter
from segmenter_model.fpn_picie import PanopticFPN
from segmenter_model.utils import colorize_one, map2cs

WEIGHTS = './weights/segmenter.pth'


def download_file_from_google_drive(destination=WEIGHTS):
    id = '1v6_d2KHzRROsjb_cgxU7jvmnGVDXeBia'

    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def download_weights():
    if not os.path.exists(WEIGHTS):
        url = 'https://drive.google.com/file/d/1v6_d2KHzRROsjb_cgxU7jvmnGVDXeBia/view?usp=sharing'
        import urllib.request
        urllib.request.urlretrieve(url, WEIGHTS)


def segment_segmenter(image, model, window_size, window_stride, encoder_features=False, decoder_features=False,
                      no_upsample=False, batch_size=2):
    seg_pred = utils.inference(
        model,
        image,
        image.shape[-2:],
        window_size,
        window_stride,
        batch_size=batch_size,
        no_upsample=no_upsample,
        encoder_features=encoder_features,
        decoder_features=decoder_features
    )
    if not (encoder_features or decoder_features):
        seg_pred = seg_pred.argmax(1).unsqueeze(1)
    return seg_pred


def remap(seg_pred, ignore=255):
    mapping = {0: 0, 12: 1, 15: 2, 23: 3, 10: 4, 14: 5, 18: 6, 2: 7, 17: 8, 13: 9, 8: 10, 3: 11, 27: 12, 4: 13, 25: 14,
               24: 15, 6: 16, 22: 17, 28: 18}
    h, w = seg_pred.shape[-2:]
    seg_pred_remap = np.ones((h, w), dtype=np.uint8) * ignore
    for pseudo, gt in mapping.items():
        whr = seg_pred == pseudo
        seg_pred_remap[whr] = gt
    return seg_pred_remap


def create_model(resnet=False):
    weights_path = WEIGHTS
    variant_path = '{}_variant.yml'.format(weights_path)

    print('Use weights {}'.format(weights_path))
    print('Load variant from {}'.format(variant_path))
    variant = yaml.load(
        open(variant_path, "r"), Loader=yaml.FullLoader
    )

    # TODO: parse hyperparameters
    window_size = variant['inference_kwargs']["window_size"]
    window_stride = variant['inference_kwargs']["window_stride"]

    net_kwargs = variant["net_kwargs"]
    if not resnet:
        net_kwargs['decoder']['dropout'] = 0.

    # TODO: create model
    if resnet:
        model = PanopticFPN(arch=net_kwargs['backbone'], pretrain=net_kwargs['pretrain'], n_cls=net_kwargs['n_cls'])
    else:
        model = create_segmenter(net_kwargs)

    # TODO: load weights
    print('Load weights from {}'.format(weights_path))
    weights = torch.load(weights_path)['model']
    model.load_state_dict(weights, strict=True)

    model.eval()

    return model, window_size, window_stride


def get_transformations():
    return transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])


download_file_from_google_drive()
model, window_size, window_stride = create_model()


def predict(input_img):
    input_img = Image.open(input_img)
    transform = transforms.Compose([transforms.Resize(256, Image.BICUBIC), transforms.ToTensor()])
    input_img = transform(input_img)
    input_img = torch.unsqueeze(input_img, 0)

    with torch.no_grad():
        segmentation = segment_segmenter(input_img, model, window_size, window_stride).squeeze().detach()
        segmentation_remap = remap(segmentation)

    drawing_pseudo = colorize_one(segmentation_remap)
    drawing_cs = map2cs(segmentation_remap)

    drawing_pseudo = transforms.ToPILImage()(drawing_pseudo)
    drawing_cs = transforms.ToPILImage()(drawing_cs)
    return drawing_pseudo, drawing_cs


title = "Drive&Segment"
description = 'Gradio Demo accompanying paper "Drive&Segment: Unsupervised Semantic Segmentation of Urban Scenes via Cross-modal Distillation"'
# article = "<p style='text-align: center'><a href='TODO' target='_blank'>Project Page</a> | <a href='codelink' target='_blank'>Github</a></p>"
examples = [['examples/img1.jpg']]

iface = gr.Interface(predict, gr.inputs.Image(type='filepath'), "image", title=title, description=description,
                     examples=examples)

iface.launch()
