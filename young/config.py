from .tools import UpdateObject,unit_format
from logging import getLogger
logger = getLogger(__name__)

"""
Experiment configuration
"""
class YoungConfig(UpdateObject):
    __id = 0
    ATTRIBUTES = ['wl_min','wl_max','wl',\
            'd_min','d_max','d','p_min','p_max','p',\
            'R']
    DEFAULT = {
            'wl_min': 400, 'wl_max': 700, 'wl': 532,
            'd_min': 0, 'd_max': 20e3, 'd': 10e3,
            'p_min': -700, 'p_max': 700, 'p': 0,
            'R': 960, # value in air and nanometers: R=0.96*1e30*λ^4/m^3
        }

    """
    Parameters:
    * physical
      * wavelength, wavelength range
      * intersource, intersource range
     (* screen position)
      * phase delay, range
    """
    # Wavelength
    @property
    def wl_min(self):
        self.__debug("get:wl_min")
        return self.__wlm
    @wl_min.setter
    def wl_min(self,v):
        self.__debug("set:wl_min:{:}",v)
        self.__wlm = int(max(350,v))
    @property
    def wl_max(self):
        self.__debug("get:wl_max")
        return self.__wlM
    @wl_max.setter
    def wl_max(self,v):
        self.__debug("set:wl_max:{:}",v)
        self.__wlM = int(min(v,750))
    @property
    def wl(self):
        self.__debug("get:wl")
        return self.__wl
    @wl.setter
    def wl(self,v):
        self.__debug("set:wl:{:}",v)
        self.__wl = int(max(self.wl_min,min(v,self.wl_max)))
        self.notify('wl')

    # Intersource distance
    @property
    def d_min(self):
        self.__debug("get:d_min")
        return self.__dm
    @d_min.setter
    def d_min(self,v):
        self.__debug("set:d_min:{:}",v)
        self.__dm = int(max(0,v))
    @property
    def d_max(self):
        self.__debug("get:d_max")
        return self.__dM
    @d_max.setter
    def d_max(self,v):
        self.__debug("set:d_max:{:}",v)
        self.__dM = int(v)
    @property
    def d(self):
        self.__debug("get:d")
        return self.__d
    @d.setter
    def d(self,v):
        self.__debug("set:d:{:}",v)
        self.__d = int(max(self.d_min,min(v,self.d_max)))
        self.notify('d')

    # Phase delay
    @property
    def p_min(self):
        self.__debug("get:p_min")
        return self.__pm
    @p_min.setter
    def p_min(self,v):
        self.__debug("set:p_min:{:}",v)
        self.__pm = int(v)
    @property
    def p_max(self):
        self.__debug("get:p_max")
        return self.__pM
    @p_max.setter
    def p_max(self,v):
        self.__debug("set:p_max:{:}",v)
        self.__pM = int(v)
    @property
    def p(self):
        self.__debug("get:p")
        return self.__p
    @p.setter
    def p(self,v):
        self.__debug("set:p:{:}",v)
        self.__p = int(max(self.p_min,min(v,self.p_max)))
        self.notify('p')

    @property
    def R(self):
        self.__debug("get:R")
        return (self.__wl)**4 * (self.__R)
    @R.setter
    def R(self,v):
        self.__debug("set:R:{:}",v)
        self.__R = v

    """
    Initialize configuration
    """
    def __init__(self,**kwargs):
        # Give an ID
        YoungConfig.__id += 1
        self.__id = YoungConfig.__id
        # Build config
        config = YoungConfig.DEFAULT.copy()
        config.update(kwargs)
        # Settings
        for key in YoungConfig.ATTRIBUTES:
            setattr(self,key,config[key])
    def copy(self):
        config = dict()
        for key in YoungConfig.ATTRIBUTES:
            config[key] = getattr(self,key)
        return YoungConfig(**config)

    """
    To string
    """
    def __repr__(self):
        return "YoungConfig{:d}".format(self.__id)
    def __str__(self):
        res = [repr(self)]
        wlm,wl,wlM, = unit_format(self.wl_min,self.wl,self.wl_max)
        res.append("  λ: {:} --- {:} --> {:}".format(wlm,wl,wlM))
        dm, d, dM,  = unit_format(self.d_min, self.d, self.d_max )
        res.append("  d: {:} --- {:} --> {:}".format(dm, d, dM ))
        pm, p, pM,  = unit_format(self.p_min, self.p, self.p_max )
        res.append("  p: {:} --- {:} --> {:}".format(pm, p, pM ))
        return '\n'.join(res)

    def __debug(self,msg,*args,**kwargs):
        logger.debug("YoungConfig[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __info(self,msg,*args,**kwargs):
        logger.info("YoungConfig[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __warning(self,msg,*args,**kwargs):
        logger.warning("YoungConfig[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __error(self,msg,*args,**kwargs):
        logger.error("YoungConfig[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __critical(self,msg,*args,**kwargs):
        logger.critical("YoungConfig[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))

"""
Graphical configuration
"""
class DisplayConfig(UpdateObject):
    __id = 0
    ATTRIBUTES = ['x_min','x_max','x','x_ratio',\
            'y_min','y_max','y','y_screen','res']
    DEFAULT = {
            'x_min': -20e7, 'x_max': 20e7, 'x': 0, 'x_ratio': 4,
            'y_min': 0, 'y_max': 30e7, 'y': 30e7, 'y_screen': 1e7,
            'res': 2048, # Number of pixels for the whole width
        }

    """
    Parameters:
    * graphical
      * left, right, bottom, top bounds
      * resolution
    """
    # Graphical bounds
    @property
    def x_min(self):
        self.__debug("get:x_min")
        return self.__xm
    @x_min.setter
    def x_min(self,v):
        self.__debug("set:x_min:{:}",v)
        self.__xm = int(v)
    @property
    def x_max(self):
        self.__debug("get:x_max")
        return self.__xM
    @x_max.setter
    def x_max(self,v):
        self.__debug("set:x_max:{:}",v)
        self.__xM = int(v)
    @property
    def x(self):
        self.__debug("get:x")
        return self.__x
    @x.setter
    def x(self,v):
        self.__debug("set:x:{:}",v)
        self.__x = int(max(self.x_min,min(v,self.x_max)))
    @property
    def x_ratio(self):
        self.__debug("get:x_ratio")
        return self.__xr
    @x_ratio.setter
    def x_ratio(self,v):
        self.__debug("set:x_ratio:{:}",v)
        self.__xr = int(max(1,v))
    @property
    def y_min(self):
        self.__debug("get:y_min")
        return self.__ym
    @y_min.setter
    def y_min(self,v):
        self.__debug("set:y_min:{:}",v)
        self.__ym = int(v)
    @property
    def y_max(self):
        self.__debug("get:y_max")
        return self.__yM
    @y_max.setter
    def y_max(self,v):
        self.__debug("set:y_max:{:}",v)
        self.__yM = int(v)
    @property
    def y(self):
        self.__debug("get:y")
        return self.__y
    @y.setter
    def y(self,v):
        self.__debug("set:y:{:}",v)
        self.__y = int(max(self.y_min,min(v,self.y_max)))
        self.notify('y')
    @property
    def y_screen(self):
        self.__debug("get:y_screen")
        return self.__ys
    @y_screen.setter
    def y_screen(self,v):
        self.__debug("set:y_screen:{:}",v)
        self.__ys = int(max(1,v))

    # Resolution
    @property
    def res(self):
        self.__debug("get:res")
        return self.__r
    @res.setter
    def res(self,v):
        self.__debug("set:res:{:}",v)
        self.__r = int(max(0,v))
    @property
    def xres(self):
        self.__debug("get:xres")
        return self.res
    @property
    def yres(self):
        self.__debug("get:yres")
        Δy = self.y_max - self.y_min
        Δx = self.x_max - self.x_min
        ρx = self.xres
        return int(ρx*Δy/Δx)

    """
    Initialize configuration
    """
    def __init__(self,**kwargs):
        # Give an ID
        DisplayConfig.__id += 1
        self.__id = DisplayConfig.__id
        # Build config
        config = DisplayConfig.DEFAULT.copy()
        config.update(kwargs)
        # Settings
        for key in DisplayConfig.ATTRIBUTES:
            setattr(self,key,config[key])
    def copy(self):
        config = dict()
        for key in DisplayConfig.ATTRIBUTES:
            config[key] = getattr(self,key)
        return DisplayConfig(**config)

    """
    To string
    """
    def __repr__(self):
        return "DisplayConfig{:d}".format(self.__id)
    def __str__(self):
        res = [repr(self)]
        xm, xM,     = unit_format(self.x_min, self.x_max)
        res.append("  x: [ {:}, {:} ] {:d}px".format(xm,xM,self.xres))
        ym, yM,     = unit_format(self.y_min, self.y_max)
        res.append("  y: [ {:}, {:} ] {:d}px".format(ym,yM,self.yres))
        return '\n'.join(res)

    def __debug(self,msg,*args,**kwargs):
        logger.debug("DisplayConfig[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __info(self,msg,*args,**kwargs):
        logger.info("DisplayConfig[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __warning(self,msg,*args,**kwargs):
        logger.warning("DisplayConfig[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __error(self,msg,*args,**kwargs):
        logger.error("DisplayConfig[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))
    def __critical(self,msg,*args,**kwargs):
        logger.critical("DisplayConfig[{:}]:{:}"\
                .format(repr(self),msg.format(*args,**kwargs)))

if __name__ == '__main__':
    yc = YoungConfig()
    print(yc)
    print("====")
    dc = DisplayConfig()
    print(dc)
