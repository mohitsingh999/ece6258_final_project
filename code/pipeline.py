import subprocess
import multiprocessing
import os
from tqdm import tqdm
import sys
from copy import deepcopy
from time import sleep

RESULTS_DIR="./results/nlm_sidd/"
DOWNLOAD_DIR="./cache/download/"
EXTRACT_DIR="./cache/extracted/"
DOWNLOAD_LINKS="../datasets/sidd_download_links.txt"

TEST=False

def download_archive(download_dir, link):
    print(f"Downloading from {link}.")
    fname = link.split("/")[-1]
    archive_path = os.path.join(download_dir, fname)
    if os.path.exists(archive_path):
        print(f"{fname} already exists, continuing.")
        return
    if TEST:
        print(f'DRY RUN: {" ".join(["wget", "-P", download_dir, link])}')
    else:
        result = subprocess.run(["wget", "-P", download_dir, link])
    if os.path.exists(archive_path):
        print(f"Downloaded {fname} successfully")
    else:
        print(f"ERROR: Expected archive {archive_path} to exist after download")

def extract_archive(archive_path, extract_dir):
    print(f"Unzipping {archive_path} to {extract_dir}")
    if os.path.exists(extract_dir):
        print(f"Extracted archive {extract_dir} already exists, continuing")
        return
    os.makedirs(extract_dir, exist_ok=True)
    if TEST:
        print(f'DRY RUN: {" ".join(["unzip", archive_path, "-d", extract_dir])}')
    else:
        result = subprocess.run(["unzip", archive_path, "-d", extract_dir])

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
    print(f"Running NLM")
    from matlab import engine
    ENG = engine.start_matlab()
    for (infilepath, outfilepath, dataset_relpath) in walk_dataset(dataset_path, results_path):
        if 'NOISY' in infilepath:
            is_rgb = True
            if '.MAT' in infilepath:
                is_rgb = False
            if TEST:
                print(f"DRY RUN: nlm({infilepath}, {outfilepath}, {is_rgb})")
            else:
                print(f"nlm({infilepath}, {outfilepath}, {is_rgb})")
                ENG.nlm(infilepath, outfilepath, is_rgb, nargout=0)

def eval_dataset(dataset_path, result_file_path):
    pass
#     global ENG
#     for (infilepath, _, dataset_relpath) in walk_dataset(dataset_path, dataset_path):
# 
#         csv = ENG.csv(infilepath, nargout=1)
#         ms_unique = ENG.ms_unique(infilepath, nargout=1)
#         summer = ENG.summer(infilepath, nargout=1)
#         unique = ENG.unique(infilepath, nargout=1)
#         rekognition_accuracy = rekognition(infilepath)
# 
#         image_id = datase_relpath.replace("/", "-")
#         image_id = datase_relpath.replace("\\", "-")
#         entry = f"{image_id} {csv} {summer} {unique} {ms_unique} {rekognition_accuracy}"
#         with open(result_file_path, "w+") as f:
#             f.write(entry + "\r\n")

if __name__ == "__main__":
    print(f"Making directories \n{RESULTS_DIR}\n{DOWNLOAD_DIR}\n{EXTRACT_DIR}")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    with open(DOWNLOAD_LINKS, "r") as f:
        links = [link.strip() for link in f.readlines()]

    pipeline = [None, None, None, None]
    archive_paths = [None, None, None, None]
    archive_idx = 0
    consumed_all_links = False

    while True:
        if pipeline[3] is not None and not pipeline[3].is_alive():
            pipeline[3].join()
            pipeline[3] = None
            archive_paths[3] = None
            if consumed_all_links == True and all(stage is None for stage in pipeline):
                break
        if pipeline[2] is not None and not pipeline[2].is_alive():
            if pipeline[3] is None:
                pipeline[2].join()
                results_dir = deepcopy(archive_paths[2])
                results_file = os.path.join(results_dir, "results.txt")
                pipeline[3] = multiprocessing.Process(target=eval_dataset, args=(results_dir, results_file))
                pipeline[3].start()
                archive_paths[3] = results_dir
                pipeline[2] = None
                archive_paths[2] = None
        if pipeline[1] is not None and not pipeline[1].is_alive():
            if pipeline[2] is None:
                pipeline[1].join()
                extract_dir = deepcopy(archive_paths[1])
                results_dir = extract_dir.replace(EXTRACT_DIR, RESULTS_DIR)
                pipeline[2] = multiprocessing.Process(target=run_nlm, args=(extract_dir, results_dir))
                pipeline[2].start()
                archive_paths[2] = results_dir
                pipeline[1] = None
                archive_paths[1] = None
        if pipeline[0] is not None and not pipeline[0].is_alive():
            if pipeline[1] is None:
                pipeline[0].join()
                download_path = deepcopy(archive_paths[0])
                extract_path = download_path.replace(DOWNLOAD_DIR, EXTRACT_DIR)
                pipeline[1] = multiprocessing.Process(target=extract_archive, args=(download_path, extract_path))
                pipeline[1].start()
                archive_paths[1] = extract_path
                pipeline[0] = None
                archive_paths[0] = None
        if pipeline[0] is None:
            if archive_idx >= len(links):
                consumed_all_links = True
                sleep(1)
                continue
            link = links[archive_idx]
            archive_path = os.path.join(DOWNLOAD_DIR, link.split("/")[-1])
            archive_paths[0] = archive_path
            print(f"PIPELINE STARTING ARCHIVE {archive_path}")
            pipeline[0] = multiprocessing.Process(target=download_archive, args=(DOWNLOAD_DIR, link))
            pipeline[0].start()
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

