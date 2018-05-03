import numpy as np
import logging,functools#,itertools
from matplotlib import pyplot as plt
from matplotlib import ticker as tkr
logging.basicConfig(level=logging.INFO)

"""
DefaultObject
"""
class DefaultObject(object):
    def __getattr__(self,name):
        return None

"""
Unit formater
"""
def u_format(*args,fs='{:4d}'):
    units = { 1: 'nm', 1e3: 'μm', 1e6: 'mm', 1e7: 'cm' }
    steps = units.keys()
    a = np.array(args,dtype=int)
    for c in reversed(sorted(steps)):
        x = a/c
        y = x.astype(int)
        if (y == x).all():
            f = fs+units[c]
            ret = [ f.format(Y) for Y in y ]
            return (*ret,)
    return None

"""
Complete configuration
"""
class YoungConfig(DefaultObject):
    __id = 0
    DEFAULT = {
            'wl_min': 400, 'wl_max': 700, 'wl': 532,
            'd_min': 0, 'd_max': 20e3, 'd': 10e3,
            'p_min': -700, 'p_max': 700, 'p': 0,
            'x_min': -20e7, 'x_max': 20e7, 'x': 0, 'x_ratio': 4,
            'y_min': 0, 'y_max': 30e7, 'y': 30e7, 'y_screen': 1e7,
            'res': 4096, # Number of pixels for the whole width
        }

    """
    Parameters:
    * physical
      * wavelength, wavelength range
      * intersource, intersource range
     (* screen position)
      * phase delay, range
    * graphical
      * left, right, bottom, top bounds
      * resolution
    """
    # Wavelength
    @property
    def wl_min(self):
        return self.__wlm
    @wl_min.setter
    def wl_min(self,v):
        self.__wlm = int(max(350,v))
    @property
    def wl_max(self):
        return self.__wlM
    @wl_max.setter
    def wl_max(self,v):
        self.__wlM = int(min(v,750))
    @property
    def wl(self):
        return self.__wl
    @wl.setter
    def wl(self,v):
        self.__wl = int(max(self.wl_min,min(v,self.wl_max)))

    # Intersource distance
    @property
    def d_min(self):
        return self.__dm
    @d_min.setter
    def d_min(self,v):
        self.__dm = int(max(0,v))
    @property
    def d_max(self):
        return self.__dM
    @d_max.setter
    def d_max(self,v):
        self.__dM = int(v)
    @property
    def d(self):
        return self.__d
    @d.setter
    def d(self,v):
        self.__d = int(max(self.d_min,min(v,self.d_max)))

    # Phase delay
    @property
    def p_min(self):
        return self.__pm
    @p_min.setter
    def p_min(self,v):
        self.__pm = int(v)
    @property
    def p_max(self):
        return self.__pM
    @p_max.setter
    def p_max(self,v):
        self.__pM = int(v)
    @property
    def p(self):
        return self.__p
    @p.setter
    def p(self,v):
        self.__p = int(max(self.p_min,min(v,self.p_max)))

    # Graphical bounds
    @property
    def x_min(self):
        return self.__xm
    @x_min.setter
    def x_min(self,v):
        self.__xm = int(v)
    @property
    def x_max(self):
        return self.__xM
    @x_max.setter
    def x_max(self,v):
        self.__xM = int(v)
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self,v):
        self.__x = int(max(self.x_min,min(v,self.x_max)))
    @property
    def x_ratio(self):
        return self.__xr
    @x_ratio.setter
    def x_ratio(self,v):
        self.__xr = int(max(1,v))
    @property
    def y_min(self):
        return self.__ym
    @y_min.setter
    def y_min(self,v):
        self.__ym = int(v)
    @property
    def y_max(self):
        return self.__yM
    @y_max.setter
    def y_max(self,v):
        self.__yM = int(v)
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self,v):
        self.__y = int(max(self.y_min,min(v,self.y_max)))
    @property
    def y_screen(self):
        return self.__ys
    @y_screen.setter
    def y_screen(self,v):
        self.__ys = int(max(1,v))

    # Resolution
    @property
    def res(self):
        return self.__r
    @res.setter
    def res(self,v):
        self.__r = int(max(0,v))
    @property
    def xres(self):
        return self.res
    @property
    def yres(self):
        Δy = self.y_max - self.y_min
        Δx = self.x_max - self.x_min
        ρx = self.xres
        return int(ρx*Δy/Δx)

    """
    Initialize configuration
    """
    def __init__(self,**kwargs):
        config = YoungConfig.DEFAULT.copy()
        config.update(kwargs)
        # Give an ID
        YoungConfig.__id += 1
        self.__id = YoungConfig.__id
        # Settings
        self.wl_min   = config['wl_min']
        self.wl_max   = config['wl_max']
        self.wl       = config['wl']
        self.d_min    = config['d_min']
        self.d_max    = config['d_max']
        self.d        = config['d']
        self.p_min    = config['p_min']
        self.p_max    = config['p_max']
        self.p        = config['p']
        self.x_min    = config['x_min']
        self.x_max    = config['x_max']
        self.x        = config['x']
        self.x_ratio  = config['x_ratio']
        self.res      = config['res']
        self.y_min    = config['y_min']
        self.y_max    = config['y_max']
        self.y        = config['y']
        self.y_screen = config['y_screen']

    """
    To string
    """
    def __repr__(self):
        return "YoungConfig{:d}".format(self.__id)
    def __str__(self):
        res = [repr(self)]
        wlm,wl,wlM, = u_format(self.wl_min,self.wl,self.wl_max)
        res.append("  λ: {:} --- {:} --> {:}".format(wlm,wl,wlM))
        dm, d, dM,  = u_format(self.d_min, self.d, self.d_max )
        res.append("  d: {:} --- {:} --> {:}".format(dm, d, dM ))
        pm, p, pM,  = u_format(self.p_min, self.p, self.p_max )
        res.append("  p: {:} --- {:} --> {:}".format(pm, p, pM ))
        xm, xM,     = u_format(self.x_min, self.x_max)
        res.append("  x: [ {:}, {:} ] {:d}px".format(xm,xM,self.xres))
        ym, yM,     = u_format(self.y_min, self.y_max)
        res.append("  y: [ {:}, {:} ] {:d}px".format(ym,yM,self.yres))
        return '\n'.join(res)

"""
Numpy approximate index of
"""
def a_indexof(array,value):
    return np.argmin(np.abs(array-value))

"""
Arguments for extent
"""
def parse_args(**kwargs):
    keys = kwargs['keys']
    deft = kwargs.get('defaults',dict())
    args = kwargs['args']
    dest = kwargs.get('dest',dict())
    for k,v in keys.items():
        dest[k] = functools.reduce(
                lambda x,y: args.get(y,x),
                reversed(v+[deft.get(k,None)])
                )
    return dest
def get_extent(d,*args,**kwargs):
    kwargs.update(enumerate(kwargs.get('extent',())))
    kwargs.update(enumerate(args))
    e = dict()
    a = {
      'left': [0,'l','left'],
      'right': [1,'r','right'],
      'bottom': [2,'b','bottom'],
      'top': [3,'t','top'],
      }
    return parse_args(keys=a,defaults=d,args=kwargs,dest=e)

"""
Extract keyword arguments
"""
def kwargs_extract(name,filtr,kwargs):
    okeys = set(kwargs.keys())
    keys = okeys & filtr
    if len(keys) != len(kwargs):
        print("Unrecognized arguments for '{:}':\n  {:}"\
                .format(name,okeys-keys))
    return { k: kwargs[k] for k in keys }
figure_arguments = { 'num', 'figsize', 'dpi', 'facecolor', 'edgecolor',
        'frameon', 'FigureClass', 'clear' }
Figure_arguments = { 'figsize', 'dpi', 'facecolor', 'edgecolor', 'linewidth',
        'frameon', 'subplotpars', 'tight_layout', 'constrained_layout' }
def kwargs_figure(**kwargs):
    filtr = figure_arguments | Figure_arguments
    return kwargs_extract('figure',filtr,kwargs)

"""
Complete computation
"""
class YoungInterference(YoungConfig):
    __id = 0
    """
    Ranges
    """
    @property
    def xrange(self):
        xr = self.__xr
        if xr is None:
            xr = np.linspace(self.x_min,self.x_max,
                    num=self.xres,dtype=int)
            xr.setflags(write=0)
            self.__xr = xr
        return xr
    @property
    def yrange(self):
        yr = self.__yr
        if yr is None:
            yr = np.linspace(self.y_min,self.y_max,
                    num=self.yres,dtype=int)
            yr.setflags(write=0)
            self.__yr = yr
        return yr

    """
    Computing phase difference
    """
    @property
    def dphase(self):
        dp = self.__dp
        if dp is None:
            # xr is a line, yr is a column
            xr_left = np.square(self.xrange+self.d).reshape(1,-1)
            xr_right = np.square(self.xrange-self.d).reshape(1,-1)
            yr = np.square(self.yrange).reshape(-1,1)
            # xo and yo are ones of same size as xr and yr
            xo = np.ones(xr_left.shape)
            yo = np.ones(yr.shape)
            # xs and ys are of size (yres,xres)
            xs_left = yo*xr_left
            xs_right = yo*xr_right
            # del yo,xr_left,xr_right
            ys = yr*xo
            # del xo,yr
            # ps is of size (yres,xres)
            ps_left = np.sqrt(xs_left+ys)
            # del xs_left
            ps_right = np.sqrt(xs_right+ys)+self.p
            # del xs_right,ys
            dp = ps_right - ps_left
            # del ps_left,ps_right
            dp.setflags(write=0)
            self.__dp = dp
        return dp

    """
    Computing light intensity
    """
    @property
    def intensity(self):
        s = self.__s
        if s is None:
            s = 4*np.square(np.cos(np.pi*self.dphase/self.wl))
            s.setflags(write=0)
            self.__s = s
        return s
    """
    get_intensity(left,right,bottom,top)
    get_intensity(extent=(l,r,b,t))
    get_intensity(left=..., right=..., b=..., t=...)
    """
    def get_intensity(self,*args,**kwargs):
        # Get parameters and data
        d = {
                'left': self.x_min,
                'right': self.x_max,
                'bottom': self.y_min,
                'top': self.y
            }
        e = get_extent(d,*args,**kwargs)
        s = self.intensity
        # Get indices for view, and real extent
        xr = self.xrange
        li = a_indexof(xr,e['left'])
        l  = xr[li]
        ri = a_indexof(xr,e['right'])
        r  = xr[ri]
        yr = self.yrange
        bi = a_indexof(yr,e['bottom'])
        b  = yr[bi]
        ti = a_indexof(yr,e['top'])
        t  = yr[ti]
        # Return correct view and extent
        return s[bi:ti+1,li:ri+1],(l,r,b,t)

    """
    Extracting screen
    """
    @property
    def projection(self):
        s = self.intensity
        i = a_indexof(self.yrange,self.y)
        return s[i:i+1,:]
    def get_projection(self,*args,**kwargs):
        # Get parameters and data
        d = {
                'left': self.x_min,
                'right': self.x_max,
                'bottom': self.y,
                'top': self.y+self.y_screen,
            }
        e = get_extent(d,*args,**kwargs)
        s = self.intensity
        # Get indices for view, and real extent
        xr = self.xrange
        li = a_indexof(xr,e['left'])
        l  = xr[li]
        ri = a_indexof(xr,e['right'])
        r  = xr[ri]
        yr = self.yrange
        bi = a_indexof(yr,e['bottom'])
        b  = yr[bi]
        t  = e['top']-e['bottom']+b
        return s[bi:bi+1,li:ri+1],(l,r,b,t)

    """
    Interference part needs no initialization
    """
    def __init__(self,**kwargs):
        YoungConfig.__init__(self,**kwargs)

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
            f = plt.figure(**self.__fig_cfg)
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
        tk = tkr.FuncFormatter(lambda x,pos: '{0:.2f} cm'.format(x/1e7))
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
            return
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
            a = plt.subplot2grid((self.h,self.w), (0,0),
                    colspan=self.cw, rowspan=self.h, fig=self.fig)
            self.config_axc(a)
            self.__axc = a
        return a
    @property
    def ax_screen(self):
        a = self.__axs
        if a is None:
            a = plt.subplot2grid((self.h,self.w), (0,self.cw),
                    colspan=self.w-self.cw, rowspan=1, fig=self.fig)
            self.config_axs(a)
            self.__axs = a
        return a
    @property
    def ax_zoom(self):
        a = self.__axz
        if a is None:
            a = plt.subplot2grid((self.h,self.w), (1,self.cw),
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
            logging.warning('TODO: Get cmap')
            c = {
                    'interpolation': 'nearest',
                    'cmap': plt.get_cmap('Greys'),
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
        # axc.cla()
        l = int(self.x_min/self.x_ratio)
        r = int(self.x_max/self.x_ratio)
        im,ex = self.get_intensity(left=l,right=r)
        axc.imshow(im,extent=ex,**self.im_cfg)
        im,ex = self.get_projection(left=l,right=r)
        axc.imshow(im,extent=ex,**self.im_cfg)
        axc.axhline(self.y,color='w',linestyle='-')
        self.config_axc()
    def draw_axs(self):
        pass
    def draw_axz(self):
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

if __name__=='__main__':
    yc = YoungDemo()
    # yc.y = yc.y_max/2
    # yc.figure_config(wonderful=True,facecolor='g')
    fig = yc.figure()
    fig.savefig('/home/neze/Desktop/try.png')
    plt.show()
