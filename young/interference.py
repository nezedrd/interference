from numpy import abs,linspace,square,ones,sqrt,cos,pi
from .tools import log_test,get_extent,array_indexof,ProxyObject,UpdateObject
from .config import DisplayConfig,YoungConfig
from logging import getLogger
logger = getLogger(__name__)

"""
Complete computation
"""
class YoungInterference(ProxyObject,UpdateObject):
    __id = 0

    """
    Children
    """
    @property
    def display_cfg(self):
        return self.__display_cfg
    @display_cfg.setter
    def display_cfg(self,v):
        if self.__display_cfg is not None:
            raise AttributeError
        self.__display_cfg = v
    @property
    def young_cfg(self):
        return self.__young_cfg
    @young_cfg.setter
    def young_cfg(self,v):
        if self.__young_cfg is not None:
            raise AttributeError
        self.__young_cfg = v

    """
    Ranges
    """
    @property
    def xrange(self):
        xr = self.__xr
        if xr is None:
            xr = linspace(self.x_min,self.x_max,
                    num=self.xres,dtype=int)
            xr.setflags(write=0)
            self.__xr = xr
        return xr
    @property
    def yrange(self):
        yr = self.__yr
        if yr is None:
            yr = linspace(self.y_min,self.y_max,
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
            xr_left = square(self.xrange+self.d).reshape(1,-1)
            xr_right = square(self.xrange-self.d).reshape(1,-1)
            yr = square(self.yrange).reshape(-1,1)
            # xo and yo are ones of same size as xr and yr
            xo = ones(xr_left.shape)
            yo = ones(yr.shape)
            # xs and ys are of size (yres,xres)
            xs_left = yo*xr_left
            xs_right = yo*xr_right
            # del yo,xr_left,xr_right
            ys = yr*xo
            # del xo,yr
            # ps is of size (yres,xres)
            ps_left = sqrt(xs_left+ys)
            # del xs_left
            ps_right = sqrt(xs_right+ys)+self.p
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
            s = 4*square(cos(pi*self.dphase/self.wl))
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
    def projection(self):
        s = self.intensity
        i = array_indexof(self.yrange,self.y)
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
    Interference part needs no initialization
    """
    def __init__(self,**kwargs):
        # Give an ID
        YoungInterference.__id += 1
        self.__id = YoungInterference.__id
        # Child configurations
        ycfg = kwargs.pop('young_cfg',None)
        dcfg = kwargs.pop('display_cfg',None)
        self.young_cfg = ycfg or YoungConfig(**kwargs)
        self.display_cfg = dcfg or DisplayConfig(**kwargs)
        # Subscribe for updates
        # Proxy setup
        self._proxy_children_set(self.young_cfg,self.display_cfg)
        self._freeze()

# log_test(logger)
if __name__=='__main__':
    pass
