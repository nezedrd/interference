from argparse import ArgumentParser
from logging import getLogger,INFO
from ..config import DisplayConfig,YoungConfig
from ..demo import YoungDemo
from numpy import linspace,cos,pi
from matplotlib.animation import writers
from progressbar import ProgressBar
from matplotlib.pyplot import show,ion,pause,draw
logger = getLogger(__name__)

def parse_args(argv):
    ap = ArgumentParser(prog=__name__)
    ap.add_argument('-o',metavar='filename',dest='output',
            default='output.mp4',
            help="Output file.")
    ap.add_argument('-q',metavar='quality',dest='res',
            choices=['lld','ld','sd','hd','hhd'], default='lld',
            help="Video quality.")
    ap.add_argument('-d','--display',dest='display',
            action='store_true',default=False,
            help="Display while recording.")
    return ap.parse_args(argv)

def run(argv):
    args = parse_args(argv)

    # 1920*1080: (19.2,10.8), alpha=1
    # 1280* 720: (12.8,7.20), alpha=2/3
    #  960* 540: (9.60,5.40), alpha=1/2
    params = {
            'hhd': {
                'figsize': (19.2,10.8),
                'dpi': 120.00,
                'alpha': 1,
                },
            'hd': {
                'figsize': (16.0,9.00),
                'dpi': 100.00,
                'alpha': 1.2,
                },
            'sd': {
                'figsize': (12.8,7.20),
                'dpi': 80.00,
                'alpha': 1.5,
                },
            'ld': {
                'figsize': (9.60,5.40),
                'dpi': 60.00,
                'alpha': 2,
                },
            'lld': {
                'figsize': (6.40,3.60),
                'dpi': 40.00,
                'alpha': 3,
                },
            }
    fps=15
    # figsize=params[args.res]['figsize']
    figsize=(16,9)
    dpi=params[args.res]['dpi']
    alpha=params[args.res]['alpha']

    def seconds(s):
        return int(s*fps)

    dc = DisplayConfig()
    dc.res /= alpha

    yc = YoungConfig()
    yc.wl = 400

    y = YoungDemo(display_cfg=dc,young_cfg=yc)
    print(y)

    y.figure_config(figsize=figsize,dpi=dpi)

    fig = y.figure()

    def slow_range(start,stop,num):
        r = cos(linspace(0,pi,num=num))
        return (stop-start)*((1-r)/2)+start

    def d_getter():
        return y.d_slider.val
    def d_setter(x):
        y.d_slider.set_val(x)

    def y_getter():
        return y.y_slider.val
    def y_setter(x):
        y.y_slider.set_val(x)

    def p_getter():
        return y.p_slider.val
    def p_setter(x):
        y.p_slider.set_val(x)

    def wl_getter():
        return y.wl_slider.val
    def wl_setter(x):
        y.wl_slider.set_val(x)

    steps = list()
    steps.append({
        'nframes': seconds(10.),
        'getter': wl_getter,
        'to': 532,
        'setter': wl_setter,
        })
    steps.append({
        'nframes': seconds(20.),
        'getter': d_getter,
        'to': 5,
        'setter': d_setter,
        })
    steps.append({
        'nframes': seconds(20.),
        'getter': y_getter,
        'to': 3.5,
        'setter': y_setter,
        })
    steps.append({
        'nframes': seconds(5.),
        'getter': y_getter,
        'to': 20,
        'setter': y_setter,
        })
    steps.append({
        'nframes': seconds(20.),
        'getter': p_getter,
        'to': 620,
        'setter': p_setter,
        })
    steps.append({
        'nframes': seconds(20.),
        'getter': wl_getter,
        'to': 680,
        'setter': wl_setter,
        })
    steps.append({
        'nframes': seconds(40.),
        'getter': wl_getter,
        'to': y.wl_slider.valmin,
        'setter': wl_setter,
        })

    nframes = sum([ s['nframes'] for s in steps ])

    FFMpegWriter = writers['ffmpeg']
    metadata = {
            'title': 'Young Interference - Animation',
            'artist': 'Clement',
        }
    writer = FFMpegWriter(fps=fps, metadata=metadata)

    fig.savefig(args.output+'.png')

    if args.display:
        ion()
        show()
    with writer.saving(fig,args.output,dpi):
        with ProgressBar(max_value=nframes) as bar:
            bar.start()
            i = 0
            for step in steps:
                vrange = slow_range(step['getter'](),step['to'],num=step['nframes'])
                setter = step['setter']
                for x in vrange:
                    setter(x)
                    writer.grab_frame()
                    if args.display:
                        draw()
                        pause(.0001)
                    i+=1; bar.update(i)

    lvl = logger.level
    logger.setLevel(INFO)
    logger.info("saved video:{:}".format(args.output))
    logger.setLevel(lvl)
