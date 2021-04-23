from .production import *  # noqa E403

try:
    from .local import *  # noqa E403
except ImportError:
    pass
