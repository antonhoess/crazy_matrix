from base.block import Block, BlockFixed


__author__ = "Anton Höß"
__copyright__ = "Copyright 2021"


class ComplexAddN(Block):
    def __init__(self):
        Block.__init__(self, None, 2)
    # end def

    def _calc_values(self):
        accum = complex(.0, .0)
        value_calculated = False

        first_input = None

        for conn_in in self._conn_in:
            if conn_in.value is None:
                self._pin_value[0] = None
                self._pin_value[1] = None
                return
            # end if

            if first_input is None:
                first_input = conn_in
                continue

            else:
                accum += complex(first_input.value, conn_in.value)
                first_input = None
                value_calculated = True
            # end if
        # end for

        self._pin_value[0] = accum.real if value_calculated else None
        self._pin_value[1] = accum.imag if value_calculated else None
    # end def
# end class


class ComplexSub(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 4, 2)
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None and self._conn_in[1].value is not None and self._conn_in[2].value is not None and self._conn_in[3].value is not None:
            z1 = complex(self._conn_in[0].value, self._conn_in[1].value)
            z2 = complex(self._conn_in[2].value, self._conn_in[3].value)
            z_res = z1 - z2
            self._pin_value[0] = z_res.real
            self._pin_value[1] = z_res.imag
        else:
            self._pin_value[0] = None
            self._pin_value[1] = None
        # end if
    # end def
# end class


class ComplexMulN(Block):
    def __init__(self):
        Block.__init__(self, None, 2)
    # end def

    def _calc_values(self):
        accum = complex(1., .0)
        value_calculated = False

        first_input = None

        for conn_in in self._conn_in:
            if conn_in.value is None:
                self._pin_value[0] = None
                self._pin_value[1] = None
                return
            # end if

            if first_input is None:
                first_input = conn_in
                continue

            else:
                accum *= complex(first_input.value, conn_in.value)
                first_input = None
                value_calculated = True
            # end if
        # end for

        self._pin_value[0] = accum.real if value_calculated else None
        self._pin_value[1] = accum.imag if value_calculated else None
    # end def
# end class


class ComplexDiv(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 4, 2)
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None and self._conn_in[1].value is not None and self._conn_in[2].value is not None and self._conn_in[3].value is not None \
                and self._conn_in[2].value != 0 and self._conn_in[3].value != 0:
            z1 = complex(self._conn_in[0].value, self._conn_in[1].value)
            z2 = complex(self._conn_in[2].value, self._conn_in[3].value)
            z_res = z1 / z2
            self._pin_value[0] = z_res.real
            self._pin_value[1] = z_res.imag
        else:
            self._pin_value[0] = None
            self._pin_value[1] = None
        # end if
    # end def
# end class
