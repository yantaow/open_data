import os
import sys
#--------
#It's important to define nc before importing numpy

import random
import numpy as np
import scipy as sp
import time
import copy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import setup_plot
fontsize = 18
setup_plot.setup(fontsize)
import seaborn as sns
sns.set_palette('colorblind')
from matplotlib.ticker import ScalarFormatter
plt.rcParams['font.family'] = 'Helvetica'


argv    = sys.argv
N       = int(argv.pop(1))
Lx      = int(argv.pop(1))
Ly      = int(argv.pop(1))
h       = float(argv.pop(1))
g       = float(argv.pop(1))
dt      = float(argv.pop(1))
name    = argv.pop(1)

np.set_printoptions(precision=15, linewidth=100000000)
#-------------------------------------------------------------------------------
def plot_Bp(Bp_avg, title=None, T=None, ax=None, i=0):
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes

    Lx, Ly = Bp_avg.shape[0] + 1, Bp_avg.shape[1] + 1

    x_edges = np.arange(Lx - 1) + 0.5
    y_edges = np.arange(Ly - 1) + 0.5
    X, Y = np.meshgrid(x_edges, y_edges, indexing='ij')

    if ax is None:
        fig, ax = plt.subplots(figsize=(4, 4))
    else:
        fig = ax.figure

    im = ax.pcolormesh(X, Y, Bp_avg, shading='auto', cmap='magma', vmin=-1, vmax=1)
    ax.set_aspect('equal')

    if i == 0:
        # Inset colorbar
        cax = inset_axes(ax,
                     width="6%", height="60%",  # ← wider bar
                     loc='right',
                     bbox_to_anchor=(0.34, 0, 0.5, 1),  # ← fine-tune position
                     bbox_transform=ax.transAxes,
                     borderpad=0)
        fig.colorbar(im, cax=cax)

    # Internal time label
    if T is not None:
        ax.text(0.36, 0.85, 'T={:.2f}'.format(T), transform=ax.transAxes, fontsize=fontsize,
                verticalalignment='bottom', bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.7))


    if i in [2, 3]:
        ax.set_xlabel('x')
        ax.set_xticks(np.arange(Lx))
    else:
        ax.set_xlabel('')
        ax.set_xticks(np.arange(Lx))
        ax.set_xticklabels([])  # hides tick labels


    if i in [0, 2]:
        ax.set_ylabel('y')
        ax.set_yticks(np.arange(Ly))
    else:
        ax.set_ylabel('')
        ax.set_yticks(np.arange(Ly))
        ax.set_yticklabels([])  # hides tick labels

    ax.grid(True, alpha=0.4)

    return im  # optional return
#------------------------------------------------------------------------------
if __name__ == '__main__':
    '''
    Z2 gauge theory
    '''
    print('name :', name)
    import matplotlib.pyplot as plt
    import numpy as np

    #fig, axs = plt.subplots(2, 2, figsize=(5.5, 6))
    fig, axs = plt.subplots(2, 2, figsize=(5.5, 6), constrained_layout=True)
    ks = [0, 1200, 2400, 3600]
    ims = []
    for i, k in enumerate(ks):
        Bp_avg = np.loadtxt(f'data/{name}_k{k}.dat')
        im = plot_Bp(Bp_avg, T=k * dt, ax=axs.flat[i], i=i)
        ims.append(im)

    fig.suptitle(rf'(b) {Lx}×{Ly} Z$_2$ gauge theory, $g={g}$', fontsize=fontsize)#, y=0.97)
    fig.set_constrained_layout(True)
    fig.savefig('vison_10x10.pdf', bbox_inches=None)
    matplotlib.rcParams['savefig.directory'] = os.getcwd()
    plt.show()
    plt.close()

