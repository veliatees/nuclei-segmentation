# Nucleus segmentation: where it fails, and can the model tell?

A small study on the nuclei images of the 2018 Data Science Bowl (BBBC038). I train a U-Net that finds every nucleus in an image, compare its output with the expert masks for each image type, and test one practical question: can the model's own uncertainty point to the images that need a second look by a person?

Status: step 1 (data check) is done. The training notebook (02) and the evaluation notebook (03) are ready; the U-Net class in 02 is the part I write myself, and training on a Kaggle GPU comes next. The plan, with the hypotheses, is in `docs/plan.md` and was written before any training. Progress is logged in `docs/progress.md`.

## Data

BBBC038v1 from the Broad Bioimage Benchmark Collection (https://bbbc.broadinstitute.org/BBBC038), training set `stage1_train`: microscopy images with an expert mask for every nucleus. Fluorescence, brightfield and histology images, different magnifications and cell types. License: CC0.

Caicedo et al. (2019). Nucleus segmentation across imaging experiments: the 2018 Data Science Bowl. Nature Methods 16, 1247-1253.

The images are not part of this repository. The notebooks download them.

## Run

On Kaggle: import a notebook from `notebooks/`, set Internet to on and use Save Version > Save & Run All. Notebook 01 runs on CPU; notebooks 02 and 03 need a GPU. Notebook 03 also needs the saved output of notebook 02 (+ Add Input > Your Work), because it loads the trained weights.

## Layout

```
notebooks/01_data_check.ipynb   image types, nuclei per image, nucleus size, touching nuclei, train/val split
notebooks/02_unet.ipynb         three-class U-Net (background, interior, boundary) trained on random crops
notebooks/03_evaluation.ipynb   single nuclei from the pixel classes, DSB score per image type, merges and splits, uncertainty test
docs/plan.md                    question, steps and hypotheses
docs/progress.md                what is done and what comes next
results/                        tables and figures from the notebooks
```

## License

MIT
