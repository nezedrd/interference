import numpy as np
from matplotlib import pyplot as plt
from .math import Values as V

if __name__=='__main__':
    V.print_wavelength()
    V.print_inter_source_distance()
    V.print_screen_distance()
    # data = np.zeros((512,512),dtype=np.float)
    # for i in reversed(range(1,101)):
        # data[256-2*i:256+2*i,256-2*i:256+2*i] = (100.-i)/100.
    # plt.imshow(data, interpolation='nearest', cmap=plt.get_cmap('Greys'))
    # plt.show()
