import numpy as np
import os
from matplotlib import pyplot as plt

def parse_results(result_filepath):
    with open(result_filepath, 'r') as f:
        results = f.readlines()
    iqa = [line.split(' ')[1:] for line in results]
    ids = [line.split(' ')[0] for line in results]
    return (ids, np.array(iqa, dtype=np.float32))

def adaptive_nlm_results():
    result_files = [
        "results/curetsr_block_smoothless_real_train_full/nlm_curetsr_block_smoothless_real_train_full_results.txt",
        "results/nlm_cureor_block_smoothless_full/nlm_cureor_block_smoothless_full_results.txt",
        "results/nlm_set12_block_smoothless_full/nlm_set12_block_smoothless_full_results.txt",
        "results/nlm_siddsmall_block_smoothless_full/nlm_siddsmall_block_smoothless_full_results.txt",
    ]
    iqas = []
    filenames = []
    imageids_lists = []
    for result_file in result_files:
        ids, iqa = parse_results(result_file)
        iqas.append(iqa)
        filenames.append(os.path.basename(result_file))
        imageids_lists.append(ids)
    return filenames, imageids_lists, iqas

def nlm_results():
    result_files = [
        "results/curetsr_real_train_full/nlm_curetsr_real_train_full_results.txt",
        "results/nlm_cureor/nlm_cureor_results.txt",
        "results/nlm_set12_full/nlm_set12_full_results.txt",
        "results/nlm_sidd/results.txt",
    ]
    iqas = []
    filenames = []
    for result_file in result_files:
        if len(result_file):
            ids, iqa = parse_results(result_file)
            if iqa.shape[1] != 3:
                iqa = iqa[:, [0, 1, 6]]
            iqas.append(iqa)
            filenames.append(os.path.basename(result_file))
        else:
            iqas.append(np.array([[0]*7]))
            filenames.append("")
    return filenames, iqas

def blsgsm_results():
    result_files = [
        "../denoising/BLGSM_Output_nparray/IQA_CURE_TSR_BLSGSM.npy",
        "../denoising/BLGSM_Output_nparray/IQA_CUREOR_BLSGSM.npy",
        "../denoising/BLGSM_Output_nparray/IQA_Set12_BLSGSM.npy",
        "../denoising/BLGSM_Output_nparray/IQA_SIDD_BLSGSM.npy",
    ]
    iqas = []
    filenames = []
    for result_file in result_files:
        iqa = np.load(result_file)
        iqas.append(iqa)
    return filenames, iqas


datasets = ["CURE-TSR", "CURE-OR", "SET12", "SIDD"]
# colors = ['red', 'green']
colors = ['blue', 'orange', 'green']
def plot_aggregate(algorithm_labels, algorithm_iqas, iqa_fast=False, psnr_only=False):
    bar_positions = np.arange(len(datasets))
    bar_width = 0.75 / len(algorithm_labels)
    for i, (label, iqas) in enumerate(zip(algorithm_labels, algorithm_iqas)):

        # Only IQA Fast
        if iqa_fast and label != "NLM":
            iqas = [iqa[:, [0, 1, 6]] for iqa in iqas]

        if psnr_only:
            iqas = [iqa[:, [0]] for iqa in iqas]

        aggregate_iqa = np.concatenate(iqas, axis=0)
        max_iqa_vals = np.max(aggregate_iqa, axis=0)
        min_iqa_vals = np.min(aggregate_iqa, axis=0)
        normalized_iqas = [np.divide((iqa - min_iqa_vals), (max_iqa_vals - min_iqa_vals)) for iqa in iqas]
        norm_mean_iqas = []
        for dataset, iqa in zip(datasets, normalized_iqas):
            mean_iqa = np.mean(iqa, axis=0)
            norm_mean_iqa = np.linalg.norm(mean_iqa)
            # norm_mean_iqa = np.mean(mean_iqa)
            norm_mean_iqas.append(norm_mean_iqa)
        plt.bar(bar_positions + i * bar_width, norm_mean_iqas, width=bar_width, label=label, color=colors[i])
    plt.xticks(bar_positions, datasets)
    plt.legend()
    plt.show()


additive_noise_strings = {
    "CURE-TSR": "DirtyLens",
    "CURE-OR": "dirtylens",
    "SET12": "additive",
    "SIDD": "sidd",
}
def nlm_additive_correlation(ids_lists, iqas_mats):
    additive_noise = []
    other_noise = []
    for i in range(len(datasets)):
        image_ids = ids_lists[i]
        iqas_mat = iqas_mats[i]
        dataset_label = datasets[i]
        keyword = additive_noise_strings[dataset_label]
        av_additive_iqa = np.zeros((7,))
        av_other_iqa = np.zeros((7,))
        additive_count = 0
        other_count = 0
        print(f"IQA analysis for {dataset_label}")
        for j, image_id in enumerate(image_ids):
            if keyword in image_id:
                av_additive_iqa += iqas_mat[j]
                additive_count += 1
            else:
                av_other_iqa += iqas_mat[j]
                other_count += 1
        av_additive_iqa /= additive_count
        av_other_iqa /= other_count
        print(f"Average iqa for additive noise {' '.join([str(round(val, 3)) for val in av_additive_iqa])}")
        print(f"Average iqa for other noise {' '.join([str(round(val, 3)) for val in av_other_iqa])}")
        additive_noise.append(av_additive_iqa)
        other_noise.append(av_other_iqa)
    additive_noise = np.mean(np.array(additive_noise), axis=0)
    other_noise = np.mean(np.array(other_noise), axis=0)
    print(f"Average iqa for additive noise in all datasets {' '.join([str(round(val, 3)) for val in additive_noise])}")
    print(f"Average iqa for other noise in all datasets {' '.join([str(round(val, 3)) for val in other_noise])}")


_, adaptive_nlm_ids, adaptive_nlm_iqas = adaptive_nlm_results()
_, nlm_iqas = nlm_results()
_, blsgsm_iqas = blsgsm_results()
# # algorithms = ["NLM", "Adaptive NLM"]
# # algorithms = ["Adaptive NLM", "BLSGSM"]
# algorithms = ["NLM", "Adaptive NLM", "BLSGSM"]
# # algorithms_iqas = [nlm_iqas, adaptive_nlm_iqas]
# # algorithms_iqas = [adaptive_nlm_iqas, blsgsm_iqas]
# algorithms_iqas = [nlm_iqas, adaptive_nlm_iqas, blsgsm_iqas]
# # plot_aggregate(algorithms, algorithms_iqas, iqa_fast=True)
# # plot_aggregate(algorithms, algorithms_iqas)
# plot_aggregate(algorithms, algorithms_iqas, psnr_only=True)

nlm_additive_correlation(adaptive_nlm_ids, adaptive_nlm_iqas)

# for result_file in result_files:
#     ids, iqa = parse_results(result_file)
#     print(f"Averages for {os.path.basename(result_file)}:")
#     print(np.mean(iqa, axis=0))

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










# result_files = [
# "results/curetsr_block/nlm_curetsr_block_results.txt",
# "results/curetsr_block_smoothless/nlm_curetsr_block_smoothless_results.txt",
# "results/curetsr_block_smoothless_real_train_full/nlm_curetsr_block_smoothless_real_train_full_results.txt",
# "results/curetsr_block_smoothless_real_train/nlm_curetsr_block_smoothless_real_train_results.txt",
# "results/nlm_cureor_block/nlm_cureor_block_results.txt",
# "results/nlm_cureor_block_smoothless/nlm_cureor_block_smoothless_results.txt",
# # "results/nlm_cureor_block_smoothless/rekognition_results.txt",
# "results/nlm_cureor_lab/nlm_lab_cureor_results.txt",
# "results/nlm_cureor/nlm_cureor_results.txt",
# "results/nlm_set12_block_smoothless_full/nlm_set12_block_smoothless_full_results.txt",
# "results/nlm_set12_block_smoothless/nlm_set12_block_smoothless_results.txt",
# "results/nlm_sidd_block/nlm_sidd_block_results.txt",
# "results/nlm_sidd_lab/nlm_lab_sidd_results.txt",
# "results/nlm_sidd/results.txt",
# "results/nlm_siddsmall_block_smoothless_full/nlm_siddsmall_block_smoothless_full_results.txt",
# "results/nlm_siddsmall_block_smoothless/nlm_siddsmall_block_smoothless_results.txt",
# ]
# 
