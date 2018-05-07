from numpy import array,argmin
from functools import reduce
from matplotlib.pyplot import get_cmap
from matplotlib.colors import LinearSegmentedColormap
from numpy import linspace,array,ones
from logging import getLogger,ERROR,DEBUG
logger = getLogger(__name__)
logger.setLevel(ERROR)

"""
Test logger
"""
def log_test(l):
    print("PRINT:{:}:Will test debug,info,warning,error,critical.".format(l.name))
    l.debug("Test of debug")
    l.info("Test of info")
    l.warning("Test of warning")
    l.error("Test of error")
    l.critical("Test of critical")
    print("PRINT:{:}:Tested debug,info,warning,error,critical.".format(l.name))

"""
DefaultObject
"""
class DefaultObject(object):
    def __getattr__(self,name):
        if name[0] == '_':
            return None
        raise AttributeError(name)

"""
ProxyObject
"""
class ProxyObject(object):
    def __getattr__(self,key):
        lgid = "ProxyObject:__getattr__:{:}:{:}".format(repr(self),key)
        logger.debug(lgid)
        if key[0] == '_':
            logger.debug(lgid+":Returning None")
            return None
        logger.debug(lgid+":Looking at children")
        for o in self.__proxy_children:
            try:
                logger.debug(lgid+":Delegating to {:}".format(repr(o)))
                return getattr(o,key)
            except AttributeError:
                logger.debug(lgid+":Delegation to {:} failed".format(repr(o)))
        raise AttributeError(key)
    def __setattr__(self,key,val):
        logger.debug("ProxyObject:__setattr__:{:}:{:}:{:}".format(repr(self),key,val))
        if not self.__frozen or key[0] == '_' or key in self.__dict__:
            object.__setattr__(self,key,val)
            return
        for o in self.__proxy_children:
            if hasattr(o,key):
                o.__setattr__(key,val)
                return
        raise AttributeError(key)
    def _freeze(self):
        logger.debug("ProxyObject:_freeze:{:}".format(repr(self)))
        self.__frozen = 1
    def _proxy_children_set(self,*args):
        logger.debug("ProxyObject:_proxy_children_set:{:}:{:}".format(repr(self),list(args)))
        self.__proxy_children = list(args)

"""
UpdateObject
"""
class UpdateObject(DefaultObject):
    def register(self,call,*args):
        calls = self.__notify_calls
        if calls is None:
            calls = dict()
            self.__notify_calls = calls
        for t in args:
            call_list = calls.get(t,set())
            call_list.add(call)
            calls[t] = call_list
    def unregister(self,call,*args):
        calls = self.__notify_calls
        if calls is None:
            return
        for t in args:
            calls.get(t,set()).discard(call)
    def notify(self,*args,**kwargs):
        calls = self.__notify_calls
        kwargs['who'] = kwargs.get('who',self)
        if calls is None:
            return
        to_call = dict() # object: list_of_reasons
        if not args:     # just notify everybody without reason
            for ct,tc in calls.items():
                to_call = { k: [] for k in tc }
        else:
            for t in args:
                for o in calls.get(t,set()):
                    to_call[o] = to_call.get(o,list())
                    to_call[o].append(t)
            for o in calls.get('*',set()):
                to_call[o] = to_call.get(o,list())
        for o,reasons in to_call.items():
            o.update(*reasons,**kwargs)
    def update(self,*args,**kwargs):
        logger.debug("update:types {:}:args {:}".format(args,kwargs))
        raise NotImplementedError
class EchoUpdateObject(UpdateObject):
    def __init__(self,name):
        self.__name = name
    def update(self,*args,**kwargs):
        print("HELLO:{:}:{:}:{:}".format(self.__name,args,kwargs))
def test_updateobject():
    a = EchoUpdateObject("architect")
    w = EchoUpdateObject("worker")
    b = EchoUpdateObject("bank")
    a.register(w.update,'plan')
    a.register(b.update,'budget')
    w.register(a.update,'delays')
    w.register(a.update,'delays')
    w.register(a.update,'delays')
    w.register(a.update,'delays')
    w.register(b.update,'delays')
    a.notify('plan',"Plans changed, workers should know.")
    a.notify('budget',"Budget changed, bank should know.")
    w.notify('delays',"Workers are late, architect and bank should know.")
    w.unregister(a.update,'delays')
    w.notify('delays',"Workers are late, architect does not care anymore.")

"""
Unit formater
"""
__verb_units = { 1: 'nm', 1e3: 'μm', 1e6: 'mm', 1e7: 'cm' }
def unit_format(*args,fs='{:4d}'):
    steps = __verb_units.keys()
    a = array(args,dtype=int)
    for c in reversed(sorted(steps)):
        x = a/c
        y = x.astype(int)
        if (y == x).all():
            f = fs+__verb_units[c]
            ret = [ f.format(Y) for Y in y ]
            return (*ret,)
    return None

"""
Numpy approximate index of
"""
def array_indexof(array,value):
    return argmin(abs(array-value))

"""
Arguments for extent
"""
def parse_funcargs(**kwargs):
    keys = kwargs['keys']
    deft = kwargs.get('defaults',dict())
    args = kwargs['args']
    dest = kwargs.get('dest',dict())
    for k,v in keys.items():
        dest[k] = reduce(
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
    return parse_funcargs(keys=a,defaults=d,args=kwargs,dest=e)

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
Get wavelength cmap
"""
__wavelength_spectre = get_cmap('nipy_spectral')
__cmap_res = 2
def wavelength_to_color(wl):
    w = max(0,min(wl,700))
    l = (w-400.)/300.
    return __wavelength_spectre(l)
def color_to_cmap(color):
    color = [color]*__cmap_res
    smooth = linspace(0.,1.,__cmap_res)
    smooth = array([smooth,smooth,smooth,ones(__cmap_res,dtype=float)]).transpose()
    colors = color*smooth
    return LinearSegmentedColormap.from_list('colormap',colors)

# log_test(logger)
if __name__=='__main__':
    logger.setLevel(DEBUG)
    test_updateobject()
