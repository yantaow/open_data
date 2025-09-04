import os
import sys
import numpy as np
import shutil
import parse
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import sys

import setup_plot
fontsize = 18
setup_plot.setup(fontsize)
import seaborn as sns
sns.set_palette('colorblind')
from matplotlib.ticker import ScalarFormatter
plt.rcParams['font.family'] = 'Helvetica'

argv    = sys.argv
O       = int(argv.pop(1))   #which column
Lx      = int(argv.pop(1))
Ly      = int(argv.pop(1))
h       = float(argv.pop(1))
g       = float(argv.pop(1))
dt      = float(argv.pop(1))
name    = argv.pop(1)

np.set_printoptions(precision=5, linewidth=1e6, suppress=False)
#---------------------------------------------------------------
if __name__ == '__main__':
    files   = [f for f in os.listdir('.') if ('vison_' in f and '.out' in f)]
    print('files:', files)

    labels  = []
    for f in files:
        if 'exact.out' in f:
            labels.append('exact')
        elif 'chi3' in f:
            labels.append('GI-PEPS D=6')
        elif 'chi2' in f:
            labels.append('GI-PEPS D=4')
        else:
            raise ValueError

    Os  = [3, 4, 15]
    fig, axs = plt.subplots(3, 1, figsize=(5.5, 2.0 * 3))
    print('fig size :', fig.get_size_inches())
    for idx, (ax, O) in enumerate(zip(axs, Os)):
        #-------------------- get data --------------------
        xs  = []
        ys  = []
        for f in files:
            print('f:', f)
            stp = 1
            dat = np.loadtxt(f)
            #dat = dat[:4000, :]
            print('dat:', dat.shape)
            x   = dat[::stp, 1]     #GD step
            y   = dat[::stp, O]     #running average of E
            xs.append(x)
            ys.append(y)
        i, j    = (O-3)//(Ly-1), (O-3)%(Ly-1)
        #-------------------- end of get data --------------
        plt.sca(ax)
        for x, y, label in zip(xs, ys, labels):
            plt.plot(x, y, '-', mfc='none', label=label)
        plt.ylabel(fr'$\langle P_{{{i},{j}}} \rangle/2$')
        ax.set_xlim([0,18])
        plt.xticks([0,3,6,9,12,15,18])
        if idx == 2:
            plt.xlabel('time',)

        if idx == 0:
            plt.legend(fontsize=fontsize-2, frameon=False)#, loc='center right')
        if O >= 3:
            i, j    = (O-3)//(Ly-1), (O-3)%(Ly-1)
            plt.ylabel(fr'$\langle P_{{{i},{j}}} \rangle/2$')
        else:
            plt.ylabel('total energy')

    fig.suptitle(rf'(a) {Lx}×{Ly} Z$_2$ gauge theory, $g={g}$', fontsize=fontsize, y=1)

    plt.tight_layout()
    plt.savefig('vison_{}x{}.pdf'.format(Lx, Ly), format='pdf')
    plt.show()

