from logging import basicConfig,getLogger,DEBUG,INFO,WARNING,ERROR,CRITICAL
basicConfig(level=DEBUG)

import os,argparse
from .tools import log_test
from importlib import import_module
logger = getLogger(__name__)

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('module')
    return ap.parse_args()

def main():
    argv = parse_args()
    # m = import_module('.'+argv.module,package=__file__.split(os.path.sep)[-2])
    m = import_module('.demos.'+argv.module,package=__file__.split(os.path.sep)[-2])
    logger.info("Finished import. Starting.")
    m.run()

if __name__=='__main__':
    logger = getLogger(__file__.split(os.path.sep)[-2])
    main()
