from argparse import ArgumentParser
from logging import getLogger,INFO
from ..config import YoungConfig,DisplayConfig
from ..demo import YoungDemo
from ..tools import unit_identify
logger = getLogger(__name__)

def parse_args(argv,helps=dict()):
    ap = ArgumentParser(prog=__name__)
    ap.add_argument('-b',metavar='filename',dest='before_output',
            default='before.png',
            help="Output for the before file.")
    ap.add_argument('-a',metavar='filename',dest='after_output',
            default='after.png',
            help="Output for the after file.")
    ap.add_argument('-p',
            default=None,
            type=float,
            help=helps.get('p',''))
    ap.add_argument('-d',
            default=None,
            type=float,
            help=helps.get('d',''))
    ap.add_argument('-y',
            default=None,
            type=float,
            help=helps.get('y',''))
    ap.add_argument('-w',
            default=None,
            type=float,
            help=helps.get('w',''))
    return ap.parse_args(argv)

def run(argv):
    yc = YoungConfig()
    dc = DisplayConfig()
    helps = dict()
    y = YoungDemo(young_cfg=yc,display_cfg=dc)
    y.figure_config(figsize=(16,9),dpi=120.00)

    helps['w'] = y.wl_slider.label.get_text()
    helps['p'] = y.p_slider.label.get_text()
    helps['d'] = y.d_slider.label.get_text()
    helps['y'] = y.y_slider.label.get_text()
    args = parse_args(argv,helps)

    fig = y.figure()
    fig.savefig(args.before_output)
    lvl = logger.level

    logger.setLevel(INFO)
    logger.info("savefig:{:}".format(args.before_output))
    logger.setLevel(lvl)

    if args.p is not None:
        y.p_slider.set_val(args.p)
    if args.d is not None:
        y.d_slider.set_val(args.d)
    if args.y is not None:
        y.y_slider.set_val(args.y)
    if args.w is not None:
        y.wl_slider.set_val(args.w)

    fig.savefig(args.after_output)
    logger.setLevel(INFO)
    logger.info("savefig:{:}".format(args.after_output))
    logger.setLevel(lvl)
