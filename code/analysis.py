import numpy as np

def parse_results(result_filepath):
    with open(result_filepath, 'r') as f:
        results = f.readlines()
    iqa = [line.split(' ')[1:] for line in results]
    ids = [line.split(' ')[0] for line in results]
    return (ids, np.array(iqa, dtype=np.float32))

ids, iqa = parse_results("results/nlm_cureor/nlm_cureor_results.txt")
means = np.mean(iqa, axis=0)
print(f"means for nlm cureor {means}")

ids, iqa = parse_results("results/nlm_cureor_lab/nlm_lab_cureor_results.txt")
means = np.mean(iqa, axis=0)
print(f"means for nlm lab cureor {means}")

ids, iqa = parse_results("results/nlm_cureor_block/nlm_cureor_block_results.txt")
means = np.mean(iqa, axis=0)
print(f"means for nlm block cureor {means}")

ids, iqa = parse_results("results/nlm_sidd/results.txt")
means = np.mean(iqa, axis=0)
print(f"means for nlm sidd {means}")

ids, iqa = parse_results("results/nlm_sidd_lab/nlm_lab_sidd_results.txt")
means = np.mean(iqa, axis=0)
print(f"means for nlm lab sidd {means}")
