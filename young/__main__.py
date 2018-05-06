from logging import basicConfig,getLogger,DEBUG,INFO,WARNING,ERROR,CRITICAL
basicConfig(level=DEBUG)

from os.path import sep
from argparse import ArgumentParser,REMAINDER
from .tools import log_test
from importlib import import_module

if __name__=='__main__':
    prog_name = __file__.split(sep)[-2]
else:
    prog_name = __name__
logger = getLogger(prog_name)


def parse_args():
    ap = ArgumentParser(prog=prog_name)
    ap.add_argument('module',metavar='demo_name',
            help="Name of the demo in the demos/ folder.")
    ap.add_argument('remainder',nargs=REMAINDER,default=list(),
            help="Everything that should be passed to the demo.")
    return ap.parse_args()

def main():
    argv = parse_args()
    m = import_module('.demos.'+argv.module,package=prog_name)
    logger.info("Finished import. Starting.")
    m.run(argv.remainder)

if __name__=='__main__':
    main()
