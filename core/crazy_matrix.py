from __future__ import annotations
from typing import Optional
import matplotlib.pyplot as plt
import numpy as np

from base.basic import Circuit


__author__ = "Anton Höß"
__copyright__ = "Copyright 2021"


class CrazyMatrix:
    def __init__(self, circuit: Circuit, width: int, height: int, cmap: Optional[str] = None):
        self.__w: int = width
        self.__h: int = height
        self.__v_min = 0
        self.__v_max = None
        self.__circuit = circuit
        self.__circuit.set_size(self.__w, self.__h)
        self.__cmap = cmap if cmap is not None else "Greys"  # "RdYlGn"
    # end def

    @staticmethod  # XXX
    def mandelbrot(x, y):
        c0 = complex(x, y)
        c = 0

        for i in range(1, 10):
            if abs(c) > 2:
                return i
            c = c * c + c0
        # end for

        return 0
    # end def

    def calc_image(self) -> np.ndarray:
        offset_x = int(-self.__w / 2)
        offset_y = int(-self.__h / 2)
        scale = 1. / 50

        z = np.empty((self.__w, self.__h))

        for _x in range(self.__w):
            for _y in range(self.__h):
                x = _x + offset_x
                y = _y + offset_y
                z[_x, _y] = self.__circuit.eval(x, y)
                # z[_x, _y] = self.mandelbrot(x * scale, y * scale)
            # end for
        # end for

        z = z.transpose()

        return z
    # end def
# end class
