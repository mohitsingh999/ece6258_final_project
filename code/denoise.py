from pipeline import *
import pipeline
import os

pipeline.DATASET='SIDD-SMALL'
pipeline.EXTRACT_DIR='./cache_siddsmall/extracted/'
pipeline.RESULTS_DIR='./results/nlm_siddsmall_block/'
pipeline.RESULTS_FILE=os.path.join(pipeline.RESULTS_DIR, 'nlm_block_siddsmall_results.txt')
pipeline.LOG_FILE='./log.txt'
pipeline.CLEAN_FILES=False
pipeline.NUM_IMAGE_SAMPLES=1

# ARCHIVE_URL=''
ARCHIVE_NAME='sidd_small'
# ARCHIVE_EXTENSION='.tar.gz'

os.makedirs(pipeline.RESULTS_DIR, exist_ok=True)
os.makedirs(pipeline.DOWNLOAD_DIR, exist_ok=True)
os.makedirs(pipeline.EXTRACT_DIR, exist_ok=True)

# download_archive(
#     pipeline.DOWNLOAD_DIR,
#     ARCHIVE_URL,
# )
# extract_archive(
#     os.path.join(pipeline.DOWNLOAD_DIR, ARCHIVE_NAME) + ARCHIVE_EXTENSION,
#     pipeline.EXTRACT_DIR,
#     os.path.join(pipeline.EXTRACT_DIR, pipeline.ARCHIVE_NAME),
# )
run_nlm(
    os.path.join(pipeline.EXTRACT_DIR, ARCHIVE_NAME),
    os.path.join(pipeline.RESULTS_DIR, ARCHIVE_NAME),
)
eval_dataset(
    os.path.join(pipeline.RESULTS_DIR, ARCHIVE_NAME),
    pipeline.RESULTS_FILE,
)
process_results(
    pipeline.RESULTS_FILE,
    ARCHIVE_NAME,
)
clean_result_files(
    os.path.join(pipeline.RESULTS_DIR, ARCHIVE_NAME),
)


