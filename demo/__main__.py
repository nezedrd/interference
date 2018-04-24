import numpy as np
from matplotlib import pyplot as plt
from .data import DataGenerator as DG

if __name__=='__main__':
    fig,ax = plt.subplots()
    DG.plot_space(ax)
    DG.plot_screen(ax)
    ax.set_ybound(lower=0)
    plt.show()
