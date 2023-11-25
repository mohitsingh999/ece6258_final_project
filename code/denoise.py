from pipeline import *
import os

ARCHIVE_URL='https://ieee-dataport.s3.amazonaws.com/open/708/08_dirtylens2.tar.gz?response-content-disposition=attachment%3B%20filename%3D%2208_dirtylens2.tar.gz%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJOHYI4KJCE6Q7MIQ%2F20231124%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231124T151725Z&X-Amz-SignedHeaders=Host&X-Amz-Expires=86400&X-Amz-Signature=b1b0e48672598f4f4f3c6228052c73263df418f9a6fb764ab50569456d02e811'
ARCHIVE_NAME='08_dirtylens2'
ARCHIVE_EXTENSION='.tar.gz'

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


