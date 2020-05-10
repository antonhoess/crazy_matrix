from base.block import Block, BlockFixed


class ComplexAddN(Block):
    def __init__(self):
        Block.__init__(self, None, 1)
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
        z1 = complex(self._conn_in[0].value, self._conn_in[1].value)
        z2 = complex(self._conn_in[2].value, self._conn_in[3].value)
        z_res = z1 - z2
        self._pin_value[0] = z_res.real
        self._pin_value[1] = z_res.imag
    # end def
# end class


class ComplexMulN(Block):
    def __init__(self):
        Block.__init__(self, None, 1)
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
        z1 = complex(self._conn_in[0].value, self._conn_in[1].value)
        z2 = complex(self._conn_in[2].value, self._conn_in[3].value)
        z_res = z1 / z2  # XXX abprüfung rein? wie schaut diese aus? wie verhält sich die complex class in diesem falle? in literatur schauen, wann div0 bei komplexen Zahlen auftritt
        self._pin_value[0] = z_res.real
        self._pin_value[1] = z_res.imag
    # end def
# end class
