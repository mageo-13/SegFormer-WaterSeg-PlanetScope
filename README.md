# SegFormer-WaterSeg-PlanetScope
Water body segmentation using SegFormer on PlanetScope imagery.

This project implements a semantic segmentation pipeline using the SegFormer model to extract water bodies from high-resolution PlanetScope satellite imagery. 
The workflow includes model training, evaluation, and postprocessing steps.

This repository contains two Google Colab notebooks demonstrating:
- Training a **SegFormer** model for binary segmentation of water bodies.
- Post-processing and evaluating predictions on **PlanetScope** satellite images.

---

## Contents

- `train_segformer_colab.ipynb`: Fine-tunes SegFormer on PlanetScope imagery and binary masks
- `eval_postprocess_colab.ipynb`: Evaluates model performance and visualizes predictions

---

## Dataset

- Satellite patches and corresponding mask are provided. This is a small sample subset of the full data.
- Satellite: PlanetScope
- Labels: Binary masks (0 = background, 1 = water)
