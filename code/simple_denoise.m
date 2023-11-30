infilepath = "images/extracted/0002_NOISY_SRGB/0002_NOISY_SRGB_001.PNG";
% infilepath = "results/nlm_cureor_block/03_underexposure_extrema/3_2_1_092_03_3_noisy.jpg";
% infilepath = "results/nlm_cureor_block/07_dirtylens1_extrema/2_2_5_053_07_1_noisy.jpg";
outfilepath = "./denoised.jpg";
gtfilepath = "images/extracted/0002_GT_SRGB/0002_GT_SRGB_001.PNG";
imageid = "0002_NOISY_SRGB_001.PNG";
resultfilepath = "images/results/results.txt";

% nlm_tuned(infilepath, outfilepath, true);
iqa_fast(outfilepath, gtfilepath, imageid, resultfilepath);
