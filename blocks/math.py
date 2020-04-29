import numpy as np

from base.block import Block


class Add2(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)

    # end def

    def _calc_values(self):
        self._pin_value[0] = self._conn_in[0].value + self._conn_in[1].value
    # end def
# end class


class Sub2(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)

    # end def

    def _calc_values(self):
        self._pin_value[0] = self._conn_in[0].value - self._conn_in[1].value
    # end def
# end class


class Mul2(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)

    # end def

    def _calc_values(self):
        self._pin_value[0] = self._conn_in[0].value * self._conn_in[1].value
    # end def
# end class


class Div2(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)

    # end def

    def _calc_values(self):
        if self._conn_in[1].value != 0.:
            self._pin_value[0] = self._conn_in[0].value / self._conn_in[1].value
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Abs(Block):
    def __init__(self):
        Block.__init__(self, 1, 1)
    # end def

    def _calc_values(self):
        self._pin_value[0] = np.abs(self._conn_in[0].value)
    # end def
# end class


class Minus(Block):
    def __init__(self):
        Block.__init__(self, 1, 1)
    # end def

    def _calc_values(self):
        self._pin_value[0] = -self._conn_in[0].value
    # end def
# end class


class Mod(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        self._pin_value[0] = self._conn_in[0].value % self._conn_in[1].value
    # end def
# end class


class Square(Block):
    def __init__(self):
        Block.__init__(self, 1, 1)
    # end def

    def _calc_values(self):
        self._pin_value[0] = np.square(self._conn_in[0].value)
    # end def
# end class


class Sqrt(Block):
    def __init__(self):
        Block.__init__(self, 1, 1)
    # end def

    def _calc_values(self):
        if self._conn_in[0].value >= 0:
            self._pin_value[0] = np.sqrt(self._conn_in[0].value)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Min2(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        self._pin_value[0] = min(self._conn_in[0].value, self._conn_in[1].value)
    # end def
# end class


class Max2(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        self._pin_value[0] = max(self._conn_in[0].value, self._conn_in[1].value)
    # end def
# end class


class Sin(Block):
    def __init__(self, deg: bool = True):
        Block.__init__(self, 1, 1)
        self.__deg = deg
    # end def

    def _calc_values(self):
        factor = 1.

        if self.__deg:
            factor = np.pi / 180.

        self._pin_value[0] = np.sin(self._conn_in[0].value * factor)
    # end def
# end class


class Cos(Block):
    def __init__(self, deg: bool = True):
        Block.__init__(self, 1, 1)
        self.__deg = deg
    # end def

    def _calc_values(self):
        factor = 1.

        if self.__deg:
            factor = np.pi / 180.

        self._pin_value[0] = np.cos(self._conn_in[0].value * factor)
    # end def
# end class
