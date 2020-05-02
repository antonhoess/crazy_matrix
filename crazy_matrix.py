import matplotlib.pyplot as plt
import numpy as np

from base.basic import Circuit


class CrazyMatrix:
    def __init__(self, circuit: Circuit):
        self.__w = 400
        self.__h = 200
        self.__v_min = 0
        self.__v_max = None
        self.__circuit = circuit
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

    def plot(self):
        offset_x = int(-self.__w / 2)
        offset_y = int(-self.__h / 2)
        scale = 1. / 50

        z = np.empty((self.__w, self.__h))

        for _x in range(self.__w):
            for _y in range(self.__h):
                x = _x + offset_x
                y = _y + offset_y
                z[_x, _y] = self.__circuit.eval(x, y)
                #z[_x, _y] = self.mandelbrot(x * scale, y * scale)
            # end for
        # end for

        fig, ax = plt.subplots()
        cmap = "RdYlGn"
        cmap = "Greys"
        im = ax.imshow(np.transpose(z), interpolation="nearest", cmap=cmap, origin='lower', extent=[-self.__w / 2, self.__w / 2, -self.__h / 2, self.__h / 2])#, vmax=0)#, vmax=np.abs(Z).max(), vmin=-np.abs(Z).max())  # interpolation="bilinear"
        ax.set_aspect("equal")

        plt.show()
    # end def
# end class
