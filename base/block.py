from __future__ import annotations
from typing import List, Optional
from abc import abstractmethod


class FlexibleBlock:
    def __init__(self, n_in: Optional[int], n_out: Optional[int], name: Optional[str] = None):
        self._pin_value: List[Optional[float]] = []
        self._conn_in: List[Optional[Conn]] = []

        # Connection from previous block into this one
        if n_in is not None:
            self.__n_in_fixed = True
            self._n_in = n_in

            for i in range(self._n_in):
                self._conn_in.append(None)
            # end for
        else:
            self.__n_in_fixed = False
            self._n_in = 0
        # end if

        # Output values provided to the next block
        if n_out is not None:
            self.__n_out_fixed = True
            self._n_out = n_out

            for i in range(self._n_out):
                self._pin_value.append(None)  # None = not yet evaluated
            # end for
        else:
            self.__n_out_fixed = False
            self._n_out = 0
        # end if

        self.__name = name
        self.__values_calculated = False
    # end def

    def __str__(self):
        return f"Block with {self._n_in} inputs and {self._n_out} outputs."
    # end def

    @property
    def _values_calculated(self) -> bool:
        return self.__values_calculated
    # end def

    @_values_calculated.setter
    def _values_calculated(self, value: bool) -> None:
        self.__values_calculated = value
    # end def

    def _add_empty_conn_in(self):
        self._conn_in.append(None)
        self._n_in += 1
    # end def

    def _add_empty_pin_value(self):
        self._pin_value.append(None)
        self._n_out += 1
    # end def

    def add_conn_to_prev_block(self, prev_block: Block, prev_pin: Optional[int] = None):
        self._add_empty_conn_in()
        self.conn_to_prev_block(prev_block, prev_pin, len(self._conn_in) - 1)
    # end def

    def _get_conn_in(self, pin: int) -> Optional[Conn]:
        return self._conn_in[pin]
    # end def

    def _get_reset_evaluated_propagation_pins(self) -> List[Conn]:
        return self._conn_in
    # end def

    def _set_conn_in(self, pin: int, conn: Conn) -> None:
        self._conn_in[pin] = conn
    # end def

    def conn_to_prev_block(self, prev_block: Block, prev_pin: Optional[int] = None, in_pin: Optional[int] = None):  # XXX diese def in Block?
        if prev_pin is None:
            prev_pin = 0

        if in_pin is None:
            in_pin = 0

        if 0 <= prev_pin < prev_block.n_out and 0 <= in_pin < self.n_in:
            conn: Conn = Conn(prev_block, prev_pin)
            if self._get_conn_in(in_pin):
                print(f"Overwriting in pin {in_pin}")
            self._set_conn_in(in_pin, conn)
            return True
        else:
            return False
        # end if
    # end def

    @property
    def n_in(self):
        return self._n_in
    # end def

    @property
    def n_out(self):
        return self._n_out
    # end def

    @abstractmethod
    def _calc_values(self):
        pass
    # end def

    def _get_pin_value(self, pin: int) -> float:
        return self._pin_value[pin]
    # end def

    def value(self, pin: Optional[int] = None) -> float:
        if pin is None:
            pin = 0

        value = None  # stattdessen besser eine exception machen?`Und/oder einen checker, der prüft, ob alle connections gesetzt sind, so dass keine fehler passieren können? Was ist mit div0 und anderen Fehlern?

        if 0 <= pin < self._n_out:
            if not self._values_calculated:
                self._calc_values()
                self._values_calculated = True  # Das klappt nicht mehr so einfach bei einer BlackBox
            # end if

            value = self._get_pin_value(pin)
        # end if

        return value
    # end def

    def reset_evaluated(self):
        self._values_calculated = False

        blocks = []

        for conn in self._get_reset_evaluated_propagation_pins():
            if conn is not None and conn.in_block not in blocks:
                blocks.append(conn.in_block)
            # end if
        # end for

        for block in blocks:
            block.reset_evaluated()
        # end for
    # end def
# end class


class Block(FlexibleBlock):
    def __init__(self, n_in: int, n_out: int, name: Optional[str] = None):
        FlexibleBlock.__init__(self, n_in, n_out, name)
    # end def

    @abstractmethod
    def _calc_values(self):
        FlexibleBlock._calc_values(self)
    # end def
# end class


class PassThroughN(FlexibleBlock):
    def __init__(self):
        FlexibleBlock.__init__(self, None, None)
    # end def

    def _calc_values(self):
        for i in range(len(self._pin_value)):
            self._pin_value[i] = self._conn_in[i].value
        # end for
    # end def
# end class


class PassThroughNFix(Block):
    def __init__(self, n_in_out: int):
        Block.__init__(self, n_in_out, n_in_out)
    # end def

    def _calc_values(self):
        for i in range(len(self._pin_value)):
            self._pin_value[i] = self._conn_in[i].value
        # end for
    # end def
# end class


class Conn:
    def __init__(self, in_block: Block, in_pin: int):
        self.__in_block: Block = in_block
        self.__in_pin: int = in_pin
    # end def

    @property
    def in_block(self):
        return self.__in_block
    # end def

    @property
    def value(self) -> float:
        return self.__in_block.value(self.__in_pin)
    # end def
# end class
