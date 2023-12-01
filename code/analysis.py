import numpy as np
import os

def parse_results(result_filepath):
    with open(result_filepath, 'r') as f:
        results = f.readlines()
    iqa = [line.split(' ')[1:] for line in results]
    ids = [line.split(' ')[0] for line in results]
    return (ids, np.array(iqa, dtype=np.float32))

result_files = [
"results/curetsr_block/nlm_curetsr_block_results.txt",
"results/curetsr_block_smoothless/nlm_curetsr_block_smoothless_results.txt",
"results/curetsr_block_smoothless_real_train_full/nlm_curetsr_block_smoothless_real_train_full_results.txt",
"results/curetsr_block_smoothless_real_train/nlm_curetsr_block_smoothless_real_train_results.txt",
"results/nlm_cureor_block/nlm_cureor_block_results.txt",
"results/nlm_cureor_block_smoothless/nlm_cureor_block_smoothless_results.txt",
# "results/nlm_cureor_block_smoothless/rekognition_results.txt",
"results/nlm_cureor_lab/nlm_lab_cureor_results.txt",
"results/nlm_cureor/nlm_cureor_results.txt",
"results/nlm_set12_block_smoothless_full/nlm_set12_block_smoothless_full_results.txt",
"results/nlm_set12_block_smoothless/nlm_set12_block_smoothless_results.txt",
"results/nlm_sidd_block/nlm_sidd_block_results.txt",
"results/nlm_sidd_lab/nlm_lab_sidd_results.txt",
"results/nlm_sidd/results.txt",
"results/nlm_siddsmall_block_smoothless_full/nlm_siddsmall_block_smoothless_full_results.txt",
"results/nlm_siddsmall_block_smoothless/nlm_siddsmall_block_smoothless_results.txt",
]

for result_file in result_files:
    ids, iqa = parse_results(result_file)
    print(f"Averages for {os.path.basename(result_file)}:")
    print(np.mean(iqa, axis=0))

# ids, iqa = parse_results("results/nlm_cureor/nlm_cureor_results.txt")
# means = np.mean(iqa, axis=0)
# print(f"means for nlm cureor {means}")
# 
# ids, iqa = parse_results("results/nlm_cureor/nlm_cureor_results.txt")
# means = np.mean(iqa, axis=0)
# print(f"means for nlm cureor {means}")
# 
# ids, iqa = parse_results("results/nlm_cureor_lab/nlm_lab_cureor_results.txt")
# means = np.mean(iqa, axis=0)
# print(f"means for nlm lab cureor {means}")
# 
# ids, iqa = parse_results("results/nlm_cureor_block/nlm_cureor_block_results.txt")
# means = np.mean(iqa, axis=0)
# print(f"means for nlm block cureor {means}")
# 
# ids, iqa = parse_results("results/nlm_sidd/results.txt")
# means = np.mean(iqa, axis=0)
# print(f"means for nlm sidd {means}")
# 
# ids, iqa = parse_results("results/nlm_sidd_lab/nlm_lab_sidd_results.txt")
# means = np.mean(iqa, axis=0)
# print(f"means for nlm lab sidd {means}")
