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

RESULTS_DIR="./results/nlm_sidd_lab/"
DOWNLOAD_DIR="./cache/download/"
EXTRACT_DIR="./cache/extracted/"
DOWNLOAD_LINKS="../datasets/sidd_rgb_download_links.txt"
NUM_ARCHIVE_SAMPLES=32  # 5% of the archives
NUM_IMAGE_SAMPLES=15  # 10% of the images


TEST=False
if TEST:
    RESULTS_DIR="./results_test/nlm_sidd/"
    DOWNLOAD_DIR="./cache_test/download/"
    EXTRACT_DIR="./cache_test/extracted/"
    DOWNLOAD_LINKS="./cache_test/sidd_download_links_test.txt"
    NUM_ARCHIVE_SAMPLES=3
    NUM_IMAGE_SAMPLES=3

RESULTS_FILE = os.path.join(RESULTS_DIR, "nlm_sidd_lab_results.txt")
LOG_FILE="./nlm_sidd_lab_log.txt"
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
            except:
                pass

def download_archive(download_dir, link):
    log(f"Downloading from {link}.")
    fname = link.split("/")[-1]
    archive_path = os.path.join(download_dir, fname)
    if os.path.exists(archive_path):
        log(f"{fname} already exists, continuing.")
        return
    if TEST:
        log(f'DRY RUN: {" ".join(["wget", "-P", download_dir, link])}')
    else:
        result = subprocess.run(["wget", "-P", download_dir, link])
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
        result = subprocess.run(["unzip", archive_path, "-d", extract_dir])
        log(f"Deleting archive {archive_path}")
        try:
            # shutil.rmtree(archive_path)
            # Won't remove if it was already there
            os.remove(archive_path)
        except:
            pass

def get_archive_name(archive_path):
    # This can fail if download was unsuccessfull
    try:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            return zip_ref.infolist()[0].filename.split('/')[0]
    except:
        return None

def walk_dataset(dataset_path, results_path):
    for (dirpath, dirnames, filenames) in os.walk(dataset_path):
        outdirpath = dirpath.replace(dataset_path, results_path)
        os.makedirs(outdirpath, exist_ok=True)
        for file in filenames:
            infilepath = os.path.join(dirpath, file)
            outfilepath = os.path.join(outdirpath, file.replace(".jpg", ".png"))
            dataset_relpath = infilepath.replace(dataset_path, "")
            yield (infilepath, outfilepath, dataset_relpath)

def run_nlm(dataset_path, results_path):
    if "GT" in dataset_path:
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
    sampled_files = random.sample(files, NUM_IMAGE_SAMPLES)
    log(f"Sampled the following files for denoising: {[path[0] for path in sampled_files]}")
    for (infilepath, outfilepath, dataset_relpath) in sampled_files:
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
    if "GT" in dataset_path:
        log(f"Skipping evaluation of ground truth archive {dataset_path}")
        return
    ENG = engine.start_matlab()
    for (denoised_filepath, _, dataset_relpath) in walk_dataset(dataset_path, dataset_path):
        gt_filepath = denoised_filepath.replace("NOISY", "GT")
        gt_filepath = gt_filepath.replace(RESULTS_DIR, EXTRACT_DIR)
        # GT file will be downloaded after in pipeline
        while not os.path.exists(gt_filepath):
            log("Waiting for ground truth file {gt_filepath} to exist")
            sleep(5)
        log(f"--------------\nEvaluating denoised file {denoised_filepath}\nwith ground truth file {gt_filepath}\n--------------")
        # rekognition_accuracy = rekognition(denoised_filepath)
        image_id = dataset_relpath
        if image_id[0] == "/":
            image_id = image_id[1:]
        image_id = image_id.replace("/", "-")
        ENG.iqa_fast(denoised_filepath, gt_filepath, image_id, result_file_path, nargout=0)
    ENG.exit()

def clean_result_files(archive_results_dir):
    ###### CALCULATE STATISTICS HERE AND SAVE BEST/WORST IMAGES ########
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

    download_time = 10 # minutes
    denoise_runtime = 0.5 # minutes
    print("Estimated Runtime is {} hours".format(max(NUM_ARCHIVE_SAMPLES * download_time, NUM_IMAGE_SAMPLES * denoise_runtime)/60))
    print(f"Status is now in {LOG_FILE}")
    log(f"Making directories \n{RESULTS_DIR}\n{DOWNLOAD_DIR}\n{EXTRACT_DIR}")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    with open(DOWNLOAD_LINKS, "r") as f:
        links = [link.strip() for link in f.readlines()]
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
                archive_path = os.path.join(DOWNLOAD_DIR, link.split("/")[-1])
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

#     for link in links:
#         archive_path = download_archive(DOWNLOAD_DIR, link)
#         if archive_path is None:
#             continue
#         # extract_archive(archive_path, EXTRACT_DIR)
#         nlm_sidd_results_dir = os.path.join(RESULTS_DIR, "nlm_sidd/")
#         nlm_sidd_results_file = os.path.join(nlm_sidd_results_dir, "nlm_sidd_results.txt")
#         run_nlm(EXTRACT_DIR, nlm_sidd_results_dir)
#         eval_dataset(nlm_sidd_results_dir, nlm_sidd_results_file)

