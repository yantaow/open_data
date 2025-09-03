import os
import sys
#----use only one core----
nc = "1"
os.environ["OMP_NUM_THREADS"] = nc
os.environ["OPENBLAS_NUM_THREADS"] = nc
os.environ["MKL_NUM_THREADS"] = nc
os.environ["VECLIB_MAXIMUM_THREADS"] = nc
os.environ["NUMEXPR_NUM_THREADS"] = nc

import numpy as np
import shutil
import parse
import matplotlib as mpl
mpl.rcParams["savefig.directory"] = ''
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
model=''
np.set_printoptions(precision=5, linewidth=1e6, suppress=False)
#---------------------------------------------------------------
if __name__ == '__main__':
    data_small_m    = np.loadtxt('../avg_w1.0_J1.0_m-0.2_L40_chi500_dt0.01.out')
    data_large_m    = np.loadtxt('../avg_w1.0_J1.0_m-2.0_L40_chi500_dt0.01.out')
    ts              = data_small_m[:,0]
    col             = 2
    small_pars      = data_small_m[:, col]
    large_pars      = data_large_m[:, col]


    plt.figure()
    plt.title('Spontaneous creation of matter-antimatter pair'.format(model))
    plt.ylabel('particle density (matter + antimatter)', fontsize=14)
    plt.xlabel('evolution time', fontsize=14)
    plt.plot(ts, small_pars, linewidth=1, label='m=0.2')
    plt.plot(ts, large_pars, linewidth=1, label='m=2.0')
    ax = plt.gca()
    # Create a custom formatter for x-axis ticks
    formatter = ScalarFormatter()
    formatter.set_scientific(False)  # Disable scientific notation
    plt.legend(fontsize=13, frameon=False, loc='best')



    plt.tight_layout()
    plt.savefig('Schwinger_Mechanism.pdf'.format(model), format='pdf')
    plt.show()

