from __future__ import annotations
from typing import Optional

from base.block import Block


class Const(Block):
    def __init__(self, value: float):
        Block.__init__(self, 0, 1)
        self._pin_value[0] = value
    # end def

    def __str__(self):
        return f"Const with a value of {self._pin_value[0]}. Has no inputs."
    # end def

    def _calc_values(self):
        pass
    # end def
# end class


class ConstPi(Const):
    def __init__(self):
        Const.__init__(self, float(np.pi))
    # end def
# end class


class ConstE(Const):
    def __init__(self):
        Const.__init__(self, float(np.e))
    # end def
# end class


class ConstUser(Const):
    def __init__(self, value: float):
        Const.__init__(self, value)
    # end def
# end class


class Variable(Block):
    def __init__(self, value: Optional[float] = None):
        Block.__init__(self, 1, 1)
        self._pin_value[0] = value
    # end def

    # @property
    # def value(self) -> float:
    #     return self._pin_value[0]
    # # end def

    def set_value(self, value: float):
        self._pin_value[0] = value
    # end def

    def _calc_values(self):
        if self._conn_in[0] is not None:
            self._pin_value[0] = self._conn_in[0].value
        # end if
    # end def
# end class
