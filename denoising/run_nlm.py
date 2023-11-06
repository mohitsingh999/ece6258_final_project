from matplotlib import pyplot as plt
import scipy
from matlab import engine

eng = engine.start_matlab()
eng.nlm("../images/cure-or-guassian-blur/01950.jpg", "data/01950_nlm.mat", nargout=0)

data = scipy.io.matlab.loadmat("data/01950_nlm.mat")
im_nl = data["im_nl"]

plt.imshow(im_nl, cmap="Greys")
plt.show()
