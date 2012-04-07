try:
    from .currentenv import *
except ImportError:
    import sys
    msg = ("Error importing settings/currentenv.py. Did you forget to symlink "
           "your local settings?\n")
    sys.stderr.write(msg)

    import traceback
    sys.stderr.write(traceback.format_exc())
