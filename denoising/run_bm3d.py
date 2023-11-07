from matplotlib import pyplot as plt
import scipy
from matlab import engine

eng = engine.start_matlab()
eng.bm3d("../images/cure-or-guassian-blur/01950.jpg", "data/01950_bm3d.mat", nargout=0)

data = scipy.io.matlab.loadmat("data/01950_bm3d.mat")
im_nl = data["im_bm3d"]

plt.imshow(im_nl, cmap="Greys")
plt.show()
