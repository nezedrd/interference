from matplotlib.pyplot import show
from argparse import ArgumentParser
from logging import getLogger,DEBUG,ERROR
from ..demo import YoungDemo,logger as dlg
from ..config import logger as clg
from ..tools import logger as tlg
logger = getLogger(__name__)

def parse_args(argv):
    ap = ArgumentParser(prog=__name__)
    ap.add_argument('-p',default=0,type=int,
            help="Phase delay in nanometers.")
    return ap.parse_args(argv)

def run(argv):
    args = parse_args(argv)
    y = YoungDemo()

    # tlg.setLevel(DEBUG)
    # logger.setLevel(DEBUG)

    # logger.debug((y.p,y.normal.young_cfg.p))
    y.p = args.p
    # logger.debug((y.p,y.normal.young_cfg.p))

    # logger.setLevel(ERROR)
    # tlg.setLevel(ERROR)

    dlg.setLevel(DEBUG)
    # clg.setLevel(DEBUG)
    # tlg.setLevel(DEBUG)

    y.figure()
    print(y)
    show()
