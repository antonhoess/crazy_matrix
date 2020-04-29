from base.block import Block


class And2(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        if self._conn_in[0].value > 0 and self._conn_in[1].value > 0:
            self._pin_value[0] = 1
        else:
            self._pin_value[0] = 0
        # end if
    # end def
# end class


class Or2(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        if self._conn_in[0].value > 0 or self._conn_in[1].value > 0:
            self._pin_value[0] = 1
        else:
            self._pin_value[0] = 0
        # end if
    # end def
# end class


class Not1(Block):
    def __init__(self):
        Block.__init__(self, 1, 1)
    # end def

    def _calc_values(self):
        if self._conn_in[0].value == 0:
            self._pin_value[0] = 1
        else:
            self._pin_value[0] = 0
        # end if
    # end def
# end class


class Gt(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        if self._conn_in[0].value > self._conn_in[1].value:
            self._pin_value[0] = 1
        else:
            self._pin_value[0] = 0
        # end if
    # end def
# end class


class Lt(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        if self._conn_in[0].value < self._conn_in[1].value:
            self._pin_value[0] = 1
        else:
            self._pin_value[0] = 0
        # end if
    # end def
# end class


class Eq2(Block):
    def __init__(self):
        Block.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        if self._conn_in[0].value == self._conn_in[1].value:
            self._pin_value[0] = 1
        else:
            self._pin_value[0] = 0
        # end if
    # end def
# end class
