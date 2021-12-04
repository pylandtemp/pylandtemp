from collections import namedtuple

from .algorithms.mono_window import MonoWindowLST
from .algorithms.split_window.algorithms import (
    SplitWindowJiminezMunozLST,
    SplitWindowKerrLST,
    SplitWindowMcMillinLST,
    SplitWindowPriceLST,
    SplitWindowSobrino1993LST,
)


single_window = {"mono-window": MonoWindowLST}

split_window = {
    "jiminez-munoz": SplitWindowJiminezMunozLST,
    "kerr": SplitWindowKerrLST,
    "mc-millin": SplitWindowMcMillinLST,
    "price": SplitWindowPriceLST,
    "sobrino-1993": SplitWindowSobrino1993LST,
}
Algorithms = namedtuple("Algorithms", ("single_window", "split_window"))

default_algorithms = Algorithms(single_window, split_window)
