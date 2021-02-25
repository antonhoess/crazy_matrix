from __future__ import annotations
from typing import Optional, Sequence
import numpy as np

from base.block import Block, BlockFixed, IBlock


__author__ = "Anton Höß"
__copyright__ = "Copyright 2021"


class AddN(Block):
    def __init__(self, prev_blocks: Sequence[IBlock] = None, name: Optional[str] = None):
        Block.__init__(self, None, 1, name=name)

        if prev_blocks is not None:
            for b in prev_blocks:
                if b is not None:
                    self.conn_to_prev_block(b)
                # end if
            # end for
        # end if
    # end def

    def _calc_values(self):
        accum = 0.
        value_calculated = False

        for conn_in in self._conn_in:
            if conn_in.value is None:
                self._pin_value[0] = None
                return
            else:
                accum += conn_in.value
                value_calculated = True
            # end if
        # end for

        self._pin_value[0] = accum if value_calculated else None
    # end def
# end class


class Sub2(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, prev_block2: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 2, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if

        if prev_block2 is not None:
            self.conn_to_prev_block(prev_block2)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None and self._conn_in[1].value is not None:
            self._pin_value[0] = self._conn_in[0].value - self._conn_in[1].value
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class MulN(Block):
    #self.desc xxx
    def __init__(self, prev_blocks: Sequence[IBlock] = None, name: Optional[str] = None):
        Block.__init__(self, None, 1, name=name)

        if prev_blocks is not None:
            for b in prev_blocks:
                if b is not None:
                    self.conn_to_prev_block(b)
                # end if
            # end for
        # end if
    # end def

    def _calc_values(self):
        prod = 1.
        value_calculated = False

        for conn_in in self._conn_in:
            if conn_in.value is None:
                self._pin_value[0] = None
                return
            else:
                prod *= conn_in.value
                value_calculated = True
            # end if
        # end for

        self._pin_value[0] = prod if value_calculated else None
    # end def
# end class


class Div2(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, prev_block2: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 2, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if

        if prev_block2 is not None:
            self.conn_to_prev_block(prev_block2)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None and self._conn_in[1].value is not None and self._conn_in[1].value != 0.:
            self._pin_value[0] = self._conn_in[0].value / self._conn_in[1].value
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Abs(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 1, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None:
            self._pin_value[0] = np.abs(self._conn_in[0].value)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Minus(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 1, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None:
            self._pin_value[0] = -self._conn_in[0].value
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Inv(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 1, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None and self._conn_in[0].value != 0:
            self._pin_value[0] = 1 / self._conn_in[0].value
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Mod(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, prev_block2: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 2, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if

        if prev_block2 is not None:
            self.conn_to_prev_block(prev_block2)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None and self._conn_in[1].value is not None and self._conn_in[1].value != 0:
            self._pin_value[0] = self._conn_in[0].value % self._conn_in[1].value
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Exp(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 1, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None:
            self._pin_value[0] = np.exp(self._conn_in[0].value)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Log(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, prev_block2: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 2, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if

        if prev_block2 is not None:
            self.conn_to_prev_block(prev_block2)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None and self._conn_in[1].value is not None and self._conn_in[0].value >= 0 and self._conn_in[0].value != 1 and self._conn_in[1].value > 0:
            self._pin_value[0] = np.log(self._conn_in[1].value) / np.log(self._conn_in[0].value)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Ln(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 1, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None:
            self._pin_value[0] = np.ln(self._conn_in[0].value)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Pow(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, prev_block2: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 2, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if

        if prev_block2 is not None:
            self.conn_to_prev_block(prev_block2)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None and self._conn_in[1].value is not None and self._conn_in[0].value >= 0:
            self._pin_value[0] = np.power(self._conn_in[0].value, self._conn_in[1].value)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Sq(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 1, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None:
            self._pin_value[0] = np.square(self._conn_in[0].value)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Sqrt(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 1, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None and self._conn_in[0].value >= 0:
            self._pin_value[0] = np.sqrt(self._conn_in[0].value)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class MinN(Block):
    def __init__(self, prev_blocks: Sequence[IBlock] = None, name: Optional[str] = None):
        Block.__init__(self, None, 1, name=name)

        if prev_blocks is not None:
            for b in prev_blocks:
                if b is not None:
                    self.conn_to_prev_block(b)
                # end if
            # end for
        # end if
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
    def __init__(self, prev_blocks: Sequence[IBlock] = None, name: Optional[str] = None):
        Block.__init__(self, None, 1, name=name)

        if prev_blocks is not None:
            for b in prev_blocks:
                if b is not None:
                    self.conn_to_prev_block(b)
                # end if
            # end for
        # end if
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
    def __init__(self, prev_block: Optional[IBlock] = None, deg: bool = True, name: Optional[str] = None):
        BlockFixed.__init__(self, 1, 1, name=name)
        self.__deg = deg

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None:
            factor = np.pi / 180 if self.__deg else 1.

            self._pin_value[0] = np.sin(self._conn_in[0].value * factor)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Cos(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, deg: bool = True, name: Optional[str] = None):
        BlockFixed.__init__(self, 1, 1, name=name)
        self.__deg = deg

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None:
            factor = np.pi / 180 if self.__deg else 1.

            self._pin_value[0] = np.cos(self._conn_in[0].value * factor)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Tan(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, deg: bool = True, name: Optional[str] = None):
        BlockFixed.__init__(self, 1, 1, name=name)
        self.__deg = deg

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None:
            factor = np.pi / 180 if self.__deg else 1.

            self._pin_value[0] = np.tan(self._conn_in[0].value * factor)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Atan(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, deg: bool = True, name: Optional[str] = None):
        BlockFixed.__init__(self, 1, 1, name=name)
        self.__deg = deg

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None:
            factor = 180 / np.pi if self.__deg else 1.

            self._pin_value[0] = np.arctan(self._conn_in[0].value) * factor
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Atan2(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, deg: bool = True, name: Optional[str] = None):
        BlockFixed.__init__(self, 2, 1, name=name)
        self.__deg = deg

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None and self._conn_in[1].value is not None:
            factor = 180 / np.pi if self.__deg else 1.

            self._pin_value[0] = np.arctan2(self._conn_in[1].value, self._conn_in[0].value) * factor
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class
