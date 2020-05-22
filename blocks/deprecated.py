from __future__ import annotations
from typing import Optional

from base.block import BlockFixed
from base.block import Conn


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
class SquareXn(BlockFixed):
    def __init__(self, prev_block: Optional[BlockFixed], prev_pin: Optional[int] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 2, 1, name)
        self.__cnt = 0
        self.__n_rep = 0
        self.__inited = False

        if prev_block is not None:  # Apply this shortcut to other items as well
            self.conn_to_prev_block(prev_block, prev_pin)
        # end if
    # end def

    def _calc_values(self):
        if not self.__inited:
            self.__n_rep = int(self._conn_in[1].value) - 1
            self.__inited = True
        # end if

        if self.__cnt < self.__n_rep:
            self.__cnt += 1
            x = Conn(self, 0).value  # This recursively triggers _calc_values()
        else:
            self.__cnt = 0
            self.__inited = False
            x = self._conn_in[0].value
        # end if

        #self._pin_value[0] = (x * x) % 217  # XXX Just some calculation for debugging purposes
        self._pin_value[0] = (x * x) % 217  # XXX Just some calculation for debugging purposes
    # end def
# end class

# # XXX
# class SquareXn(BlockFixed):
#     def __init__(self, prev_block: Optional[BlockFixed], prev_pin: Optional[int] = None, name: Optional[str] = None):
#         BlockFixed.__init__(self, 2, 1, name)
#         #self.__n_rep = 1
#         self.__cnt = 0
#         #self.__inited = False
#
#         if prev_block is not None:  # Apply this shortcut to other items as well
#             self.conn_to_prev_block(prev_block, prev_pin)
#         # end if
#     # end def
#
#     def _calc_values(self):
#         # if not self.__inited:
#         #     self.__inited = True
#         #     #self._pin_value[0] = self._conn_in[0].value  # Initial value
#         #     self.__n_rep = int(self._conn_in[1].value)
#         #     #self.__recursive_active = True
#         # # end if
#
#         if self.__cnt < int(self._conn_in[1].value) - 1:  # self.__n_rep:
#             self.__cnt += 1
#             x = Conn(self, 0).value  # This recursively triggers _calc_values()
#         else:
#             self.__cnt = 0
#             x = self._conn_in[0].value
#         # end if
#
#         self._pin_value[0] = (x * x) % 217  # XXX Just some calculation for debugging purposes
#
#         # # Repeat the operation N times by using for the input the output of the previous call
#         # if self.__recursive_active:
#         #     if self.__cnt < self.__n_rep:
#         #         self.__cnt += 1
#         #         self._pin_value[0] = np.square(Conn(self, 0).value)  # This recursively triggers _calc_values()
#         #     else:
#         #         self.__recursive_active = False
#         #     # end if
#         # else:
#         #     if self.__cnt > 0:
#         #         self.__cnt -= 1
#         #         #self._pin_value[0] = np.square(Conn(self, 0).value)  # This recursively triggers _calc_values()
#         #     else:
#         #         self.__recursive_active = True
#         #         self.__inited = False
#         #     # end if
#         # # end if
#     # end def
#
#     # def reset_evaluated(self) -> None:
#     #     BlockFixed.reset_evaluated()
#     #     self.__inited = False
#     # # end def
# # end class

# # XXX
# class SquareXn(BlockFixed):
#     def __init__(self, prev_block: Optional[BlockFixed] = None, name: Optional[str] = None):
#         BlockFixed.__init__(self, 2, 1, name)
#         self.__n_rep = 3
#         self.__cnt = 0
#         self.__inited = False
#
#         if prev_block is not None:  # Apply this shortcut to other items as well
#             self.conn_to_prev_block(prev_block)
#         # end if
#     # end def
#
#     def _calc_values(self):
#         if not self.__inited:
#             self.__inited = True
#             self._pin_value[0] = self._conn_in[0].value  # Initial value
#             self.__n_rep = int(self._conn_in[1].value)
#             self.__recursive_active = True
#         # end if
#
#         # Repeat the operation N times by using for the input the output of the previous call
#         if self.__recursive_active:
#             if self.__cnt < self.__n_rep:
#                 self.__cnt += 1
#                 self._pin_value[0] = np.square(Conn(self, 0).value)  # This recursively triggers _calc_values()
#             else:
#                 self.__recursive_active = False
#             # end if
#         else:
#             if self.__cnt > 0:
#                 self.__cnt -= 1
#                 #self._pin_value[0] = np.square(Conn(self, 0).value)  # This recursively triggers _calc_values()
#             else:
#                 self.__recursive_active = True
#                 self.__inited = False
#             # end if
#         # end if
#     # end def
#
#     # def reset_evaluated(self) -> None:
#     #     BlockFixed.reset_evaluated()
#     #     self.__inited = False
#     # # end def
# # end class


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
