import numpy as np
from matplotlib import pyplot as plt
from .data import DataGenerator as DG
from .math import Values as V

if __name__=='__main__':
    fig,ax = plt.subplots()
    ax.set_axis_off()
    V.set_wavelength(670)
    DG.plot_space_ld(ax)
    DG.plot_screen(ax)
    ax.set_ybound(lower=0)
    plt.show()
