# Plan

## Question

A nucleus segmentation model can reach a good average score and still fail on whole groups of images. On which images does it fail, and can the model warn us itself, before anyone checks the result by hand?

In a real imaging pipeline nobody can check every image. If the software marks the images that need a second look, the expert only reviews those.

## Steps

1. **Data check** (`01_data_check.ipynb`). Image types, nuclei per image, nucleus size, share of touching nuclei. Split 80/20 by image, stratified by image type, fixed seed.
2. **Model** (`02_unet.ipynb`). A small U-Net written by hand in PyTorch. Every pixel gets one of three classes: background, nucleus interior, nucleus boundary. The boundary class is what separates nuclei that touch.
3. **Evaluation** (`03_evaluation.ipynb`). Turn the pixel classes into single nuclei, match them with the expert masks and score each image: average precision over IoU thresholds 0.5 to 0.95 (the Data Science Bowl metric) and F1 at IoU 0.5. Report the score per image type, not only the average. Show the worst images.
4. **Warning signal.** One uncertainty number per image (mean pixel entropy of the model output). Does it rank the bad images first? If the 10% most uncertain images are flagged, how many of the 10% worst images are among them?

## Hypotheses (written before training)

- H1: Histology and brightfield images score lower than fluorescence images. They are fewer in the training set and look very different.
- H2: On fluorescence images most errors come from touching nuclei that are merged into one or split in two.
- H3: The uncertainty signal catches the worst images clearly better than chance, but it misses mistakes the model makes with high confidence.

## Known limits

- Some masks in `stage1_train` are known to be wrong or incomplete, so a small part of the error is label noise.
- The brightfield group is small, so its score will be unstable.
- 2D images only.

## Done when

One table with scores per image type, one figure with the worst images and their errors, and a written answer to the warning question with numbers.
