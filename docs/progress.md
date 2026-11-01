# Progress log

## 2026-10-31

- Notebook 01 (data check) is done. The 670 training images of BBBC038 stage1 are grouped into three image types (fluorescence, brightfield, histology) and split into train and validation sets per type. Results are in `results/`.
- Notebook 02 (U-Net) is set up: data loading, per-image normalisation, random 256 x 256 crops with flips and rotations, weighted cross-entropy loss (boundary class weight 3) and validation with foreground IoU.
- Next step: write the `UNet` class myself, check the output shape, then train on a Kaggle T4 GPU.

## 2026-11-01

- Notebook 03 (evaluation) is ready. It turns the three pixel classes into single nuclei with a watershed from the interior class, scores every validation image with the Data Science Bowl metric (AP over IoU 0.5 to 0.95) and F1 at IoU 0.5, reports the scores per image type, counts merged and split nuclei, and tests the warning question from the plan: do the 10 % most uncertain images contain the 10 % worst ones?
- The scoring functions were checked on synthetic masks first: a perfect prediction scores 1.0, two touching nuclei predicted as one count as one merge, and a nucleus cut in two counts as one split.
- Next step: unchanged. The U-Net class in notebook 02, then training, then notebook 03 on the trained weights.
