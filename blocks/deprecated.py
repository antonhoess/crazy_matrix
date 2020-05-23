from base.block import BlockFixed


class Add2(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 2, 1)

    # end def

    def _calc_values(self):
        self._pin_value[0] = self._conn_in[0].value + self._conn_in[1].value
    # end def
# end class


class Mul2(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 2, 1)

    # end def

    def _calc_values(self):
        self._pin_value[0] = self._conn_in[0].value * self._conn_in[1].value
    # end def
# end class


class Min2(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        self._pin_value[0] = min(self._conn_in[0].value, self._conn_in[1].value)
    # end def
# end class


class Max2(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        self._pin_value[0] = max(self._conn_in[0].value, self._conn_in[1].value)
    # end def
# end class


class And2(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        if self._conn_in[0].value > 0 and self._conn_in[1].value > 0:
            self._pin_value[0] = 1
        else:
            self._pin_value[0] = 0
        # end if
    # end def
# end class


class Or2(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        if self._conn_in[0].value > 0 or self._conn_in[1].value > 0:
            self._pin_value[0] = 1
        else:
            self._pin_value[0] = 0
        # end if
    # end def
# end class


class Eq2(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 2, 1)
    # end def

    def _calc_values(self):
        if self._conn_in[0].value == self._conn_in[1].value:
            self._pin_value[0] = 1
        else:
            self._pin_value[0] = 0
        # end if
    # end def
# end class


# XXX
# auch eine klasse machen, die den wert durchreicht, wenn an einem pin 1 anlieget? oder über mul lösen und als block abspeichern

# class Discr(Block):  # werte diskretisieren zwischen min und max in n stufen (also 4 inputs und 1 output)
#     def __init__(self):
#         Block.__init__(self, 1, 1)
#     # end def
#
#     def _calc_values(self):
#         self._pin_value[0] = np.abs(self._conn_in[0].value)
#     # end def
# # end class
# XXX einen discretizer kann man auch als block bauen.
# eigtl. alles so umbauen, dass alle pixel als matrix auf einmal ausgewrtet werden, dann kann ich auch funktionen machen, die wissen müssen,w as min und max werte aller pixel (bzw. deren an diesem punkt berechneten werte) sind


# XXX variabel gestalten
class Rot1_4(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 4, 4)
    # end def

    def _calc_values(self):
        for i in range(4):
            self._pin_value[i] = self._conn_in[(i+1) % 4].value
        # end for
    # end def
# end class


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
