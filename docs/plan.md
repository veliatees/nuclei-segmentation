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

## Follow-up after the first run (written on 2026-11-05, before notebook 04 was run)

What the first run on the validation split showed: mean score 0.536 over 134 images; fluorescence 0.596, histology 0.276, brightfield 0.284 (only 3 images). The planned warning signal, the mean pixel entropy over the whole image, flagged 3 of the 14 worst images, with 1.46 expected by chance (p = 0.16). So H3 is not supported with the planned measure. This mean grows with the number and size of the nuclei in the picture (Spearman 0.56 with the nucleus count), so a sparse image with badly found nuclei can still look calm. The entropy over the nucleus area only, reported as an extra, flagged 8 of 14 (p < 0.0001). It was the second measure, not the planned one, so it is only a lead.

H2 cannot be answered from the event counts: merges and splits are at least 30 % of the errors on fluorescence images, but the counts say no more than that.

Fixed now, before any further run:

- **H2, measured properly.** Every missed nucleus and every extra prediction at IoU 0.5 gets exactly one cause: merged, cut, not found / false alarm, or bad outline (`error_types` in notebook 03). H2 holds if merged or cut nuclei are more than half of all errors on fluorescence images.
- **H3b, a test on new images.** Data: the `stage1_test` images with the expert masks from `stage1_solution.csv`. They played no part in training or in any choice so far. Model: the same weights (best epoch of notebook 02) and the same post-processing, nothing tuned. The 10 % of test images with the highest nucleus-area entropy are flagged (7 images if the set has 65) and compared with the 10 % of images with the lowest score. H3b holds if the overlap is larger than chance with p < 0.05 in a one-sided hypergeometric test; with 65 images this needs at least 3 of 7. The result is reported either way.
