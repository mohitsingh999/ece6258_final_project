import subprocess
import multiprocessing
import os
from tqdm import tqdm
import sys
from copy import deepcopy
from time import sleep
import zipfile
import shutil

RESULTS_DIR="./results/nlm_sidd/"
DOWNLOAD_DIR="./cache/download/"
EXTRACT_DIR="./cache/extracted/"
DOWNLOAD_LINKS="../datasets/sidd_download_links.txt"

TEST=False
if TEST:
    RESULTS_DIR="./results_test/nlm_sidd/"
    DOWNLOAD_DIR="./cache_test/download/"
    EXTRACT_DIR="./cache_test/extracted/"
    DOWNLOAD_LINKS="../datasets/sidd_download_links.txt"

LOG_FILE="./log.txt"
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
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        return zip_ref.infolist()[0].filename.split('/')[0]

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
    log(f"Running NLM")
    log(dataset_path)
    from matlab import engine
    ENG = engine.start_matlab()
    for (infilepath, outfilepath, dataset_relpath) in walk_dataset(dataset_path, results_path):
        if 'NOISY' in infilepath:
            is_rgb = True
            if '.MAT' in infilepath:
                is_rgb = False
            if TEST:
                log(f"DRY RUN: nlm({infilepath}, {outfilepath}, {is_rgb})")
            else:
                log(f"nlm({infilepath}, {outfilepath}, {is_rgb})")
                if os.path.exists(outfilepath):
                    log(f"{outfilepath} exists, continuing")
                    continue
                ENG.nlm(infilepath, outfilepath, is_rgb, nargout=0)

def eval_dataset(dataset_path, result_file_path):
    from matlab import engine
    # Don't evaluate ground truth files
    if "GT" in dataset_path:
        return
    ENG = engine.start_matlab()
    for (denoised_filepath, _, dataset_relpath) in walk_dataset(dataset_path, dataset_path):
        gt_filepath = denoised_filepath.replace("NOISY", "GT")
        # GT file will be downloaded after in pipeline
        log(f"--------------\nEvaluating denoised file {denoised_filepath}\nwith ground truth file {gt_filepath}\n--------------")
        while not os.path.exists(gt_filepath):
            log("Waiting for ground truth to download")
            sleep(5)
        # rekognition_accuracy = rekognition(denoised_filepath)
        image_id = dataset_relpath.replace("/", "-")
        image_id = image_id.replace("\\", "-")
        ENG.iqa(denoised_filepath, gt_filepath, image_id, result_file_path, 0)

def clean_result_files(archive_results_dir):
    ###### CALCULATE STATISTICS HERE AND SAVE BEST/WORST IMAGES ########
    archive_extract_dir = archive_results_dir.replace(RESULTS_DIR, EXTRACT_DIR)
    log(f"Removing {archive_results_dir}")
    log(f"Removing {archive_extract_dir}")
    if not TEST:
        try:
            shutil.rmtree(archive_results_dir)
            shutil.rmtree(archive_extract_dir)
        except:
            pass


if __name__ == "__main__":
    if LOG_FILE is not None:
        try:
            os.remove(LOG_FILE)
        except:
            pass
    log(f"Making directories \n{RESULTS_DIR}\n{DOWNLOAD_DIR}\n{EXTRACT_DIR}")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    with open(DOWNLOAD_LINKS, "r") as f:
        links = [link.strip() for link in f.readlines()]

    DOWNLOAD_STAGE = None
    EXTRACT_STAGE = None
    DENOISE_STAGE = None
    EVAL_STAGE = None

    DOWNLOAD_STAGE_PATH = None
    EXTRACT_STAGE_PATH = None
    DENOISE_STAGE_PATH = None
    EVAL_STAGE_PATH = None

    archive_idx = 0
    consumed_all_links = False

    while True:
        if EVAL_STAGE is not None and not EVAL_STAGE.is_alive():
            log("EVAL STAGE")
            EVAL_STAGE.join()
            clean_result_files(EVAL_STAGE_PATH)
            log("IS DONE")
            EVAL_STAGE = None
            EVAL_STAGE_PATH = None
            if consumed_all_links == True and all(stage is None for stage in pipeline):
                break
        if DENOISE_STAGE is not None and not DENOISE_STAGE.is_alive():
            if EVAL_STAGE is None:
                log("DENOISE STAGE")
                DENOISE_STAGE.join()
                log("IS DONE")
                archive_results_dir = deepcopy(DENOISE_STAGE_PATH)
                results_file = os.path.join(archive_results_dir, "../results.txt")
                EVAL_STAGE = multiprocessing.Process(target=eval_dataset, args=(archive_results_dir, results_file))
                EVAL_STAGE.start()
                EVAL_STAGE_PATH = archive_results_dir
                DENOISE_STAGE = None
                DENOISE_STAGE_PATH = None
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
        if DOWNLOAD_STAGE is not None and not DOWNLOAD_STAGE.is_alive():
            if EXTRACT_STAGE is None:
                log("DOWNLOAD STAGE")
                DOWNLOAD_STAGE.join()
                log("IS DONE")
                download_path = deepcopy(DOWNLOAD_STAGE_PATH)
                folder_name = get_archive_name(download_path)
                archive_extract_dir = os.path.join(EXTRACT_DIR, folder_name)
                log(f"Starting extract from {download_path} to {archive_extract_dir}")
                EXTRACT_STAGE_PATH = archive_extract_dir
                EXTRACT_STAGE = multiprocessing.Process(target=extract_archive, args=(download_path, EXTRACT_DIR, archive_extract_dir))
                EXTRACT_STAGE.start()
                DOWNLOAD_STAGE = None
                DOWNLOAD_STAGE_PATH = None
        if DOWNLOAD_STAGE is None:
            if TEST and archive_idx >= 1:
                sleep(1)
                continue
            if archive_idx >= len(links):
                consumed_all_links = True
                sleep(1)
                continue
            link = links[archive_idx]
            archive_path = os.path.join(DOWNLOAD_DIR, link.split("/")[-1])
            DOWNLOAD_STAGE_PATH = archive_path
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

