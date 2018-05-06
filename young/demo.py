from logging import getLogger
from matplotlib.pyplot import figure,subplot2grid,get_cmap
from matplotlib.ticker import FuncFormatter
from .interference import YoungInterference
from .tools import log_test,kwargs_figure
logger = getLogger(__name__)

"""
Complete demo
"""
class YoungDemo(YoungInterference):
    DEFAULT = {
            'h': 6, 'w': 9, 'cw': 2,
        }

    """
    Dimensions
    """
    @property
    def h(self):
        return self.__h
    @h.setter
    def h(self,v):
        self.__h =  max(1,int(v))
    @property
    def w(self):
        return self.__w
    @w.setter
    def w(self,v):
        self.__w = max(1,int(v))
    @property
    def cw(self):
        return self.__cw
    @cw.setter
    def cw(self,v):
        self.__cw = max(1,min(int(v),self.w-1))

    """
    Figure
    """
    @property
    def fig(self):
        f = self.__fig
        if f is None:
            f = figure(**self.__fig_cfg)
            self.__fig = f
        return f

    """
    Axes config
    """
    def config_ax(self,*axs):
        for ax in axs:
            ax.tick_params(
                    left=0,right=0,bottom=0,top=0,
                    labelleft=0,labelright=0,labelbottom=0,labeltop=0,
                    direction='out',length=3,
                    )
    def config_axc(self,ax=None):
        a = self.__axc
        if a is None:
            self.config_ax(ax)
            ax.tick_params(bottom=1,left=1,labelleft=1)
            ax.set_frame_on(0)
            ax.set_aspect(aspect='equal',anchor='S')
            return
        tk = FuncFormatter(lambda x,pos: '{0:.2f} cm'.format(x/1e7))
        a.set_xticks([-self.d,self.d])
        a.set_yticks([self.y])
        a.yaxis.set_major_formatter(tk)
        a.set_xlim(left=int(self.x_min/self.x_ratio),
                right=int(self.x_max/self.x_ratio))
        a.set_ylim(bottom=self.y_min,top=self.y_max+self.y_screen)
    def config_axs(self,ax=None):
        a = self.__axs
        if a is None:
            self.config_ax(ax)
            ax.tick_params(bottom=1,top=1)
            return
        a.set_xticks([0])
        a.set_yticks([])
        a.set_aspect(aspect='auto')
    def config_axz(self,ax=None):
        a = self.__axz
        if a is None:
            self.config_ax(ax)
            return

    """
    Axes
    """
    @property
    def ax_complete(self):
        a = self.__axc
        if a is None:
            a = subplot2grid((self.h,self.w), (0,0),
                    colspan=self.cw, rowspan=self.h, fig=self.fig)
            self.config_axc(a)
            self.__axc = a
        return a
    @property
    def ax_screen(self):
        a = self.__axs
        if a is None:
            a = subplot2grid((self.h,self.w), (0,self.cw),
                    colspan=self.w-self.cw, rowspan=1, fig=self.fig)
            self.config_axs(a)
            self.__axs = a
        return a
    @property
    def ax_zoom(self):
        a = self.__axz
        if a is None:
            a = subplot2grid((self.h,self.w), (1,self.cw),
                    colspan=self.w-self.cw, rowspan=self.h-1, fig=self.fig)
            self.config_axz(a)
            self.__axz = a
        return a

    """
    Images config
    """
    @property
    def im_cfg(self):
        c = self.__imcfg
        if c is None:
            logger.warning('TODO: Get cmap')
            c = {
                    'interpolation': 'nearest',
                    'cmap': get_cmap('Greys'),
                    'origin': 'lower',
                }
            self.__imcfg = c
        return c

    """
    Draw
    """
    def figure_config(self,**kwargs):
        self.__fig_cfg = kwargs_figure(**kwargs)
    def figure(self):
        fig = self.fig
        self.draw_axc()
        self.draw_axs()
        self.draw_axz()
        return fig
    def draw_axc(self):
        axc = self.ax_complete
        axc.cla()
        # Get left and right bounds
        l = int(self.x_min/self.x_ratio)
        r = int(self.x_max/self.x_ratio)
        # Get and draw space
        im,ex = self.get_intensity(left=l,right=r)
        axc.imshow(im,extent=ex,**self.im_cfg)
        # Get and draw screen
        im,ex = self.get_projection(left=l,right=r)
        axc.imshow(im,extent=ex,**self.im_cfg)
        # Draw nice separation line
        axc.axhline(self.y,color='w',linestyle='-')
        # Reconfigure volatile aspect settings
        self.config_axc()
    def draw_axs(self):
        axs = self.ax_screen
        axs.cla()
        # Get and draw screen
        im,ex = self.get_projection(left=self.x_min,right=self.x_max)
        axs.imshow(im,extent=ex,**self.im_cfg)
        # Reconfigure volatile aspect settings
        self.config_axs()
        pass
    def draw_axz(self):
        axz = self.ax_zoom
        self.config_axz()
        pass

    """
    Initialization
    """
    def __init__(self,**kwargs):
        YoungInterference.__init__(self,**kwargs)
        config = YoungDemo.DEFAULT.copy()
        config.update(kwargs)
        # Settings
        self.h  = config['h']
        self.w  = config['w']
        self.cw = config['cw']
        self.__fig_cfg = dict()

# log_test(logger)
if __name__=='__main__':
    pass
