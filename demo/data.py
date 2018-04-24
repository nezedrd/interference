import numpy as np
from matplotlib import pyplot as plt
from .math import Values as V

class DataGenerator:
    __screen_x_px = 1024
    __screen_y_px = 256

    __screen_left = - 10e4
    __screen_right= + 10e4

    __screen_x = __screen_right - __screen_left
    __screen_y = (__screen_y_px*__screen_x)/__screen_x_px

    @classmethod
    def get_cmap(cls):
        return plt.get_cmap('Greys')

    @classmethod
    def plot_screen(cls,ax=plt):
        xr = np.linspace(cls.__screen_left,
                cls.__screen_right,
                num=cls.__screen_x_px,
                endpoint=True,
                dtype=np.float)
        y = V.get_screen_distance()
        data = np.ones((cls.__screen_y_px,1))*V.get_intensity_1d(xr,y).reshape(1,-1)
        return ax.imshow(data, interpolation='nearest', cmap=cls.get_cmap(),
                extent=(cls.__screen_left,cls.__screen_right,y,y+cls.__screen_y),
                origin='lower')

    @classmethod
    def plot_space(cls,ax=plt):
        xr = np.linspace(cls.__screen_left,
                cls.__screen_right,
                num=cls.__screen_x_px,
                endpoint=True,
                dtype=np.float)
        y = V.get_screen_distance()
        y_px = y*cls.__screen_x_px/cls.__screen_y
        yr = np.linspace(0,
                y,
                num=y_px,
                endpoint=True,
                dtype=np.float)
        data = np.transpose(V.get_intensity_2d(xr,yr))
        return ax.imshow(data, interpolation='nearest', cmap=cls.get_cmap(),
                extent=(cls.__screen_left,cls.__screen_right,0,y),
                origin='lower')
