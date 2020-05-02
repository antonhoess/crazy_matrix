from __future__ import annotations
from typing import Optional
import numpy as np

from base.block import FlexibleBlock, Block


class Add2(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)

    # end def

    def _calc_values(self):
        self._pin_value[0] = self._conn_in[0].value + self._conn_in[1].value
    # end def
# end class


class AddN(FlexibleBlock):
    def __init__(self):
        FlexibleBlock.__init__(self, None, 1)
    # end def

    def _calc_values(self):
        accum = 0.
        value_calculated = False

        for conn_in in self._conn_in:
            if conn_in.value is None:
                self._pin_value[0] = None
                return
            # end if
            accum += conn_in.value
            value_calculated = True
        # end for

        self._pin_value[0] = accum if value_calculated else None
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
    def __init__(self, prev_block: Optional[Block] = None):
        Block.__init__(self, 1, 1)

        if prev_block is not None:  # Apply this shortcut to other items as well
            self.conn_to_prev_block(prev_block)
        # end if
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
    def __init__(self, prev_block: Optional[Block] = None):
        Block.__init__(self, 1, 1)

        if prev_block is not None:  # Apply this shortcut to other items as well
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        self._pin_value[0] = np.square(self._conn_in[0].value)
    # end def
# end class


class Sqrt(Block):
    def __init__(self, prev_block: Optional[Block] = None):
        Block.__init__(self, 1, 1)

        if prev_block is not None:  # Apply this shortcut to other items as well
            self.conn_to_prev_block(prev_block)
        # end if
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
