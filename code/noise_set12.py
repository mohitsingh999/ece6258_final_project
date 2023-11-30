import dippykit
import os
import scipy
import numpy as np
import IPython

dirpath = "../datasets/set12/"
gt_dirpath = os.path.join(dirpath, "GT/")

for fname in os.listdir(gt_dirpath):
    gt_fpath = os.path.join(gt_dirpath, fname)
    im = dippykit.imread(gt_fpath)
    for sigma in ['0.01', '0.10', '1.00', '10.0']:
        challenge = 'blur'
        challenge_dirpath = os.path.join(dirpath, challenge + sigma.replace(".", "-"))
        os.makedirs(challenge_dirpath, exist_ok=True)

        sigma = float(sigma)
        im_noisy = (scipy.ndimage.gaussian_filter(im, sigma) * 255).astype(np.uint8)
        dippykit.im_write(im_noisy, os.path.join(challenge_dirpath, fname))
        dippykit.imshow(im_noisy)
        # dippykit.show()

    for sigma in ['0.01', '0.03', '0.05', '0.10']:
        challenge = 'additive'
        challenge_dirpath = os.path.join(dirpath, challenge + sigma.replace(".", "-"))
        os.makedirs(challenge_dirpath, exist_ok=True)

        sigma = float(sigma)
        noise = np.random.randn(*im.shape) * sigma
        im_noisy = np.clip((im + noise), 0, 1)
        im_noisy = (im_noisy * 255).astype(np.uint8)
        dippykit.im_write(im_noisy, os.path.join(challenge_dirpath, fname))
        # dippykit.imshow(im_noisy)
