import subprocess
import multiprocessing
import os
from tqdm import tqdm
import sys
from copy import deepcopy
from time import sleep
import zipfile
import shutil
import random
import tarfile
import numpy as np
import math

RESULTS_DIR="./results/nlm_cureor/"
DOWNLOAD_DIR="./cache/download/"
EXTRACT_DIR="./cache/extracted/"
DOWNLOAD_LINKS="../datasets/cureor_rgb_noresize_nosaltpepper_download_links.txt"
# NUM_IMAGE_SAMPLES=15  # 10% of the images
NUM_IMAGE_SAMPLES=80
# NUM_IMAGE_SAMPLES=None
DATASET="CURE-OR"
# DATASET="SIDD"

if DATASET == "SIDD":
    NUM_ARCHIVE_SAMPLES=32  # 5% of the archives

if DATASET != "SIDD":
    GT_PATH = "../datasets/cureor_ground_truth/01_no_challenge/"

TEST=False
if TEST:
    if DATASET == "SIDD":
        RESULTS_DIR="./results_sidd_test/nlm_cureor/"
        DOWNLOAD_DIR="./cache_sidd_test/download/"
        EXTRACT_DIR="./cache_sidd_test/extracted/"
        DOWNLOAD_LINKS="./cache_sidd_test/sidd_download_links_test.txt"
        NUM_ARCHIVE_SAMPLES=3
        NUM_IMAGE_SAMPLES=3
    elif DATASET == "CURE-OR":
        RESULTS_DIR="./results_cureor_test/nlm_cureor/"
        DOWNLOAD_DIR="./cache_cureor_test/download/"
        EXTRACT_DIR="./cache_cureor_test/extracted/"
        DOWNLOAD_LINKS="./cache_cureor_test/cureor_rgb_download_links.txt"
        NUM_IMAGE_SAMPLES=3


RESULTS_FILE = os.path.join(RESULTS_DIR, "nlm_cureor_results.txt")
LOG_FILE="./nlm_cureor_log.txt"
# LOG_FILE=None
def log(string):
    if LOG_FILE is None:
        print(string)
    else:
        while True:
            try:
                with open(LOG_FILE, "a") as f:
                    f.write(string + '\n')
                return
            except Exception as e:
                print(e)
                pass

# Name of compressed archive
def get_archive_download_name(link):
    if DATASET == "CURE-OR":
        fname = link[:link.find("?")]
        fname = fname[fname.rfind("/")+1:]
    elif DATASET == "SIDD":
        fname = link.split("/")[-1]
    else:
        log("DATASET not yet supported")
        exit()
    return fname

# Name of the folder in the compressed archive
def get_archive_name(archive_path):
    # This can fail if download was unsuccessfull
    try:
        if DATASET == 'SIDD':
            # zip file
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                return zip_ref.infolist()[0].filename.split('/')[0]
        elif DATASET == 'CURE-OR':
            # tar file
            with tarfile.open(archive_path, 'r:gz') as tar:
                return tar.getnames()[0]
    except Exception as e:
        return None

def download_archive(download_dir, link):
    log(f"Downloading from {link}.")
    fname = get_archive_download_name(link)
    archive_path = os.path.join(download_dir, fname)
    if os.path.exists(archive_path):
        log(f"{fname} already exists, continuing.")
        return
    if TEST:
        log(f'DRY RUN: {" ".join(["wget", "-O", archive_path, link])}')
    else:
        result = subprocess.run(["wget", "-O", archive_path, link])
    if os.path.exists(archive_path):
        log(f"Downloaded {fname} successfully")
    else:
        log(f"ERROR: Expected archive {archive_path} to exist after download")

def extract_archive(archive_path, extract_dir, archive_extract_dir):
    log(f"Unzipping {archive_path} to {extract_dir}")
    if os.path.exists(archive_extract_dir):
        log(f"Extracted archive {archive_extract_dir} already exists, continuing")
        return
    os.makedirs(extract_dir, exist_ok=True)
    if TEST:
        log(f'DRY RUN: {" ".join(["unzip", archive_path, "-d", extract_dir])}')
    else:
        if DATASET == 'CURE-OR':
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(extract_dir)
        elif DATASET == 'SIDD':
            result = subprocess.run(["unzip", archive_path, "-d", extract_dir])
        else:
            log("DATASET not yet supported")
        log(f"Deleting archive {archive_path}")
        try:
            # shutil.rmtree(archive_path)
            # Won't remove if it was already there
            os.remove(archive_path)
        except:
            pass

def walk_dataset(dataset_path, results_path):
    for (dirpath, dirnames, filenames) in os.walk(dataset_path):
        outdirpath = dirpath.replace(dataset_path, results_path)
        if len(filenames) > 0:
            os.makedirs(outdirpath, exist_ok=True)
        for file in filenames:
            infilepath = os.path.join(dirpath, file)
            # outfilepath = os.path.join(outdirpath, file.replace(".jpg", ".png"))
            outfilepath = os.path.join(outdirpath, file)
            dataset_relpath = infilepath.replace(dataset_path, "")
            yield (infilepath, outfilepath, dataset_relpath)

def run_nlm(dataset_path, results_path):
    if "GT" in dataset_path:  # For SIDD GT means it's ground truth
        log(f"Skipping denoising of ground truth archive {dataset_path}")
        return
    log(f"Running NLM on {dataset_path}")
    from matlab import engine
    ENG = engine.start_matlab()
    log(f"MATLAB started")
    # Sample from the dataset_path
    files = []
    for path in walk_dataset(dataset_path, results_path):
        files.append(path)
    if NUM_IMAGE_SAMPLES is not None:
        files = random.sample(files, NUM_IMAGE_SAMPLES)
        log(f"Sampled the following files for denoising: {[path[0] for path in files]}")
    else:
        log(f"Running denoising on all images")
    for (infilepath, outfilepath, dataset_relpath) in files:
        is_rgb = True
        if '.MAT' in infilepath:
            is_rgb = False
        # if False:
        if TEST:
            log(f"DRY RUN: nlm({infilepath}, {outfilepath}, {is_rgb})")
        else:
            log(f"nlm({infilepath}, {outfilepath}, {is_rgb})")
            if os.path.exists(outfilepath):
                log(f"{outfilepath} exists, continuing")
                continue
            ENG.nlm(infilepath, outfilepath, is_rgb, nargout=0)
    ENG.exit()

def eval_dataset(dataset_path, result_file_path):
    from matlab import engine
    # Don't evaluate ground truth files
    if "GT" in dataset_path:  # For SIDD dataset
        log(f"Skipping evaluation of ground truth archive {dataset_path}")
        return
    ENG = engine.start_matlab()
    for (denoised_filepath, _, dataset_relpath) in walk_dataset(dataset_path, dataset_path):
        if DATASET == "SIDD":
            gt_filepath = denoised_filepath.replace("NOISY", "GT")
            gt_filepath = gt_filepath.replace(RESULTS_DIR, EXTRACT_DIR)
        elif DATASET == "CURE-OR":
            # Remove Level_X for CURE-OR which is first folder in dataset_relpath
            gt_relpath = dataset_relpath[dataset_relpath[1:].find("/")+2:]
            gt_filepath = os.path.join(GT_PATH, gt_relpath)
            gt_filepath = list(gt_filepath)  # List so we can edit at indexes
            gt_filepath[-5] = '0'  # Challenge level to 0
            gt_filepath[-8] = '0'  # Challenge type to 01
            gt_filepath[-7] = '1'  # Challenge type to 01
            gt_filepath = "".join(gt_filepath)
        else:
            log("DATASET not supported by eval_dataset")
            return
        # GT file will be downloaded after in pipeline
        while not os.path.exists(gt_filepath):
            log(f"Waiting for ground truth file {gt_filepath} to exist")
            sleep(5)
        log(f"--------------\nEvaluating denoised file {denoised_filepath}\nwith ground truth file {gt_filepath}\n--------------")
        # rekognition_accuracy = rekognition(denoised_filepath)
        dataset_name = os.path.basename(dataset_path)
        image_id = dataset_name + dataset_relpath
        ENG.iqa_fast(denoised_filepath, gt_filepath, image_id, result_file_path, nargout=0)
    ENG.exit()

def process_results(result_file, archive_name):
    while True:
        try:
            with open(result_file, "r") as f:
                results = f.readlines()
            break
        except:
            log("Unable to open results file for processing")
            sleep(5)
    result_norms = []
    for result in results:
        result_fields = result.split(" ")
        if archive_name not in result_fields[0]:
            continue
        l2_norm = 0
        for metric in result_fields[1:]:
            l2_norm += float(metric) ** 2
        l2_norm = math.sqrt(l2_norm)
        result_norms.append((result_fields[0], l2_norm))
    result_norms = np.array(result_norms)
    # GET MAX/MIN
    max_result_id = result_norms[np.argmax(result_norms[:, 1].astype(np.float32))][0]
    min_result_id = result_norms[np.argmin(result_norms[:, 1].astype(np.float32))][0]
    # COPY FILE
    extrema_dir = os.path.join(RESULTS_DIR, archive_name + '_extrema/')
    os.makedirs(extrema_dir, exist_ok=True)
    # archive_path = os.path.join(RESULTS_DIR, archive_name)
    max_image_path = os.path.join(RESULTS_DIR, max_result_id)
    min_image_path = os.path.join(RESULTS_DIR, min_result_id)
    shutil.copy(max_image_path, extrema_dir)
    shutil.copy(min_image_path, extrema_dir)
    #### MAYBE ALSO COPY NOISY IMAGES? #####

def clean_result_files(archive_results_dir):
    ###### REMOVE EXTRACTED NOISY FILES AND PROCESSED FILES ############
    archive_extract_dir = archive_results_dir.replace(RESULTS_DIR, EXTRACT_DIR)
    log(f"Removing {archive_results_dir}")
    log(f"Removing {archive_extract_dir}")
    if not TEST:
        try:
            shutil.rmtree(archive_results_dir)
        except:
            pass
        try:
            shutil.rmtree(archive_extract_dir)
        except:
            pass


if __name__ == "__main__":
    if os.path.exists(RESULTS_FILE):
        print(f"MOVE THE EXISTING RESULT FILE AT {RESULTS_FILE} BEFORE RUNNING")
        sys.exit()
    if LOG_FILE is not None:
        try:
            os.remove(LOG_FILE)
        except:
            pass

    print(f"Status is now in {LOG_FILE}")
    log(f"Making directories \n{RESULTS_DIR}\n{DOWNLOAD_DIR}\n{EXTRACT_DIR}")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    with open(DOWNLOAD_LINKS, "r") as f:
        links = [link.strip() for link in f.readlines()]

    if DATASET == "SIDD":
        sample_idxs = range(int(len(links) / 2))
        link_idxs = random.sample(sample_idxs, NUM_ARCHIVE_SAMPLES)
        sampled_links = []
        for link_idx in link_idxs:
            sampled_links.append(links[link_idx * 2])  # Noisy
            sampled_links.append(links[link_idx * 2 + 1])  # Ground truth follows noisy
        links = sampled_links

        log(f"Sampled the following links for this run {links}")

    DOWNLOAD_STAGE = None
    EXTRACT_STAGE = None
    DENOISE_STAGE = None
    NOP_STAGE = None  # This is so our ground truth archive can get out of denoise while we eval
    EVAL_STAGE = None

    DOWNLOAD_STAGE_PATH = None
    EXTRACT_STAGE_PATH = None
    DENOISE_STAGE_PATH = None
    NOP_STAGE_PATH = None
    EVAL_STAGE_PATH = None

    archive_idx = 0
    consumed_all_links = False

    while True:
        # EVAL -> CLEANUP
        if EVAL_STAGE is not None and not EVAL_STAGE.is_alive():
            log("EVAL STAGE")
            EVAL_STAGE.join()
            process_results(RESULTS_FILE, EVAL_STAGE_PATH.replace(RESULTS_DIR, ""))
            clean_result_files(EVAL_STAGE_PATH)
            log("IS DONE")
            EVAL_STAGE = None
            EVAL_STAGE_PATH = None
            if consumed_all_links == True and all(stage is None for stage in [DOWNLOAD_STAGE, EXTRACT_STAGE, DENOISE_STAGE, NOP_STAGE, EVAL_STAGE]):
                log("PIPELINE FINISHED, EXITING")
                break
        # NOP -> EVAL
        if NOP_STAGE is not None:
            if EVAL_STAGE is None:
                log("NOP STAGE")
                log("IS DONE")
                archive_results_dir = deepcopy(NOP_STAGE_PATH)
                EVAL_STAGE = multiprocessing.Process(target=eval_dataset, args=(archive_results_dir, RESULTS_FILE))
                EVAL_STAGE.start()
                EVAL_STAGE_PATH = archive_results_dir
                NOP_STAGE = None
                NOP_STAGE_PATH = None
        # DENOISE -> NOP
        if DENOISE_STAGE is not None and not DENOISE_STAGE.is_alive():
            if NOP_STAGE is None:
                log("DENOISE STAGE")
                DENOISE_STAGE.join()
                log("IS DONE")
                archive_results_dir = deepcopy(DENOISE_STAGE_PATH)
                NOP_STAGE = True
                NOP_STAGE_PATH = archive_results_dir
                DENOISE_STAGE = None
                DENOISE_STAGE_PATH = None
        # EXTRACT -> DENOISE
        if EXTRACT_STAGE is not None and not EXTRACT_STAGE.is_alive():
            if DENOISE_STAGE is None:
                log("EXTRACT STAGE")
                EXTRACT_STAGE.join()
                log("IS DONE")
                archive_extract_dir = deepcopy(EXTRACT_STAGE_PATH)
                archive_results_dir = archive_extract_dir.replace(EXTRACT_DIR, RESULTS_DIR)
                DENOISE_STAGE = multiprocessing.Process(target=run_nlm, args=(archive_extract_dir, archive_results_dir))
                DENOISE_STAGE.start()
                DENOISE_STAGE_PATH = archive_results_dir
                EXTRACT_STAGE = None
                EXTRACT_STAGE_PATH = None
        # DOWNLOAD -> EXTRACT
        if DOWNLOAD_STAGE is not None and not DOWNLOAD_STAGE.is_alive():
            if EXTRACT_STAGE is None:
                log("DOWNLOAD STAGE")
                DOWNLOAD_STAGE.join()
                log("IS DONE")
                link = deepcopy(DOWNLOAD_STAGE_PATH)
                archive_name = get_archive_download_name(link)
                archive_path = os.path.join(DOWNLOAD_DIR, archive_name)
                folder_name = get_archive_name(archive_path)
                if folder_name is None:
                    # unizipping failed, so restart download
                    log(f"failed to open {archive_path}, removing it and restarting download")
                    if not TEST:
                        try:
                            os.remove(archive_path)
                        except:
                            pass
                    DOWNLOAD_STAGE_PATH = link
                    DOWNLOAD_STAGE = multiprocessing.Process(target=download_archive, args=(DOWNLOAD_DIR, link))
                    DOWNLOAD_STAGE.start()
                    continue
                archive_extract_dir = os.path.join(EXTRACT_DIR, folder_name)
                log(f"Starting extract from {archive_path} to {archive_extract_dir}")
                EXTRACT_STAGE_PATH = archive_extract_dir
                EXTRACT_STAGE = multiprocessing.Process(target=extract_archive, args=(archive_path, EXTRACT_DIR, archive_extract_dir))
                EXTRACT_STAGE.start()
                DOWNLOAD_STAGE = None
                DOWNLOAD_STAGE_PATH = None
        # -> DOWNLOAD
        if DOWNLOAD_STAGE is None:
            if archive_idx >= len(links):
                consumed_all_links = True
                sleep(1)
                continue
            link = links[archive_idx]
            archive_path = os.path.join(DOWNLOAD_DIR, link.split("/")[-1])
            DOWNLOAD_STAGE_PATH = link
            log(f"-----\nPIPELINE STARTING ARCHIVE {archive_path}\n-----")
            DOWNLOAD_STAGE = multiprocessing.Process(target=download_archive, args=(DOWNLOAD_DIR, link))
            DOWNLOAD_STAGE.start()
            archive_idx += 1

        sleep(1)

