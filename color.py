from collections import namedtuple


RGB = namedtuple('RGB', ['R', 'G', 'B'])


class COLOR:
    RED = RGB(255, 0, 0)
    GREEN = RGB(0, 255, 0)
    BLUE = RGB(0, 0, 255)
    YELLOW = RGB(255, 255, 0)
    CYAN = RGB(0, 255, 255)
    MAGENTA = RGB(255, 0, 255)
    WHITE = RGB(255, 255, 255)
    OFF = RGB(0, 0, 0)
