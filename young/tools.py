from numpy import array,argmin
from functools import reduce
from logging import getLogger
logger = getLogger(__name__)

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
        return None

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

# log_test(logger)
if __name__=='__main__':
    pass
