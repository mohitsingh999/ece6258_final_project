from pipeline import *
import pipeline
import os

pipeline.DATASET='CURE-OR'
pipeline.EXTRACT_DIR='./cache/extracted/'
pipeline.DOWNLOAD_DIR='./cache/download/'
pipeline.RESULTS_DIR='./results/nlm_cureor_block_smoothless/'
pipeline.RESULTS_FILE=os.path.join(pipeline.RESULTS_DIR, 'nlm_cureor_block_smoothless_results.txt')
pipeline.LOG_FILE='./log_nlm_cureor_block_smoothless.txt'
pipeline.CLEAN_FILES=True
pipeline.NUM_IMAGE_SAMPLES=80

# ARCHIVE_URL=''
URLS=[
'https://ieee-dataport.s3.amazonaws.com/open/708/06_contrast.tar.gz?response-content-disposition=attachment%3B%20filename%3D%2206_contrast.tar.gz%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJOHYI4KJCE6Q7MIQ%2F20231130%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231130T160916Z&X-Amz-SignedHeaders=Host&X-Amz-Expires=86400&X-Amz-Signature=320c662250a5c62c2910253ad4cd9cc27c7e896e0b2fd487c81829536858800c',
'https://ieee-dataport.s3.amazonaws.com/open/708/07_dirtylens1.tar.gz?response-content-disposition=attachment%3B%20filename%3D%2207_dirtylens1.tar.gz%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJOHYI4KJCE6Q7MIQ%2F20231130%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231130T160916Z&X-Amz-SignedHeaders=Host&X-Amz-Expires=86400&X-Amz-Signature=93cb77ecac52eb2d03f4b5a2c9e6384b4fa5328bbd1610dc7db123b8738bea51',
'https://ieee-dataport.s3.amazonaws.com/open/708/08_dirtylens2.tar.gz?response-content-disposition=attachment%3B%20filename%3D%2208_dirtylens2.tar.gz%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJOHYI4KJCE6Q7MIQ%2F20231130%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231130T160916Z&X-Amz-SignedHeaders=Host&X-Amz-Expires=86400&X-Amz-Signature=241fc81272372ad41bc88eee951e61456dd2d4b1e27ea3ea1e4d98d302ab38d3',
]
ARCHIVE_NAMES=['06_contrast', '07_dirtylens1', '08_dirtylens2']
ARCHIVE_EXTENSION='.tar.gz'

os.makedirs(pipeline.RESULTS_DIR, exist_ok=True)
os.makedirs(pipeline.DOWNLOAD_DIR, exist_ok=True)
os.makedirs(pipeline.EXTRACT_DIR, exist_ok=True)


for url, archive_name in zip(URLS, ARCHIVE_NAMES):
    download_archive(
        pipeline.DOWNLOAD_DIR,
        url,
    )
    extract_archive(
        os.path.join(pipeline.DOWNLOAD_DIR, archive_name) + ARCHIVE_EXTENSION,
        pipeline.EXTRACT_DIR,
        os.path.join(pipeline.EXTRACT_DIR, archive_name),
    )
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


