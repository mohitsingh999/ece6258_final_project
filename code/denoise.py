from pipeline import *
import os

ARCHIVE_URL=''
ARCHIVE_NAME='08_dirtylens2'
ARCHIVE_EXTENSION='.tar.gz'

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACT_DIR, exist_ok=True)

download_archive(
    DOWNLOAD_DIR,
    ARCHIVE_URL,
)
extract_archive(
    os.path.join(DOWNLOAD_DIR, ARCHIVE_NAME) + ARCHIVE_EXTENSION,
    EXTRACT_DIR,
    os.path.join(EXTRACT_DIR, ARCHIVE_NAME),
)
run_nlm(
    os.path.join(EXTRACT_DIR, ARCHIVE_NAME),
    os.path.join(RESULTS_DIR, ARCHIVE_NAME),
)
eval_dataset(
    os.path.join(RESULTS_DIR, ARCHIVE_NAME),
    RESULTS_FILE,
)
process_results(
    RESULTS_FILE,
    ARCHIVE_NAME,
)
clean_result_files(
    os.path.join(RESULTS_DIR, ARCHIVE_NAME),
)


