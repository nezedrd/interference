from matplotlib import pyplot as plt
from .data import DataGenerator as DG
from .math import Values as V

class Settings:
    """
    Canvas dimensions
    """
    __canvas_total_width = 9
    __canvas_total_height = 6

    @classmethod
    def get_canvas(cls):
        return cls.__canvas_total_height,cls.__canvas_total_width

    """
    Display parameters
    """
    __tick_params = {
            'labelbottom':   False,
            'labeltop':      False,
            'labelleft':     False,
            'labelright':    False,
            'bottom':        False,
            'top':           False,
            'left':          False,
            'right':         False,
            'direction':     'in',
            'length':        3,
        }

    __aspect = {
            'aspect': 'equal',
            # 'adjustable': 'datalim',
            'anchor': 'SW',
        }

    @classmethod
    def configure_axes(cls,*axs):
        for ax in axs:
            ax.tick_params(**cls.__tick_params)
            # ax.set_aspect(**cls.__aspect)

    @classmethod
    def get_imshow_parameters(cls):
        return { 'interpolation': 'nearest',
                'cmap': cls.get_cmap(),
                'origin': 'lower' }

    @classmethod
    def get_cmap(cls):
        return DG.get_cmap()

    """
    Data bounds and resolution parameters
    """
    __min_x = -  5e4 # -10 cm
    __max_x =    5e4 #  10 cm
    __min_y =      0 #   0 nm
    __max_y =   30e4 #  30 cm
    __hd_w = 1024
    __ld_w = 128

    @classmethod
    def get_space_parameters(cls):
        extent = (cls.__min_x,
                cls.__max_x,
                cls.__min_y,
                cls.__max_y - (cls.__max_y-cls.__min_y)*.05)
        cols = cls.__ld_w
        rows = int(cols*(extent[3]-extent[2])/(extent[1]-extent[0]))
        return { 'extent': extent, 'cols': cols, 'rows': rows }

    @classmethod
    def get_space(cls):
        param = cls.get_space_parameters()
        imparam = cls.get_imshow_parameters()
        imparam['extent'] = param['extent']
        return DG.get_space(**param),imparam

    @classmethod
    def get_zoombox_parameters(cls,**kwargs):
        ratio = kwargs.get('ratio',1)
        w = kwargs.get('resolution', cls.__hd_w)
        h = int(w/ratio)
        max_x = min(cls.__max_x,2*V.get_inter_source_distance())
        min_x = - max_x
        max_y = ratio * (max_x-min_x) / 2
        min_y = - max_y
        extent = (min_x, max_x, min_y, max_y)
        return { 'extent': extent, 'cols': h, 'rows': w }

    @classmethod
    def get_zoombox(cls,**kwargs):
        param = cls.get_zoombox_parameters(**kwargs)
        imparam = cls.get_imshow_parameters()
        imparam['extent'] = param['extent']
        return DG.get_space(**param),imparam

    @classmethod
    def get_screen_parameters(cls,**kwargs):
        ratio = kwargs.get('ratio',1)
        extent = (cls.__min_x*ratio,
                cls.__max_x*ratio,
                cls.__max_y,
                cls.__max_y + (cls.__max_y-cls.__min_y)*.1)
        cols = cls.__hd_w*ratio
        rows = 2
        return { 'extent': extent, 'cols': cols, 'rows': rows }

    @classmethod
    def get_screen(cls,**kwargs):
        param = cls.get_screen_parameters(**kwargs)
        imparam = cls.get_imshow_parameters()
        imparam['extent'] = param['extent']
        return DG.get_screen(**param),imparam

def create_canvas():
    pass

def static():
    space_w = 2
    h,w = Settings.get_canvas()
    ax1 = plt.subplot2grid((h,w), (0,0), colspan=space_w, rowspan=h)
    ax2 = plt.subplot2grid((h,w), (0,space_w), colspan=w-space_w)
    ax3 = plt.subplot2grid((h,w), (1,space_w), colspan=w-space_w, rowspan=h-1)
    Settings.configure_axes(ax1,ax2,ax3)

    space,space_param = Settings.get_space()
    screen,screen_param = Settings.get_screen()
    ax1.imshow(screen,**screen_param)
    ax1.imshow(space,**space_param)
    ax1.set_aspect(aspect='equal',anchor='S')
    ax1.set_axis_off()
    ax1.set_xlim(left=space_param['extent'][0], right=space_param['extent'][1])
    ax1.set_ylim(bottom=space_param['extent'][2], top=screen_param['extent'][3])

    screen,screen_param = Settings.get_screen(ratio=2*(w-space_w))
    ax2.imshow(screen,**screen_param)
    ax2.set_aspect(aspect='auto')

    space,space_param = Settings.get_zoombox(ratio=(h-1)/(w-space_w))
    ax3.set_aspect(aspect='equal',anchor='S')
    ax3.imshow(space,**space_param)

    plt.show()

if __name__=='__main__':
    static()
