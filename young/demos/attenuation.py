from matplotlib.pyplot import show
from argparse import ArgumentParser
from logging import getLogger,DEBUG,ERROR
from ..attenuation import YoungAttenuatedInterference
from ..demo import YoungDemo
logger = getLogger(__name__)

def parse_args(argv):
    ap = ArgumentParser(prog=__name__)
    ap.add_argument('-R',default=960,type=float,
            help="Attenuation (air is 960).")
    return ap.parse_args(argv)

def run(argv):
    args = parse_args(argv)
    y = YoungDemo(young_if_class=YoungAttenuatedInterference)

    y.R = args.R

    y.figure()
    print(y)
    show()
