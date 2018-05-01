import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as mcol
from .math import Values as V

class DataGenerator:
    __screen_x_px = 1024
    __screen_y_px = 256

    __screen_left = - 10e4
    __screen_right= + 10e4

    __screen_x = __screen_right - __screen_left
    __screen_y = (__screen_y_px*__screen_x)/__screen_x_px

    __spectre = plt.get_cmap('nipy_spectral')
    __cmap = None

    @classmethod
    def get_cmap(cls):
        if cls.__cmap is None:
            l = (V.get_wavelength()-400.)/300.
            res = 2
            ref_color = [cls.__spectre(l)]*res
            smooth = np.linspace(0.,1.,res)
            smooth = np.array([smooth,smooth,smooth,np.ones(res,dtype=float)]).transpose()
            colors = ref_color*smooth
            cls.__cmap = mcol.LinearSegmentedColormap.from_list('colormap',colors)
        return cls.__cmap

    @classmethod
    def reset_cmap(cls):
        cls.__cmap = None

    @classmethod
    def get_screen(cls,**kwargs):
        extent = kwargs['extent']
        cols   = kwargs['cols']
        rows   = kwargs['rows']
        xr = np.linspace(extent[0], extent[1], num = cols)
        y = extent[2]
        data = np.ones((rows,1))*V.get_intensity_1d(xr,y).reshape(1,-1)
        return data

    """
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
    """

    @classmethod
    def get_space(cls,**kwargs):
        extent = kwargs['extent']
        cols   = kwargs['cols']
        rows   = kwargs['rows']
        xr = np.linspace(extent[0], extent[1], num = cols)
        yr = np.linspace(extent[2], extent[3], num = rows)
        data = np.transpose(V.get_intensity_2d(xr,yr))
        return data

    """
    @classmethod
    def plot_space(cls,ax,x_px,y_px):
        xr = np.linspace(cls.__screen_left,
                cls.__screen_right,
                num=x_px,
                endpoint=True,
                dtype=np.float)
        y = V.get_screen_distance()*.9
        yr = np.linspace(0,
                y,
                num=y_px,
                endpoint=True,
                dtype=np.float)
        data = np.transpose(V.get_intensity_2d(xr,yr))
        return ax.imshow(data, interpolation='nearest', cmap=cls.get_cmap(),
                extent=(cls.__screen_left,cls.__screen_right,0,y),
                origin='lower')

    @classmethod
    def plot_space_hd(cls,ax=plt):
        x_px = cls.__screen_x_px
        y = V.get_screen_distance()*.9
        y_px = y*x_px/cls.__screen_y
        return cls.plot_space(ax,x_px,y_px)

    @classmethod
    def plot_space_ld(cls,ax=plt):
        x_px = cls.__screen_x_px >> 3
        y = V.get_screen_distance()*.9
        y_px = y*x_px/cls.__screen_y
        return cls.plot_space(ax,x_px,y_px)
    """

if __name__=='__main__':
    print(DataGenerator.get_cmap())
