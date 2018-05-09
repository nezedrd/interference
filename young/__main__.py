from logging import basicConfig,getLogger,DEBUG,INFO,WARNING,ERROR,CRITICAL
basicConfig(level=ERROR)
DBG_LEVELS = [ CRITICAL,ERROR,WARNING,INFO,DEBUG ]
DBG_VLEVELS= [ "CRITICAL","ERROR","WARNING","INFO","DEBUG" ]
DBG_DEFAULT = 2
def get_dbg_level(i,verb=0):
    real_i = max(0,min(i+DBG_DEFAULT,len(DBG_LEVELS)-1))
    if verb:
        return DBG_LEVELS[real_i],DBG_VLEVELS[real_i]
    return DBG_LEVELS[real_i]

from os.path import sep
from argparse import ArgumentParser,REMAINDER
from importlib import import_module
from pkgutil import iter_modules

from .demo import logger as dlog
from .tools import logger as tlog
from .interference import logger as ilog
from .config import logger as clog

prog_path_components = __file__.split(sep)
if __name__=='__main__':
    prog_name = prog_path_components[-2]
else:
    prog_name = __name__
logger = getLogger(prog_name)


def parse_args(demos):
    ap = ArgumentParser(prog=prog_name)
    ap.add_argument('-v',dest='verb',action='count',default=0)
    ap.add_argument('--tools-verb',dest='tools_verb',type=int,default=-1)
    ap.add_argument('--interference-verb',dest='interference_verb',type=int,default=-1)
    ap.add_argument('--config-verb',dest='config_verb',type=int,default=-1)
    ap.add_argument('--demo-verb',dest='demo_verb',type=int,default=-1)
    ap.add_argument('module',metavar='demo_name',choices=list(demos),
            help="Name of the demo among {:}".format(list(demos)))
    ap.add_argument('remainder',nargs=REMAINDER,default=list(),
            help="Everything that should be passed to the demo.")
    args = ap.parse_args()
    return args

def set_verb(argv):
    lvl,vlvl = get_dbg_level(argv.verb,verb=1)
    logger.setLevel(lvl)
    logger.info("VERB_LEVEL:{:}".format(vlvl))
    for l in [dlog,tlog,ilog,clog]:
        l.setLevel(lvl)
    if argv.tools_verb >= 0:
        lvl,vlvl = get_dbg_level(argv.tools_verb,verb=1)
        logger.info("TOOLS_VERB_LEVEL:{:}".format(vlvl))
        tlog.setLevel(lvl)
    if argv.interference_verb >= 0:
        lvl,vlvl = get_dbg_level(argv.interference_verb,verb=1)
        logger.info("INTERFERENCE_VERB_LEVEL:{:}".format(vlvl))
        ilog.setLevel(lvl)
    if argv.config_verb >= 0:
        lvl,vlvl = get_dbg_level(argv.config_verb,verb=1)
        logger.info("CONFIG_VERB_LEVEL:{:}".format(vlvl))
        clog.setLevel(lvl)
    if argv.demo_verb >= 0:
        lvl,vlvl = get_dbg_level(argv.demo_verb,verb=1)
        logger.info("DEMO_VERB_LEVEL:{:}".format(vlvl))
        clog.setLevel(lvl)

def get_demos():
    subfolder = 'demos'
    modules_folder = sep.join(prog_path_components[:-1]+[subfolder])
    res = dict()
    for _,name,_ in iter_modules([modules_folder]):
        res[name] = '.'.join(['',subfolder,name])
    return res

def main():
    demos = get_demos()
    argv = parse_args(demos)
    set_verb(argv)
    m = import_module(demos[argv.module],package=prog_name)
    m.logger.setLevel(get_dbg_level(argv.verb))
    logger.info("IMPORT:finished")
    m.run(argv.remainder)

if __name__=='__main__':
    main()
