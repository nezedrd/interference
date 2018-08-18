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
    ap.add_argument('-i',metavar='filename',dest='input',
            default=None,
            help="Input yaml or json file.")
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
    get_quality = {
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
    # SET DEFAULT CONFIGURATION INCLUDING STEPS
    figsize=(16,9)
    fps=15
    resolution = args.res

    movie_title = "Interference Video"
    movie_artist = "nezedrd"
    movie_comment = "void"

    steps = [
        {
        "var": "wl",
        "sec": 10,
        "end": 532
        },
        {
        "var": "d",
        "sec": 20,
        "end": 5
        },
        {
        "var": "y",
        "end": 3.5
        },
        {
        "sec": 5,
        "end": 20
        },
        {
        "var": "p",
        "sec": 20,
        "end": 620
        },
        {
        "var": "wl",
        "end": 680
        },
        {
        "sec": 40,
        "end": 400
        }
    ]

    # GET EVERY CONFIGURATION VALUE
    if args.input is not None:
        pass

    # CREATE CONFIGURATIONS AND SET INITIAL VALUES
    quality = get_quality[resolution]
    dpi = quality['dpi']
    alpha = quality['alpha']

    dc = DisplayConfig()
    dc.res /= alpha
    yc = YoungConfig()

    # CREATE DEMO
    y = YoungDemo(display_cfg=dc,young_cfg=yc)
    print(y)

    # CONFIGURE AND CREATE FIGURE
    y.figure_config(figsize=figsize,dpi=dpi)
    fig = y.figure()

    # CREATE GETTERS AND SETTERS
    def seconds(s):
        return int(s*fps)
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
    getters = {
            'd': d_getter,
            'y': y_getter,
            'p': p_getter,
            'wl': wl_getter,
            }
    setters = {
            'd': d_setter,
            'y': y_setter,
            'p': p_setter,
            'wl': wl_setter,
            }

    # CREATE FFMPEG WRITER
    FFMpegWriter = writers['ffmpeg']
    metadata = {
            'title': movie_title,
            'artist': movie_artist,
            'comment': movie_comment,
        }
    writer = FFMpegWriter(fps=fps, metadata=metadata)

    # START WRITING
    if args.display:
        ion()
        show()

    s0 = steps[0]
    if 'var' not in s0 or 'sec' not in s0 or 'end' not in s0:
        logger.critical("First step should be completely set up.")
        raise KeyError
    s0['nframes'] = seconds(s0['sec'])
    for i in range(1,len(steps)):
        t = steps[i-1]
        s = steps[i]
        s['var'] = s.get('var',t['var'])
        if s['var'] not in getters:
            logger.critical("Variable should be among {:}.".format(getters.keys()))
            raise KeyError(s['var'])
        s['sec'] = s.get('sec',t['sec'])
        if s['sec'] <= 0:
            logger.critical("Seconds should be positive.")
            raise ValueError(s['sec'])
        s['end'] = s.get('end',t['end'])
        s['nframes'] = seconds(s['sec'])
    nframes = sum([ s['nframes'] for s in steps ])

    with writer.saving(fig,args.output,dpi):
        with ProgressBar(max_value=nframes) as bar:
            bar.start()
            i = 0
            for step in steps:
                var = step['var']
                getter = getters[var]
                setter = setters[var]
                end = step['end']
                num = step['nframes']
                vrange = slow_range(getter(),end,num=num)
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
