import scipy.io
import numpy as np

# Load in mat file
mat = scipy.io.loadmat('IQA_CUREOR10percent_BLSGSM.mat')
x = mat.items()

np_mat = np.zeros((38429, 7))

for i in range(0, np_mat.shape[0]):
    np_mat[i, 0] = mat['IQA_CUREOR_Images'][0][i][0][0][0][0][0] #psnr
    np_mat[i, 1] = mat['IQA_CUREOR_Images'][0][i][0][0][1][0][0] #ssim
    np_mat[i, 2] = mat['IQA_CUREOR_Images'][0][i][0][0][2][0][0] #cw-ssim
    np_mat[i, 3] = mat['IQA_CUREOR_Images'][0][i][0][0][3][0][0] #unique
    np_mat[i, 4] = mat['IQA_CUREOR_Images'][0][i][0][0][4][0][0] #ms-unique
    np_mat[i, 5] = mat['IQA_CUREOR_Images'][0][i][0][0][5][0][0] #csv
    np_mat[i, 6] = mat['IQA_CUREOR_Images'][0][i][0][0][6][0][0] #summer
    print(i)

np.save('IQA_CUREOR_BLSGSM.npy', np_mat)