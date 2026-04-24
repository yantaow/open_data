import os
import sys
import numpy as np
import shutil
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import sys

import setup_plot
fontsize = 20
setup_plot.setup(fontsize)
import seaborn as sns
sns.set_palette('colorblind')
from matplotlib.ticker import ScalarFormatter

argv    = sys.argv
model   = argv.pop(1)
folder  = argv.pop(1)

np.set_printoptions(precision=5, linewidth=1e6, suppress=False)

if model == 'Hubbard':
    E_exact =  -6.8084144664
    L       = 4
else:
    raise ValueError
#---------------------------------------------------------------
def parse(string, splitter='_'):
    import re
    parts = string.split(splitter)
    param = {}
    for p in parts:
        #m = re.fullmatch(r'([A-Za-z]+)(.*)', p)
        m = re.fullmatch(r'([^0-9]+)([0-9].*)', p)
        if m:
            key, val = m.groups()
            param[key] = val
    return param
#---------------------------------------------------------------
def moving_avg(A, window=100):
    A = np.asarray(A)
    # Compute growing average for the first (window - 1) elements
    pad = np.cumsum(A[:window - 1], dtype=float) / np.arange(1, window)
    # Compute full window moving average for the rest
    avg = np.convolve(A, np.ones(window) / window, mode='valid')
    return np.concatenate((pad, avg))
#---------------------------------------------------------------
if __name__ == '__main__':
    fs  = [f for f in os.listdir(folder) if 'log' in f and 'x' in f]
    print('fs:', fs)

    plt.figure(figsize=(10, 8))
    for file in fs:
        #----- get data -----
        stp = 10
        dat = np.loadtxt(folder + '/' + file + '/avg.out')
        dat = dat[:10000, :]
        x   = dat[::stp, 0]     #GD step
        y   = moving_avg(dat[:,2])[::stp]
        y   = (y-E_exact)/L**2

        param = parse(file)
        D   = param['chi']
        Nb  = int(param['Nb']) * int(param['Ns'])
        #----- plot data -----
        plt.title(r'{}$\times${} {} ($U$={}, half-filled, open boundary)'.format(L, L, model, 8))
        plt.ylabel('energy density error',)
        plt.xlabel('vmc step',)
        plt.plot(x, y, label=r'D{}_Nb{}'.format(D, Nb))

    ax = plt.gca()
    def clean_sci_notation(x, _):
        if x == 0:
            return "0"
        return f"{x:.0e}".replace("e-0", "e-").replace("e+0", "e+")

    #from matplotlib.ticker import LogFormatter
    from matplotlib.ticker import FormatStrFormatter
    from matplotlib.ticker import FuncFormatter
    ax.set_yscale('log')
    ax.set_ylim([1e-6, 10])
    #ax.set_yticks([1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1])
    ax.yaxis.set_major_formatter(FuncFormatter(clean_sci_notation))
    ax.set_xticks([0, 2000, 4000, 6000, 8000, 10000])

    #---plot labels----
    handles, labels = plt.gca().get_legend_handles_labels()
    def get_D(label):
        print('label:', label)
        param = parse(label)
        print('param:', param)
        D   = param['D']
        Nb  = param['Nb']
        #return int(label.split('=')[1])
        return int(D), int(Nb)
    pairs = sorted(zip(handles, labels), key=lambda x: get_D(x[1]))
    handles_sorted, labels_sorted = zip(*pairs)
    plt.legend(handles_sorted, labels_sorted)

    plt.tight_layout()
    plt.savefig('energy_{}.pdf'.format(model), format='pdf')
    plt.show()

