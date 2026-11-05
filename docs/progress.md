# Progress log

## 2026-10-31

- Notebook 01 (data check) is done. The 670 training images of BBBC038 stage1 are grouped into three image types (fluorescence, brightfield, histology) and split into train and validation sets per type. Results are in `results/`.
- Notebook 02 (U-Net) is set up: data loading, per-image normalisation, random 256 x 256 crops with flips and rotations, weighted cross-entropy loss (boundary class weight 3) and validation with foreground IoU.
- Next step: write the `UNet` class myself, check the output shape, then train on a Kaggle T4 GPU.

## 2026-11-01

- Notebook 03 (evaluation) is ready. It turns the three pixel classes into single nuclei with a watershed from the interior class, scores every validation image with the Data Science Bowl metric (AP over IoU 0.5 to 0.95) and F1 at IoU 0.5, reports the scores per image type, counts merged and split nuclei, and tests the warning question from the plan: do the 10 % most uncertain images contain the 10 % worst ones?
- The scoring functions were checked on synthetic masks first: a perfect prediction scores 1.0, two touching nuclei predicted as one count as one merge, and a nucleus cut in two counts as one split.
- Next step: unchanged. The U-Net class in notebook 02, then training, then notebook 03 on the trained weights.

## 2026-11-05

- The `UNet` class is in notebook 02 (encoder 32-64-128-256, bottom 512, decoder with skip connections, 1x1 output layer, 7.8 million parameters) and the same class is in notebook 03. Checked on CPU: a 256 x 256 input gives a 256 x 256 output with 3 classes, a full image padded to a multiple of 16 works, one training step runs, and the saved weights load back.
- Notebook 03b added: Cellpose-SAM, a large pretrained model, is run on the same validation images without any training on this dataset and scored with the same functions as notebook 03. With the output of notebook 03 added, it compares both models image by image per image type.
- Next step: train notebook 02 on a Kaggle T4 GPU, then run notebook 03 and 03b.
- First full run on a Kaggle T4, started with `scripts/run_on_kaggle.py`. Training: 40 epochs of about 50 s, best epoch 30 by validation loss, foreground IoU 0.876 on the validation split.
- Validation scores (Data Science Bowl AP / F1 at IoU 0.5): fluorescence 0.596 / 0.891 (109 images), histology 0.276 / 0.643 (22), brightfield 0.284 / 0.621 (3), all 0.536 / 0.844. H1 holds; the brightfield number rests on 3 images.
- Of the 14 worst images, 11 are histology, 2 brightfield and 1 fluorescence. In the worst images the model finds small false objects in empty tissue and merges nuclei in dense clusters.
- H3 with the planned measure (whole-image entropy): 3 of the 14 worst images flagged, 1.46 expected by chance, p = 0.16, so not supported. The nucleus-area entropy (the extra measure) flagged 8 of 14 (p = 3e-6, Spearman -0.75). Inside the fluorescence images alone it still catches 5 of the 11 worst (1.1 by chance), so it does not only detect the image type.
- H2 is still open: merges and splits are at least 30 % of the errors on fluorescence images, but the event counts cannot say more.
- Cellpose-SAM used as it is (03b) scores higher than the U-Net on every image type: all 0.620 vs 0.536, fluorescence 0.653 vs 0.596 (better on 76 of 109 images, Wilcoxon p = 0.0001), histology 0.478 vs 0.276 (better on all 22), brightfield 0.484 vs 0.284 (3 of 3). This is not a clean zero-shot result: Cellpose-SAM was trained on the Cellpose nuclei set, and that set contains BBBC038 images with corrected masks (Stringer et al. 2021, Pachitariu et al. 2025). So it has probably seen many of these validation images. Its score here is best read as an upper bound.
- Next: notebook 03 now gives every error one cause (H2). Notebook 04 tests the nucleus-area entropy on `stage1_test`, which the model has never seen; the test (H3b) was written into `docs/plan.md` before the run.
- The follow-up (H2 breakdown, H3b) was committed before the run (commit b407c25), then notebooks 03 and 04 ran on Kaggle.
- H2 holds. On the validation fluorescence images, 69.5 % of all errors (683 of 983) are merged or cut nuclei, almost all merged (631). On the test fluorescence images it is 69.1 %. On histology test images only 31 % are merged or cut; most errors there are nuclei not found (291) and false alarms (205).
- Test scores (65 images, never seen): all 0.396, fluorescence 0.463 (53 images), histology 0.100 (12). There are no brightfield images in the test set by the type rule. The test histology images hold far more nuclei than the validation ones (89 vs 36 per image).
- H3b holds. The nucleus-area entropy flags 6 of the 7 worst test images, 0.75 expected by chance, p = 6e-7, Spearman -0.73. The whole-image entropy flags 1 of 7.
- Checked after the run, not planned: all 7 worst test images are histology. Flagging 7 random histology images would catch about 4 of them on average, so part of the signal is the image type. Within histology the rank correlation is -0.97 (12 images), within fluorescence -0.54 (53 images, p = 3e-5), but inside fluorescence the top 10 % rule catches only 2 of 6 (0.68 by chance, p = 0.13).
- Next: an exploratory check whether the colour part of the first layer is used at all (histology images turned grey), and Cellpose-SAM on the test images.
