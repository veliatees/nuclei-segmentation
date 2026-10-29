# Nucleus segmentation: where it fails, and can the model tell?

A small study on the nuclei images of the 2018 Data Science Bowl (BBBC038). I train a U-Net that finds every nucleus in an image, compare its output with the expert masks for each image type, and test one practical question: can the model's own uncertainty point to the images that need a second look by a person?

Status: step 1, data check. The plan, with the hypotheses, is in `docs/plan.md` and was written before any training.

## Data

BBBC038v1 from the Broad Bioimage Benchmark Collection (https://bbbc.broadinstitute.org/BBBC038), training set `stage1_train`: microscopy images with an expert mask for every nucleus. Fluorescence, brightfield and histology images, different magnifications and cell types. License: CC0.

Caicedo et al. (2019). Nucleus segmentation across imaging experiments: the 2018 Data Science Bowl. Nature Methods 16, 1247-1253.

The images are not part of this repository. The notebooks download them.

## Run

On Kaggle: import a notebook from `notebooks/`, set Internet to on and use Save Version > Save & Run All. Notebook 01 runs on CPU; the training notebook needs a GPU.

## Layout

```
notebooks/01_data_check.ipynb   image types, nuclei per image, nucleus size, touching nuclei, train/val split
docs/plan.md                    question, steps and hypotheses
results/                        tables and figures from the notebooks
```

## License

MIT
