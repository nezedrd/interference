from matplotlib import pyplot as plt
from matplotlib import ticker as tkr
from matplotlib.widgets import Slider
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
            'direction':     'out',
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
    __add_y =    1e4 #   1 cm
    __y     =   30e4 #  30 cm
    __min_d =    100 # 100 nm
    __max_d =   30e3 #  30 mm
    __d     = V.get_inter_source_distance()
    __src1  = None
    __src2  = None
    __src3  = None
    __src4  = None
    __ref_d =   15e3
    __hd_w = 1024
    __ld_w = 128

    @classmethod
    def get_src(cls):
        if cls.__src1 is None:
            cls.set_src()
        return cls.__src1,cls.__src2,cls.__src3,cls.__src4
    @classmethod
    def set_src(cls):
        p = { 'color': DG.get_color(),
                'ec': 'w',
                'radius': (cls.__max_x - cls.__min_x)/80 }
        cls.__src1 = plt.Circle((-cls.__d,0), **p)
        cls.__src2 = plt.Circle((+cls.__d,0), **p)
        p['radius']/=5
        cls.__src3 = plt.Circle((-cls.__d,0), **p)
        cls.__src4 = plt.Circle((+cls.__d,0), **p)

    @classmethod
    def get_min_x(cls):
        return cls.__min_x
    @classmethod
    def get_max_x(cls):
        return cls.__max_x
    @classmethod
    def get_min_y_cm(cls):
        min_y = cls.__min_y/1e4
        return min_y
    @classmethod
    def get_min_y(cls):
        return cls.__min_y
    @classmethod
    def get_max_y_cm(cls):
        max_y = cls.__max_y/1e4
        return max_y
    @classmethod
    def get_max_y(cls):
        return cls.__max_y
    @classmethod
    def get_add_y(cls):
        return cls.__add_y
    @classmethod
    def get_y_cm(cls):
        y = cls.__y/1e4
        return y
    @classmethod
    def get_y(cls):
        return cls.__y
    @classmethod
    def set_y_cm(cls,y):
        cls.__y = min(cls.__max_y,max(cls.__min_y,y*1e4))

    @classmethod
    def get_min_d_mm(cls):
        return cls.__min_d/1e3
    @classmethod
    def get_max_d_mm(cls):
        return cls.__max_d/1e3
    @classmethod
    def get_d(cls):
        return cls.__d
    @classmethod
    def get_d_mm(cls):
        return cls.__d/1e3
    @classmethod
    def set_d_mm(cls,d):
        cls.__d = min(cls.__max_d,max(cls.__min_d,d*1e3))
        V.set_inter_source_distance(cls.__d)
        cls.set_src()

    @classmethod
    def get_space_parameters(cls):
        extent = (cls.__min_x,
                cls.__max_x,
                cls.__min_y,
                cls.__y - (cls.__add_y)*.1)
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
        max_x = min(cls.__max_x,2*cls.__ref_d)
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
                cls.__y,
                cls.__y + cls.__add_y)
        cols = cls.__hd_w*ratio
        rows = 2
        return { 'extent': extent, 'cols': cols, 'rows': rows }

    @classmethod
    def get_screen(cls,**kwargs):
        param = cls.get_screen_parameters(**kwargs)
        imparam = cls.get_imshow_parameters()
        imparam['extent'] = param['extent']
        return DG.get_screen(**param),imparam

__slider_h = 0.02
__slider_ih= 0.01
__slider_l = 0.37
__slider_r = 0.15
__slider_y = 0.99
def new_slider(f):
    global __slider_y,__slider_h,__slider_l,__slider_r,__slider_ih
    __slider_y -= __slider_h + __slider_ih
    return f.add_axes([__slider_l,__slider_y,1-__slider_l-__slider_r,__slider_h])

def main():
    fig = plt.figure()
    space_w = 2
    h,w = Settings.get_canvas()
    ax1 = plt.subplot2grid((h,w), (0,0), colspan=space_w, rowspan=h)
    ax2 = plt.subplot2grid((h,w), (0,space_w), colspan=w-space_w)
    ax3 = plt.subplot2grid((h,w), (1,space_w), colspan=w-space_w, rowspan=h-1)
    Settings.configure_axes(ax1,ax2,ax3)
    tk1 = tkr.FuncFormatter(lambda x,pos: '{0:.2f} cm'.format(x/1e4))
    ax1.tick_params(bottom=True,left=True,labelleft=True)
    ax1.set_frame_on(False)
    srcs = [None,None,None,None]

    def get_src():
        Settings.set_src()
        srcs[:] = Settings.get_src()
    get_src()

    def draw_main():
        space,space_param = Settings.get_space()
        screen,screen_param = Settings.get_screen()
        ax1.cla()
        ax1.imshow(screen,**screen_param)
        ax1.imshow(space,**space_param)
        ax1.add_artist(srcs[0])
        ax1.add_artist(srcs[1])
        ax1.set_aspect(aspect='equal',anchor='S')
        ax1.set_xlim(left=Settings.get_min_x(), right=Settings.get_max_x())
        ax1.set_ylim(bottom=Settings.get_min_y(), top=Settings.get_max_y()+Settings.get_add_y())
        d = Settings.get_d()
        ax1.set_xticks([-d,d])
        ax1.set_yticks([Settings.get_y()])
        ax1.yaxis.set_major_formatter(tk1)
    draw_main()

    def draw_screen():
        screen,screen_param = Settings.get_screen(ratio=2*(w-space_w))
        ax2.cla()
        ax2.imshow(screen,**screen_param)
        ax2.set_aspect(aspect='auto')
    draw_screen()

    def draw_space():
        space,space_param = Settings.get_zoombox(ratio=(h-1)/(w-space_w))
        ax3.cla()
        ax3.imshow(space,**space_param)
        ax3.add_artist(srcs[2])
        ax3.add_artist(srcs[3])
        ax3.set_aspect(aspect='equal',anchor='S')
    draw_space()

    axwl = new_slider(fig)#fig.add_axes([0.4,0.9,0.45,0.02]) # [ x, y, w, h ]
    slwl = Slider(axwl, 'Wavelength', 400, 690, valinit=V.get_wavelength())
    def upwl(val):
        V.set_wavelength(val)
        DG.reset_cmap()
        get_src()
        draw_main()
        draw_screen()
        draw_space()
        fig.canvas.draw()
    slwl.on_changed(upwl)

    axsd = new_slider(fig)#fig.add_axes([0.4,0.93,0.45,0.02])
    slsd = Slider(axsd, 'Screen distance', Settings.get_min_y_cm(),
            Settings.get_max_y_cm(), valinit=Settings.get_y_cm())
    def upsd(val):
        Settings.set_y_cm(val)
        draw_main()
        draw_screen()
        fig.canvas.draw()
    slsd.on_changed(upsd)

    axid = new_slider(fig)#fig.add_axes([0.4,0.96,0.45,0.02])
    slid = Slider(axid, 'Inter source distance', Settings.get_min_d_mm(),
            Settings.get_max_d_mm(), valinit=Settings.get_d_mm())
    def upid(val):
        Settings.set_d_mm(val)
        get_src()
        draw_main()
        draw_screen()
        draw_space()
        fig.canvas.draw()
    slid.on_changed(upid)

    plt.show()

if __name__=='__main__':
    main()
