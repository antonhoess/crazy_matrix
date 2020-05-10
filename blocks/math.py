from __future__ import annotations
from typing import Optional
import numpy as np

from base.block import Block, BlockFixed


class AddN(Block):
    def __init__(self):
        Block.__init__(self, None, 1)
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


class Sub2(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 2, 1)

    # end def

    def _calc_values(self):
        self._pin_value[0] = self._conn_in[0].value - self._conn_in[1].value
    # end def
# end class


class MulN(Block):
    def __init__(self):
        Block.__init__(self, None, 1)
    # end def

    def _calc_values(self):
        prod = 1.
        value_calculated = False

        for conn_in in self._conn_in:
            if conn_in.value is None:
                self._pin_value[0] = None
                return
            # end if
            prod *= conn_in.value
            value_calculated = True
        # end for

        self._pin_value[0] = prod if value_calculated else None
    # end def
# end class


class Div2(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 2, 1)

    # end def

    def _calc_values(self):
        if self._conn_in[1].value != 0.:
            self._pin_value[0] = self._conn_in[0].value / self._conn_in[1].value
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Abs(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 1, 1)
    # end def

    def _calc_values(self):
        self._pin_value[0] = np.abs(self._conn_in[0].value)
    # end def
# end class


class Minus(BlockFixed):
    def __init__(self, prev_block: Optional[BlockFixed] = None):
        BlockFixed.__init__(self, 1, 1)

        if prev_block is not None:  # Apply this shortcut to other items as well
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        self._pin_value[0] = -self._conn_in[0].value
    # end def
# end class


class Mod(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        self._pin_value[0] = self._conn_in[0].value % self._conn_in[1].value
    # end def
# end class


class Square(BlockFixed):
    def __init__(self, prev_block: Optional[BlockFixed] = None):
        BlockFixed.__init__(self, 1, 1)

        if prev_block is not None:  # Apply this shortcut to other items as well
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        self._pin_value[0] = np.square(self._conn_in[0].value)
    # end def
# end class


class Sqrt(BlockFixed):
    def __init__(self, prev_block: Optional[BlockFixed] = None):
        BlockFixed.__init__(self, 1, 1)

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


class MinN(Block):
    def __init__(self):
        Block.__init__(self, None, 1)
    # end def

    def _calc_values(self):
        value = None
        value_calculated = False

        for conn_in in self._conn_in:
            if conn_in.value is None:
                self._pin_value[0] = None
                return
            # end if

            if not value_calculated:
                value = conn_in.value
            else:
                value = min(value, conn_in.value)
            # end if

            value_calculated = True
        # end for

        self._pin_value[0] = value if value_calculated else None
    # end def
# end class


class MaxN(Block):
    def __init__(self):
        Block.__init__(self, None, 1)

    # end def

    def _calc_values(self):
        value = None
        value_calculated = False

        for conn_in in self._conn_in:
            if conn_in.value is None:
                self._pin_value[0] = None
                return
            # end if

            if not value_calculated:
                value = conn_in.value
            else:
                value = max(value, conn_in.value)
            # end if

            value_calculated = True
        # end for

        self._pin_value[0] = value if value_calculated else None
    # end def
# end class


class Sin(BlockFixed):
    def __init__(self, deg: bool = True):
        BlockFixed.__init__(self, 1, 1)
        self.__deg = deg
    # end def

    def _calc_values(self):
        factor = 1.

        if self.__deg:
            factor = np.pi / 180.

        self._pin_value[0] = np.sin(self._conn_in[0].value * factor)
    # end def
# end class


class Cos(BlockFixed):
    def __init__(self, deg: bool = True):
        BlockFixed.__init__(self, 1, 1)
        self.__deg = deg
    # end def

    def _calc_values(self):
        factor = 1.

        if self.__deg:
            factor = np.pi / 180.

        self._pin_value[0] = np.cos(self._conn_in[0].value * factor)
    # end def
# end class


class Tan(BlockFixed):
    def __init__(self, deg: bool = True):
        BlockFixed.__init__(self, 1, 1)
        self.__deg = deg
    # end def

    def _calc_values(self):
        factor = 1.

        if self.__deg:
            factor = np.pi / 180.

        self._pin_value[0] = np.tan(self._conn_in[0].value * factor)
    # end def
# end class
