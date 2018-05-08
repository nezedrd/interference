from matplotlib.pyplot import show
from argparse import ArgumentParser
from logging import getLogger,DEBUG,ERROR
from ..demo import YoungDemo
logger = getLogger(__name__)

def parse_args(argv):
    ap = ArgumentParser(prog=__name__)
    ap.add_argument('-p',default=0,type=int,
            help="Phase delay in nanometers.")
    return ap.parse_args(argv)

def run(argv):
    args = parse_args(argv)
    y = YoungDemo()

    y.p = args.p

    y.figure()
    print(y)
    show()
