from pipeline import *
import pipeline
import os

pipeline.DATASET='SET12'
pipeline.EXTRACT_DIR='../datasets/set12/'
pipeline.RESULTS_DIR='./results/nlm_set12_block_smoothless/'
pipeline.RESULTS_FILE=os.path.join(pipeline.RESULTS_DIR, 'nlm_set12_block_smoothless_results.txt')
pipeline.GT_PATH='../datasets/set12/GT/'
pipeline.LOG_FILE='./log_nlm_set12_block_smoothless.txt'
pipeline.CLEAN_FILES=False
pipeline.NUM_IMAGE_SAMPLES=None

ARCHIVE_NAMES=['additive0-01', 'additive0-03', 'additive0-05', 'additive0-10', 'blur0-50', 'blur1-00', 'blur1-50', 'blur10-0']

os.makedirs(pipeline.RESULTS_DIR, exist_ok=True)

for archive_name in ARCHIVE_NAMES:
    run_nlm(
        os.path.join(pipeline.EXTRACT_DIR, archive_name),
        os.path.join(pipeline.RESULTS_DIR, archive_name),
    )
    eval_dataset(
        os.path.join(pipeline.RESULTS_DIR, archive_name),
        pipeline.RESULTS_FILE,
    )
    process_results(
        pipeline.RESULTS_FILE,
        archive_name,
    )
    clean_result_files(
        os.path.join(pipeline.RESULTS_DIR, archive_name),
    )
