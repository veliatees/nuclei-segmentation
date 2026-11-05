# Nucleus segmentation: where it fails, and can the model tell?

A small study on the nuclei images of the 2018 Data Science Bowl (BBBC038). I train a U-Net that finds every nucleus in an image, compare its output with the expert masks for each image type, and test one practical question: can the model's own uncertainty point to the images that need a second look by a person?

Status: the U-Net is trained and evaluated on the validation split (first results in `docs/progress.md`). Notebook 03b compares a pretrained generalist model (Cellpose-SAM, used as it is) on the same images and metrics. Its training data includes the Cellpose nuclei set, which contains BBBC038 images, so it has probably seen many of these validation images before. Notebook 04 tests the warning signal on the `stage1_test` images, which the model has never seen; that test was fixed in `docs/plan.md` before it was run. The plan, with the hypotheses, was written before any training.

## Data

BBBC038v1 from the Broad Bioimage Benchmark Collection (https://bbbc.broadinstitute.org/BBBC038), training set `stage1_train`: microscopy images with an expert mask for every nucleus. Fluorescence, brightfield and histology images, different magnifications and cell types. License: CC0.

Caicedo et al. (2019). Nucleus segmentation across imaging experiments: the 2018 Data Science Bowl. Nature Methods 16, 1247-1253.

The images are not part of this repository. The notebooks download them.

## Run

On Kaggle: import a notebook from `notebooks/`, set Internet to on and use Save Version > Save & Run All. Notebook 01 runs on CPU; notebooks 02 and 03 need a GPU. Notebooks 03 and 04 also need the saved output of notebook 02 (+ Add Input > Your Work), because they load the trained weights.

Or all three in a row from your own computer with the Kaggle API: `python scripts/run_on_kaggle.py`. It runs 02, 03, 03b and 04 one after the other on Kaggle GPUs, passes each output on to the next notebook and downloads the results into `runs/`. The one-time setup is at the top of the script.

## Layout

```
notebooks/01_data_check.ipynb   image types, nuclei per image, nucleus size, touching nuclei, train/val split
notebooks/02_unet.ipynb         three-class U-Net (background, interior, boundary) trained on random crops
notebooks/03_evaluation.ipynb   single nuclei from the pixel classes, DSB score per image type, merges and splits, uncertainty test
notebooks/03b_cellpose_baseline.ipynb  Cellpose-SAM used as it is, same validation images and metrics, paired comparison with the U-Net
notebooks/04_test_set.ipynb     same model and scoring on stage1_test (never seen), confirmatory test of the warning signal
scripts/run_on_kaggle.py        runs 02 -> 03 -> 03b -> 04 on Kaggle and downloads the results
docs/plan.md                    question, steps and hypotheses
docs/progress.md                what is done and what comes next
results/                        tables and figures from the notebooks
```

## License

MIT
