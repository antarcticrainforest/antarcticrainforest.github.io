import karabo_data as kd
import warnings

from IPython.display import HTML
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
plt.rcParams['figure.figsize'] = (20.0, 10.0)
matplotlib.rc('image', cmap='RdYlBu_r')

warnings.filterwarnings("ignore")
#%matplotlib inline
import karabo_data as kd
run_folder = '/gpfs/exfel/exp/XMPL/201750/p700000/raw/r0273'
exmpl_file = '/gpfs/exfel/exp/XMPL/201750/p700000/proc/r0273/CORR-R0273-AGIPD03-S00000.h5'
hdf5_file = kd.H5File(exmpl_file)
run_dir = kd.RunDirectory(run_folder)
