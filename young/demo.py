from logging import getLogger
from matplotlib.pyplot import figure,subplot2grid,Circle
from matplotlib.ticker import FuncFormatter
from matplotlib.widgets import Slider
from .interference import YoungInterference
from .tools import kwargs_figure,ProxyObject,UpdateObject,wavelength_to_color,color_to_cmap,array_indexof,unit_identify
logger = getLogger(__name__)

"""
Complete demo
"""
class YoungDemo(ProxyObject,UpdateObject):
    __id = 0
    ATTRIBUTES = ['h','w','cw']
    DEFAULT = {
            'h': 6, 'w': 9, 'cw': 2,
        }

    """
    Children
    """
    @property
    def normal(self):
        self.__debug("get:normal")
        return self.__normal
    @normal.setter
    def normal(self,v):
        if self.__normal is not None:
            self.__error("set:normal:AlreadySet")
            raise AttributeError
        self.__debug("set:normal:{:}",repr(v))
        self.__normal = v
    @property
    def zoom(self):
        self.__debug("get:zoom")
        return self.__zoom
    @zoom.setter
    def zoom(self,v):
        if self.__zoom is not None:
            self.__error("set:zoom:AlreadySet")
            raise AttributeError
        self.__debug("set:zoom:{:}",repr(v))
        self.__zoom = v

    """
    Dimensions
    """
    @property
    def h(self):
        self.__debug("get:h")
        return self.__h
    @h.setter
    def h(self,v):
        self.__debug("set:h:{:}",v)
        self.__h =  max(1,int(v))
    @property
    def w(self):
        self.__debug("get:w")
        return self.__w
    @w.setter
    def w(self,v):
        self.__debug("set:w:{:}",v)
        self.__w = max(1,int(v))
    @property
    def cw(self):
        self.__debug("get:cw")
        return self.__cw
    @cw.setter
    def cw(self,v):
        self.__debug("set:cw:{:}",v)
        self.__cw = max(1,min(int(v),self.w-1))

    """
    Colormap
    """
    @property
    def color(self):
        self.__debug("get:color")
        c = self.__color
        if c is None:
            self.__debug("get:color:CacheMiss")
            logger.debug("Computing color from wavelength {:d}".format(self.wl))
            c = wavelength_to_color(self.wl)
            self.__color = c
        return c
    @property
    def cmap(self):
        self.__debug("get:cmap")
        c = self.__cmap
        if c is None:
            self.__debug("get:cmap:CacheMiss")
            c = color_to_cmap(self.color)
            self.__cmap = c
        return c

    """
    Source points
    """
    @property
    def normal_srcs(self):
        self.__debug("get:normal_srcs")
        s = self.__normal_srcs
        if s is None:
            self.__debug("get:normal_srcs:CacheMiss")
            p = { 'color': self.color, 'ec': 'w', 'radius': (self.x_max-self.x_min)/self.x_ratio/80 }
            s = (Circle((-self.d,0),**p),Circle((self.d,0),**p))
            self.__normal_srcs = s
        return s
    @property
    def zoom_srcs(self):
        self.__debug("get:zoom_srcs")
        s = self.__zoom_srcs
        if s is None:
            self.__debug("get:zoom_srcs:CacheMiss")
            p = { 'color': self.color, 'ec': 'w', 'radius': (self.zoom.x_max-self.zoom.x_min)/200 }
            s = (Circle((-self.d,0),**p),Circle((self.d,0),**p))
            self.__zoom_srcs = s
        return s

    """
    Middle x
    """
    @property
    def x_mid(self):
        self.__debug("get:x_mid")
        x = self.__x_mid
        if x is None:
            self.__debug("get:x_mid:CacheMiss")
            xr = self.xrange
            dp = self.projection_phase
            x = xr[array_indexof(dp,0)]
            self.__x_mid = x
        return x

    """
    Figure
    """
    @property
    def fig(self):
        self.__debug("get:fig")
        f = self.__fig
        if f is None:
            self.__debug("get:fig:CacheMiss")
            f = figure(**self.fig_cfg)
            self.__fig = f
        return f

    """
    Axes config
    """
    def config_ax(self,*axs):
        self.__debug("config_ax")
        for ax in axs:
            ax.tick_params(
                    left=0,right=0,bottom=0,top=0,
                    labelleft=0,labelright=0,labelbottom=0,labeltop=0,
                    direction='out',length=3,
                    )
    def config_axc(self,ax=None):
        self.__debug("config_axc")
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
        self.__debug("config_axs")
        a = self.__axs
        if a is None:
            self.config_ax(ax)
            ax.tick_params(bottom=1,top=1)
            return
        a.set_xticks([0,self.x_mid])
        a.set_yticks([])
        a.set_aspect(aspect='auto')
    def config_axz(self,ax=None):
        self.__debug("config_axz")
        a = self.__axz
        if a is None:
            self.config_ax(ax)
            return
        a.set_aspect(aspect='equal',anchor='S')

    """
    Axes
    """
    @property
    def ax_complete(self):
        self.__debug("get:ax_complete")
        a = self.__axc
        if a is None:
            self.__debug("get:ax_complete:CacheMiss")
            a = subplot2grid((self.h,self.w), (0,0),
                    colspan=self.cw, rowspan=self.h, fig=self.fig)
            self.config_axc(a)
            self.__axc = a
        return a
    @property
    def ax_screen(self):
        self.__debug("get:ax_screen")
        a = self.__axs
        if a is None:
            self.__debug("get:ax_screen:CacheMiss")
            a = subplot2grid((self.h,self.w), (0,self.cw),
                    colspan=self.w-self.cw, rowspan=1, fig=self.fig)
            self.config_axs(a)
            self.__axs = a
        return a
    @property
    def ax_zoom(self):
        self.__debug("get:ax_zoom")
        a = self.__axz
        if a is None:
            self.__debug("get:ax_zoom:CacheMiss")
            a = subplot2grid((self.h,self.w), (1,self.cw),
                    colspan=self.w-self.cw, rowspan=self.h-1, fig=self.fig)
            self.config_axz(a)
            self.__axz = a
        return a

    """
    Sliders
    """
    __slider_h  = .015
    __slider_ih = .008
    __slider_l  = .37
    __slider_r  = .15
    __slider_y  = .99
    __slider_p  = {
            'valfmt': '%d',
            'closedmax': True,
            'valstep': 1,
        }
    def new_slider_ax(self):
        self.__slider_y -= self.__slider_h+self.__slider_ih
        self.__debug("new_slider_ax:{:}",self.__slider_y)
        return self.fig.add_axes([self.__slider_l,self.__slider_y,\
                1-self.__slider_l-self.__slider_r,self.__slider_h])
    @property
    def wl_slider(self):
        self.__debug("get:wl_slider")
        s = self.__wl_slider
        if s is None:
            self.__debug("get:wl_slider:CacheMiss")
            ax = self.new_slider_ax()
            s = Slider(ax, 'Wavelength (nm)', self.wl_min, self.wl_max,\
                    valinit=self.wl, **self.__slider_p)
            s.on_changed(self.wl_update)
            self.__wl_slider = s
        return s
    def wl_update(self,v):
        self.__info("wl_update:{:}",v)
        self.wl = v
    @property
    def p_slider(self):
        self.__debug("get:p_slider")
        s = self.__p_slider
        if s is None:
            self.__debug("get:p_slider:CacheMiss")
            ax = self.new_slider_ax()
            s = Slider(ax, 'Phase delay (nm)', self.p_min, self.p_max,\
                    valinit=self.p, **self.__slider_p)
            s.on_changed(self.p_update)
            self.__p_slider = s
        return s
    def p_update(self,v):
        self.__info("p_update:{:}",v)
        self.p = v
    @property
    def y_slider(self):
        self.__debug("get:y_slider")
        s = self.__y_slider
        if s is None:
            self.__debug("get:y_slider:CacheMiss")
            ax = self.new_slider_ax()
            unit,alpha = unit_identify(self.y_min,self.y,self.y_max)
            self.__y_slider_alpha = alpha
            y_min = self.y_min/alpha
            y_max = self.y_max/alpha
            y = self.y/alpha
            s = Slider(ax, 'Screen distance ({:})'.format(unit),
                    y_min,y_max,valinit = y,
                    valfmt='%1.2f',valstep=.01)
            s.on_changed(self.y_update)
            self.__y_slider = s
        return s
    def y_update(self,v):
        self.__info("y_update:{:}",v)
        self.y = v*self.__y_slider_alpha
    @property
    def d_slider(self):
        self.__debug("get:d_slider")
        s = self.__d_slider
        if s is None:
            self.__debug("get:d_slider:CacheMiss")
            ax = self.new_slider_ax()
            unit,alpha = unit_identify(self.d_min,self.d,self.d_max)
            alpha /= 2.
            self.__d_slider_alpha = alpha
            d_min = self.d_min/alpha
            d_max = self.d_max/alpha
            d = self.d/alpha
            s = Slider(ax, 'Intersource ({:})'.format(unit),
                    d_min,d_max,valinit = d,
                    valfmt='%1.2f',valstep=.05)
            s.on_changed(self.d_update)
            self.__d_slider = s
        return s
    def d_update(self,v):
        self.__info("d_update:{:}",v)
        self.d = v*self.__d_slider_alpha

    """
    Images config
    """
    @property
    def im_cfg(self):
        self.__debug("get:im_cfg")
        c = self.__imcfg
        if c is None:
            self.__debug("get:im_cfg:CacheMiss")
            c = {
                    'interpolation': 'nearest',
                    'cmap': self.cmap,
                    'origin': 'lower',
                    'vmin': 0,
                    'vmax': 4,
                }
            self.__imcfg = c
        return c

    """
    Draw
    """
    @property
    def fig_cfg(self):
        self.__debug("get:fig_cfg")
        c = self.__figcfg
        if c is None:
            self.__debug("get:fig_cfg:CacheMiss")
            c = dict()
            self.__figcfg = c
        return c
    def figure_config(self,**kwargs):
        self.__debug("figure_config:{:}",kwargs)
        self.__figcfg = kwargs_figure(**kwargs)
    def figure(self):
        self.__debug("figure")
        self.draw()
        return self.fig
    def draw(self):
        self.__debug("draw")
        self.draw_axc()
        self.draw_axs()
        self.draw_axz()
        _ = self.wl_slider
        _ = self.p_slider
        _ = self.y_slider
        _ = self.d_slider
    def draw_axc(self):
        self.__debug("draw_axc")
        axc = self.ax_complete
        axc.cla()
        # Get left and right bounds
        l = int(self.x_min/self.x_ratio)
        r = int(self.x_max/self.x_ratio)
        # Get and draw space
        im,ex = self.get_intensity(left=l,right=r)
        self.__info("draw_axc:intensity:min({:}):max({:})",im.min(),im.max())
        self.__info("draw_axc:im_cfg:{:}",self.im_cfg)
        axc.imshow(im,extent=ex,**self.im_cfg)
        # Get and draw screen
        im,ex = self.get_projection(left=l,right=r)
        self.__info("draw_axc:projection:min({:}):max({:})",im.min(),im.max())
        self.__info("draw_axc:im_cfg:{:}",self.im_cfg)
        axc.imshow(im,extent=ex,**self.im_cfg)
        # Draw source points
        sl,sr = self.normal_srcs
        axc.add_artist(sl)
        axc.add_artist(sr)
        # Draw nice separation line
        axc.axhline(self.y,color='w',linestyle='-')
        # Reconfigure volatile aspect settings
        self.config_axc()
    def draw_axs(self):
        self.__debug("draw_axs")
        axs = self.ax_screen
        axs.cla()
        # Get and draw screen
        im,ex = self.get_projection(left=self.x_min,right=self.x_max)
        self.__info("draw_axs:projection:min({:}):max({:})",im.min(),im.max())
        self.__info("draw_axc:im_cfg:{:}",self.im_cfg)
        axs.imshow(im,extent=ex,**self.im_cfg)
        # Draw nice middle fringe line
        axs.axvline(self.x_mid,color='w',linestyle='--')
        # Reconfigure volatile aspect settings
        self.config_axs()
        pass
    def draw_axz(self):
        self.__debug("draw_axz")
        axz = self.ax_zoom
        axz.cla()
        # Get and draw space
        im,ex = self.zoom.get_intensity()
        self.__info("draw_axz:intensity:min({:}):max({:})",im.min(),im.max())
        self.__info("draw_axc:im_cfg:{:}",self.im_cfg)
        axz.imshow(im,extent=ex,**self.im_cfg)
        # Draw source points
        sl,sr = self.zoom_srcs
        axz.add_artist(sl)
        axz.add_artist(sr)
        # Reconfigure volatile aspect settings
        self.config_axz()
        pass

    """
    Update handlers
    """
    __color_reset_trigger = 0
    def color_reset(self,**kwargs):
        self.__debug("color_reset")
        if self.__color_reset_trigger:
            self.__color = None
            self.__cmap = None
            self.__imcfg = None
            self.__zoom_srcs = None
            self.__normal_srcs = None
            self.draw()
            self.fig.canvas.draw()
        else:
            self.__info("color_reset:avoided")
        self.__color_reset_trigger ^= 1

    __p_reset_trigger = 0
    def p_reset(self,**kwargs):
        self.__debug("p_reset")
        if self.__p_reset_trigger:
            self.__x_mid = None
            self.draw()
            self.fig.canvas.draw()
        else:
            self.__info("p_reset:avoided")
        self.__p_reset_trigger ^= 1

    def y_reset(self,**kwargs):
        self.__debug("y_reset")
        self.__x_mid = None
        self.draw_axc()
        self.draw_axs()
        self.fig.canvas.draw()

    __d_reset_trigger = 0
    def d_reset(self,**kwargs):
        self.__debug("d_reset")
        if self.__d_reset_trigger:
            self.__xmid = None
            self.__zoom_srcs = None
            self.__normal_srcs = None
            self.draw()
            self.fig.canvas.draw()
        else:
            self.__info("d_reset:avoided")
        self.__d_reset_trigger ^= 1


    """
    Update
    """
    __handlers = {
            'wl': 'color_reset',
            'p': 'p_reset',
            'y': 'y_reset',
            'd': 'd_reset',
        }
    def update(self,*args,**kwargs):
        self.__debug("update:{:}:{:}",list(args),kwargs)
        for t in args:
            if t in self.__handlers:
                getattr(self,self.__handlers[t])(**kwargs)
            else:
                self.__error("update({:}):NotImplemented",t)
                raise NotImplementedError

    """
    Initialization
    """
    def __init__(self,**kwargs):
        # Give an ID
        YoungDemo.__id += 1
        self.__id = YoungDemo.__id
        # Child configurations
        YIFC=kwargs.pop('young_if_class',YoungInterference)
        self.normal = YIFC(**kwargs)
        ycfg = self.normal.young_cfg
        zdcfg = self.normal.display_cfg.copy()
        zboxratio = kwargs.get('zboxratio',9/16)
        zdcfg.x_max = ycfg.d_max*1.01
        zdcfg.y_max = zboxratio*zdcfg.x_max
        zdcfg.x_min = -zdcfg.x_max
        zdcfg.y_min = -zdcfg.y_max
        self.zoom = YIFC(young_cfg=ycfg,display_cfg=zdcfg)
        # Build configuration
        config = YoungDemo.DEFAULT.copy()
        config.update(kwargs)
        # Settings
        for key in YoungDemo.ATTRIBUTES:
            setattr(self,key,config[key])
        # Subscribe for updates
        self.normal.register(self,'wl')
        self.zoom.register(self,'wl')
        self.normal.register(self,'p')
        self.zoom.register(self,'p')
        self.normal.register(self,'y')
        self.normal.register(self,'d')
        self.zoom.register(self,'d')
        # Proxy setup
        self._proxy_children_set(self.normal)
        self._freeze()

    """
    To string
    """
    def __repr__(self):
        return "YoungDemo{:d}".format(self.__id)
    def __str__(self):
        res = [repr(self)]
        res.append('  (normal) '+str(self.normal).replace('\n','\n  '))
        res.append('  (zoomed) '+str(self.zoom).replace('\n','\n  '))
        return '\n'.join(res)

    def __debug(self,msg,*args,**kwargs):
        logger.debug("YoungDemo[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __info(self,msg,*args,**kwargs):
        logger.info("YoungDemo[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __warning(self,msg,*args,**kwargs):
        logger.warning("YoungDemo[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __error(self,msg,*args,**kwargs):
        logger.error("YoungDemo[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __critical(self,msg,*args,**kwargs):
        logger.critical("YoungDemo[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))

if __name__=='__main__':
    yd = YoungDemo()
    print(yd)
