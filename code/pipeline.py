import subprocess
import os
from matlab import engine

RESULTS_DIR="./results/"
DOWNLOAD_DIR="./cache/"
EXTRACT_DIR="./cache/extracted/"
DOWNLOAD_LINKS="../datasets/sidd_download_links.txt"

def download_archive(download_dir, link):
    print(f"Downloading from {link}.")
    fname = links.split("/")[-1]
    result = subprocess.run(["wget", "-P", download_dir, link], shell=True)
    archive_path = os.path.join(download_dir, fname)
    if not os.path.exists(archive_path):
        print(f"Downloaded {fname} successfully")
        return archive_path
    else:
        print(f"Expected archive {fname} to exist but can't find it")
        return None

def extract_archive(extract_dir, archive_path):
    print(f"Unzipping {archive_path}")
    result = subprocess.run(["unzip", "-d", extract_dir, archive_path], shell=True)

def walk_dataset(dataset_path, result_path):
    for (dirpath, dirnames, filenames) in os.walk(dataset_path):
        outdirpath = dirpath.replace(dataset_path, result_path)
        os.makedirs(outdirpath)
        for file in filenames:
            infilepath = os.path.join(dirpath, file)
            outfilepath = os.path.join(outdirpath, file.replace(".jpg", ".png"))
            dataset_relpath = infilepath.replace(dataset_path, "")
            yield (infilepath, outfilepath, dataset_relpath)

def run_nlm(dataset_path):
    global ENG
    for (infilepath, outfilepath, dataset_relpath) in walk_dataset(dataset_path):
        ENG.nlm(infilepath, outfilepath, nargout=0)

def eval_dataset(dataset_path, result_file_path):
    global ENG
    for (infilepath, outfilepath, dataset_relpath) in walk_dataset(dataset_path):

        csv = ENG.csv(infilepath, nargout=1)
        ms_unique = ENG.ms_unique(infilepath, nargout=1)
        summer = ENG.summer(infilepath, nargout=1)
        unique = ENG.unique(infilepath, nargout=1)
        rekognition_accuracy = rekognition(infilepath)

        image_id = datase_relpath.replace("/", "-")
        image_id = datase_relpath.replace("\\", "-")
        entry = f"{image_id} {csv} {summer} {unique} {ms_unique} {rekognition_accuracy}"
        with open(result_file_path, "w+") as f:
            f.write(entry + "\r\n")

if __name__ == "__main__":
    ENG = engine.start_matlab()

    os.path.makedirs(RESULTS_DIR)
    os.path.makedirs(DOWNLOAD_DIR)
    os.path.makedirs(EXTRACT_DIR)

    with open(DOWNLOAD_LINKS, "r") as f:
        links = f.readlines()

    for link in links:
        archive_path = download_archive(DOWNLOAD_DIR, link)
        if archive_path is None:
            continue
        extract_archive(EXTRACT_DIR, archive_path)
        nlm_sidd_results_dir = os.path.join(RESULTS_DIR, "nlm_sidd/")
        nlm_sidd_results_file = os.path.join(RESULTS_DIR, "nlm_sidd_results.txt")
        run_nlm(EXTRACT_DIR, nlm_results_dir)
        eval_dataset(nlm_sidd_results_dir, nlm_sidd_results_file)

