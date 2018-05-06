from matplotlib.pyplot import show
from argparse import ArgumentParser
from logging import getLogger
from ..demo import YoungDemo
logger = getLogger(__name__)

def parse_args(argv):
    ap = ArgumentParser(prog=__name__)
    return ap.parse_args(argv)

def run(argv):
    args = parse_args(argv)
    y = YoungDemo()
    y.figure()
    print(y)
    show()
