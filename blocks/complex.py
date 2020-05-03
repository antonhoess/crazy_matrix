from base.block import BlockFixed


class ComplexAdd(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 4, 2)
    # end def

    def _calc_values(self):
        z1 = complex(self._conn_in[0].value, self._conn_in[1].value)
        z2 = complex(self._conn_in[2].value, self._conn_in[3].value)
        z_res = z1 + z2
        self._pin_value[0] = z_res.real
        self._pin_value[1] = z_res.imag
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


class ComplexMul(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 4, 2)
    # end def

    def _calc_values(self):
        z1 = complex(self._conn_in[0].value, self._conn_in[1].value)
        z2 = complex(self._conn_in[2].value, self._conn_in[3].value)
        z_res = z1 * z2
        self._pin_value[0] = z_res.real
        self._pin_value[1] = z_res.imag
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
