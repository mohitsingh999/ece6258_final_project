from matplotlib import pyplot as plt
import scipy
from matlab import engine
import time
import os

DATASET_PATH = "/media/nwitt/Seagate Portable Drive/6258 Project/cureor/full/"
RESULT_PATH = "/media/nwitt/Seagate Portable Drive/6258 Project/cureor/full_denoised/"
DRY_RUN = True

if not DRY_RUN:
    eng = engine.start_matlab()

start = time.time()

for (dirpath, dirnames, filenames) in os.walk(DATASET_PATH):
    outdirpath = dirpath.replace(DATASET_PATH, RESULT_PATH)
    os.makedirs(outdirpath)
    for file in filenames:
        infilepath = os.path.join(dirpath, file)
        outfilepath = os.path.join(outdirpath, file.replace(".jpg", ".png"))
        print(f"{infilepath} -> {outfilepath}")
        break
        if not DRY_RUN:
            eng.nlm(infilepath, outfilepath, nargout=0)
    break

stop = time.time()

print(f"Time elapsed {stop - start}s")
