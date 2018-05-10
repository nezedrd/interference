from numpy import abs,linspace,square,ones,sqrt,cos,pi,exp
from .tools import get_extent,array_indexof,ProxyObject,UpdateObject
from .config import DisplayConfig,YoungConfig
from logging import getLogger
logger = getLogger(__name__)

"""
Complete computation
"""
class YoungAttenuatedInterference(ProxyObject,UpdateObject):
    __id = 0

    """
    Children
    """
    @property
    def display_cfg(self):
        self.__debug("get:display_cfg")
        return self.__display_cfg
    @display_cfg.setter
    def display_cfg(self,v):
        if self.__display_cfg is not None:
            self.__error("set:display_cfg:AlreadySet")
            raise AttributeError
        self.__debug("set:display_cfg:{:}",repr(v))
        self.__display_cfg = v
    @property
    def young_cfg(self):
        self.__debug("get:young_cfg")
        return self.__young_cfg
    @young_cfg.setter
    def young_cfg(self,v):
        if self.__young_cfg is not None:
            self.__error("set:young_cfg:AlreadySet")
            raise AttributeError
        self.__debug("set:young_cfg:{:}",repr(v))
        self.__young_cfg = v

    """
    Ranges
    """
    @property
    def xrange(self):
        self.__debug("get:xrange")
        xr = self.__xr
        if xr is None:
            self.__info("get:xrange:CacheMiss")
            xr = linspace(self.x_min,self.x_max,
                    num=self.xres,dtype=int)
            xr.setflags(write=0)
            self.__xr = xr
        return xr
    @property
    def yrange(self):
        self.__debug("get:yrange")
        yr = self.__yr
        if yr is None:
            self.__info("get:yrange:CacheMiss")
            yr = linspace(self.y_min,self.y_max,
                    num=self.yres,dtype=int)
            yr.setflags(write=0)
            self.__yr = yr
        return yr

    """
    Computing phase difference
    """
    def compute_distances(self):
        xr_left = square(self.xrange+self.d).reshape(1,-1)
        xr_right = square(self.xrange-self.d).reshape(1,-1)
        yr = square(self.yrange).reshape(-1,1)
        xo = ones(xr_left.shape)
        yo = ones(yr.shape)
        xs_left = yo*xr_left
        xs_right = yo*xr_right
        ys = yr*xo
        ps_left = sqrt(xs_left+ys)
        ps_left.setflags(write=0)
        ps_right = sqrt(xs_right+ys)
        ps_right.setflags(write=0)
        self.__dleft = ps_left
        self.__dright = ps_right
    @property
    def dleft(self):
        self.__debug("get:dleft")
        dl = self.__dleft
        if dl is None:
            self.__info("get:dleft:CacheMiss")
            self.compute_distances()
            dl = self.__dleft
        return dl
    @property
    def dright(self):
        self.__debug("get:dright")
        dr = self.__dright
        if dr is None:
            self.__info("get:dright:CacheMiss")
            self.compute_distances()
            dr = self.__dright
        return dr
    @property
    def dphase(self):
        self.__debug("get:dphase")
        dp = self.__dp
        if dp is None:
            self.__info("get:dphase:CacheMiss")
            dp = self.dright - self.dleft + self.p
            dp.setflags(write=0)
            self.__dp = dp
        return dp

    """
    Computing light intensity
    """
    @property
    def intensity(self):
        self.__debug("get:intensity")
        s = self.__s
        if s is None:
            self.__info("get:intensity:CacheMiss")
            self.__info("get:intensity:R:{:} nm",self.R)
            dl = -self.dleft/self.R
            self.__info("get:intensity:dl:min({:}):max({:})",-dl.max(),-dl.min())
            dr = -self.dright/self.R
            self.__info("get:intensity:dr:min({:}):max({:})",-dr.max(),-dr.min())
            s1 = exp(dl)+exp(dr)
            self.__info("get:intensity:s1:min({:}):max({:})",s1.min(),s1.max())
            s2 = 2*exp((dl+dr)/2)*cos(pi*self.dphase/self.wl)
            self.__info("get:intensity:s2:min({:}):max({:})",s2.min(),s2.max())
            s = s1+s2
            s.setflags(write=0)
            self.__s = s
        return s
    def wl_reset(self):
        self.__info("wl_reset")
        self.__s = None
        self.notify('wl')
    def p_reset(self):
        self.__info("p_reset")
        self.__dp = None
        self.__s = None
        self.notify('p')
    def y_reset(self):
        self.__info("y_reset")
        self.notify('y')
    def d_reset(self):
        self.__info("d_reset")
        self.__dleft = None
        self.__dright = None
        self.__dp = None
        self.__s = None
        self.notify('d')
    """
    get_intensity(left,right,bottom,top)
    get_intensity(extent=(l,r,b,t))
    get_intensity(left=..., right=..., b=..., t=...)
    """
    def get_intensity(self,*args,**kwargs):
        self.__debug("get_intensity:{:}:{:}",list(args),kwargs)
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
        li = array_indexof(xr,e['left'])
        l  = xr[li]
        ri = array_indexof(xr,e['right'])
        r  = xr[ri]
        yr = self.yrange
        bi = array_indexof(yr,e['bottom'])
        b  = yr[bi]
        ti = array_indexof(yr,e['top'])
        t  = yr[ti]
        # Return correct view and extent
        return s[bi:ti+1,li:ri+1],(l,r,b,t)

    """
    Extracting screen
    """
    @property
    def projection_phase(self):
        self.__debug("get:projection_phase")
        d = self.dphase
        i = array_indexof(self.yrange,self.y)
        return d[i:i+1,:]
    @property
    def projection(self):
        self.__debug("get:projection")
        s = self.intensity
        i = array_indexof(self.yrange,self.y)
        return s[i:i+1,:]
    def get_projection(self,*args,**kwargs):
        self.__debug("get_projection:{:}:{:}",list(args),kwargs)
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
        li = array_indexof(xr,e['left'])
        l  = xr[li]
        ri = array_indexof(xr,e['right'])
        r  = xr[ri]
        yr = self.yrange
        bi = array_indexof(yr,e['bottom'])
        b  = yr[bi]
        t  = e['top']-e['bottom']+b
        return s[bi:bi+1,li:ri+1],(l,r,b,t)

    """
    Update
    """
    __handlers = {
            'wl': 'wl_reset',
            'p': 'p_reset',
            'y': 'y_reset',
            'd': 'd_reset',
        }
    def update(self,*args,**kwargs):
        self.__debug("update:{:}:{:}",list(args),kwargs)
        for t in args:
            if t in self.__handlers:
                getattr(self,self.__handlers[t])()
            else:
                self.__error("update({:}):NotImplemented",t)
                raise NotImplementedError

    """
    Interference part needs no initialization
    """
    def __init__(self,**kwargs):
        # Give an ID
        YoungAttenuatedInterference.__id += 1
        self.__id = YoungAttenuatedInterference.__id
        # Child configurations
        ycfg = kwargs.pop('young_cfg',None)
        dcfg = kwargs.pop('display_cfg',None)
        self.young_cfg = ycfg or YoungConfig(**kwargs)
        self.display_cfg = dcfg or DisplayConfig(**kwargs)
        # Subscribe for updates
        self.young_cfg.register(self,'wl')
        self.young_cfg.register(self,'p')
        self.display_cfg.register(self,'y')
        self.young_cfg.register(self,'d')
        # Proxy setup
        self._proxy_children_set(self.young_cfg,self.display_cfg)
        self._freeze()

    """
    To string
    """
    def __repr__(self):
        return "YoungAttenuatedInterference{:d}".format(self.__id)
    def __str__(self):
        res = [repr(self)]
        res.append('  '+str(self.young_cfg).replace('\n','\n  '))
        res.append('  '+str(self.display_cfg).replace('\n','\n  '))
        return '\n'.join(res)

    def __debug(self,msg,*args,**kwargs):
        logger.debug("YoungAttenuatedInterference[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __info(self,msg,*args,**kwargs):
        logger.info("YoungAttenuatedInterference[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __warning(self,msg,*args,**kwargs):
        logger.warning("YoungAttenuatedInterference[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __error(self,msg,*args,**kwargs):
        logger.error("YoungAttenuatedInterference[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __critical(self,msg,*args,**kwargs):
        logger.critical("YoungAttenuatedInterference[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))

if __name__=='__main__':
    yi = YoungAttenuatedInterference()
    print(yi)
