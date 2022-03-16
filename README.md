<h1 align="center">Welcome to the code for Drive&Segment 👋</h1>

<p align="center">
 <a href="TBD">
    <img alt="Project Page" src="https://img.shields.io/badge/Project Page-Open-green.svg" target="_blank" />
  </a>
  <a href="https://github.com/kefranabg/readme-md-generator/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-yellow.svg" target="_blank" />
  </a>
  <a href="https://twitter.com/AVobecky">
    <img alt="Twitter: AVobecky" src="https://badgen.net/badge/icon/twitter?icon=twitter&label" target="_blank" />
  </a>
  <a href="https://huggingface.co/spaces/vobecant/DaS">
    <img alt="Gradio App" src="https://img.shields.io/badge/Gradio App-Open%20In%20Spaces-blue.svg" target="_blank" />
  </a>
</p>

<h2 align="center">
  <a href="#">project page</a> |
  <a href="#">arXiv</a> |
  <a href="https://huggingface.co/spaces/vobecant/DaS">Gradio</a>
</h2>

# 🚙📷 Drive&Segment: Unsupervised Semantic Segmentation of Urban Scenes via Cross-modal Distillation

This project hosts the code for inference of the Drive&Segment for unsupervised image segmentation of urban scenes.

> [**Drive&Segment: Unsupervised Semantic Segmentation of Urban Scenes via Cross-modal Distillation**](TBD)            
> [Antonin Vobecky](https://vobecant.github.io/), [David Hurych](https://scholar.google.com/citations?hl=en&user=XY1PVwYAAAAJ), [Oriane Siméoni](https://osimeoni.github.io/), [Spyros Gidaris](https://scholar.google.fr/citations?user=7atfg7EAAAAJ&hl=en), [Andrei Bursuc](https://abursuc.github.io/), [Patrick Pérez](https://ptrckprz.github.io/), and [Josef Sivic](https://people.ciirc.cvut.cz/~sivic/)
>
> *arXiv preprint ([arXiv XYZ.xyz](TBD))*

**Table of Contents**
- [Highlights](#-highlights)
- [Examples](#-examples)
- [Running the models](#-running-the-models)
- [Results](#-results)
- [Citation](#-citation)

![teaser](sources/teaser.png)

## 💫 Highlights

- 🚫🔬 **Unsupervised semantic segmentation:** Drive&Segments proposes learning semantic segmentation in urban scenes without any manual annotation, just from
the raw non-curated data collected by cars which, equipped with 📷 cameras and 💥 LiDAR sensors.
- 📷💥 **Multi-modal training:** During the train time our method takes 📷 images and 💥 LiDAR scans as an input, and
  learns a semantic segmentation model *without using manual annotations*.
- 📷 **Image-only inference:** During the inference time, Drive&Segments takes *only images* as an input.
- 🏆 **State-of-the-art performance:** Our best single model based on Segmenter architecture achieves **21.8%** in mIoU on
  Cityscapes (without any fine-tuning).
- 🚀 **Gradio Application**: We provide an interactive [Gradio application](https://huggingface.co/spaces/vobecant/DaS)
  so that everyone can try our model.

## 📺 Examples

### **Pseudo** segmentation.

Example of **pseudo** segmentation.

![](sources/video128_blend03_v2_10fps_640px_lanczos.gif)

### Cityscapes segmentation.

Two examples of pseudo segmentation mapped to the 19 ground-truth classes of the Cityscapes dataset by using Hungarian
algorithm.

![](sources/video_stuttgart00_remap_blended03_20fps_crop.gif)
![](sources/video_stuttgart01_remap_blended03_20fps_crop2.gif)

## ✨ Running the models

### 📝 Requirements

Please, refer to `requirements.txt`

To create and run a virtual environment with the required packages, you can run:
```
conda create --name DaS --file requirements.txt
conda activate DaS
```

### 🚀 Inference

We provide our Segmenter model trained on the nuScenes dataset.

Run

```
python3 inference.py --input-path [path to image/folder with images] --output-dir [where to save the outputs] --cuda
```

where:

- `--input-path` specifies either a path to a single image or a path to a folder with images,
- `output-dir` (optional) specifies the output directory, and
- `--cuda` is flag denoting whether to run the code on the GPU **(strongly recommended)**.

Example: `python3 inference.py --input-path sources/img1.jpeg --output-dir ./outputs --cuda`

### nuScenes model

We provide [weights](https://data.ciirc.cvut.cz/public/projects/2022DriveAndSegment/segmenter_nusc.pth) and config
files ([CPU](https://data.ciirc.cvut.cz/public/projects/2022DriveAndSegment/segmenter_nusc.pth_variant.yml)
/ [GPU](https://data.ciirc.cvut.cz/public/projects/2022DriveAndSegment/segmenter_nusc.pth_variant_gpu.yml)) for the
Segmenter model trained on the nuScenes dataset.

The weights and config files are downloaded automatically when running `inference.py`. Should you prefer to download
them by hand, please place them to the `./weights` folder.

### Waymo Open model

Due to the Waymo Open dataset license terms, we cannot openly share the trained weights. If you are interested in using
the model trained on the Waymo Open dataset, please register at
the [Waymo Open](https://waymo.com/intl/en_us/dataset-download-terms/) and send the confirmation of your agreement to
the license terms to the [authors](mailto:antonin.vobecky@cvut.cz).

## 📈 Results
In the table below, we report the results of our best model (Segmenter trained on Waymo Open dataset) evaluated in the unsupervised setup (i.e., by obtaining mapping between pseudo- and ground-truth classes by Hungarian algorithm).

| Dataset  | mIoU |
| ------------- | ------------- |
| Cityscapes (19 cls)  | 21.8  |
| Cityscapes (27 cls)  | 15.3  |
| Dark Zurich  | 14.2  |
| Nighttime Driving  | 18.9  |
| ACDC (night)  | 13.8 |
| ACDC (fog)  | 14.5 |
| ACDC (rain)  | 14.9 |
| ACDC (snow)  | 14.6 |
| ACDC (mean)   | 16.7  |

## 📖 Citation
Please consider citing our paper in your publications if the project helps your research. BibTeX reference is as follows.
```
@article{XY,
  title     =  {},
  author    =  {},
  booktitle =  {arXiv preprint},
  year      =  {2022}
}
