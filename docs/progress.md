# Progress log

## 2026-10-31

- Notebook 01 (data check) is done. The 670 training images of BBBC038 stage1 are grouped into three image types (fluorescence, brightfield, histology) and split into train and validation sets per type. Results are in `results/`.
- Notebook 02 (U-Net) is set up: data loading, per-image normalisation, random 256 x 256 crops with flips and rotations, weighted cross-entropy loss (boundary class weight 3) and validation with foreground IoU.
- Next step: write the `UNet` class myself, check the output shape, then train on a Kaggle T4 GPU.
