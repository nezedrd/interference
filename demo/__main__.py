import numpy as np
from matplotlib import pyplot as plt
from .math import Values as V

if __name__=='__main__':
    xr = np.arange(-100000,100000,100)
    D = V.get_screen_distance()
    y = D
    data = np.ones((300,1))*V.get_intensity_1d(xr,y).reshape(1,-1)
    plt.imshow(data, interpolation='nearest', cmap=plt.get_cmap('Greys'))
    plt.show()
