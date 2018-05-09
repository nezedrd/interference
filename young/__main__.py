from logging import basicConfig,getLogger,DEBUG,INFO,WARNING,ERROR,CRITICAL
basicConfig(level=ERROR)
DBG_LEVELS = [ CRITICAL,ERROR,WARNING,INFO,DEBUG ]
DBG_DEFAULT = 2
def get_dbg_level(i):
    real_i = max(0,min(i+DBG_DEFAULT,len(DBG_LEVELS)-1))
    return DBG_LEVELS[real_i]

from os.path import sep
from argparse import ArgumentParser,REMAINDER
from importlib import import_module

from .demo import logger as dlog
from .tools import logger as tlog
from .interference import logger as ilog
from .config import logger as clog

if __name__=='__main__':
    prog_name = __file__.split(sep)[-2]
else:
    prog_name = __name__
logger = getLogger(prog_name)


def parse_args():
    ap = ArgumentParser(prog=prog_name)
    ap.add_argument('-v',dest='verb',action='count',default=0)
    ap.add_argument('--tools-verb',dest='tools_verb',type=int,default=-1)
    ap.add_argument('--interference-verb',dest='interference_verb',type=int,default=-1)
    ap.add_argument('--config-verb',dest='config_verb',type=int,default=-1)
    ap.add_argument('--demo-verb',dest='demo_verb',type=int,default=-1)
    ap.add_argument('module',metavar='demo_name',
            help="Name of the demo in the demos/ folder.")
    ap.add_argument('remainder',nargs=REMAINDER,default=list(),
            help="Everything that should be passed to the demo.")
    return ap.parse_args()

def set_verb(argv):
    for l in [logger,dlog,tlog,ilog,clog]:
        l.setLevel(get_dbg_level(argv.verb))
    if argv.tools_verb >= 0:
        tlog.setLevel(get_dbg_level(argv.tools_verb))
    if argv.interference_verb >= 0:
        ilog.setLevel(get_dbg_level(argv.interference_verb))
    if argv.config_verb >= 0:
        clog.setLevel(get_dbg_level(argv.config_verb))
    if argv.demo_verb >= 0:
        clog.setLevel(get_dbg_level(argv.demo_verb))

def main():
    argv = parse_args()
    set_verb(argv)
    m = import_module('.demos.'+argv.module,package=prog_name)
    m.logger.setLevel(DBG_LEVELS[argv.verb])
    logger.info("Finished import. Starting.")
    m.run(argv.remainder)

if __name__=='__main__':
    main()
