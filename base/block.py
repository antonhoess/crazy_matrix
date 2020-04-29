from __future__ import annotations
from typing import List, Optional
from abc import abstractmethod


class Block:
    def __init__(self, n_in: int, n_out: int, name: Optional[str] = None):
        self.__name = name
        self._n_in = n_in
        self._n_out = n_out
        self._pin_value: List[Optional[float]] = [None] * n_out  # None = not yet evaluated
        self._conn_in: List[Optional[Conn]] = [None] * n_in
        self.__values_calculated = False
    # end def

    def __str__(self):
        return f"Block with {self._n_in} inputs and {self._n_out} outputs."
    # end def

    def conn_to_prev_block(self, prev_block: Block, prev_pin: Optional[int] = None, in_pin: Optional[int] = None):
        if prev_pin is None:
            prev_pin = 0

        if in_pin is None:
            in_pin = 0

        if 0 <= prev_pin < prev_block.n_out and 0 <= in_pin < self.n_in:
            conn: Conn = Conn(prev_block, prev_pin)
            if self._conn_in[in_pin]:
                print(f"Overwriting in pin {in_pin}")
            self._conn_in[in_pin] = conn
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

    def value(self, pin: Optional[int] = None) -> float:
        if pin is None:
            pin = 0

        value = None  # stattdessen besser eine exception machen?`Und/oder einen checker, der prüft, ob alle connections gesetzt sind, so dass keine fehler passieren können? Was ist mit div0 und anderen Fehlern?

        if 0 <= pin < self._n_out:
            if not self.__values_calculated:
                self._calc_values()
                self.__values_calculated = True
            # end if

            value = self._pin_value[pin]
        # end if

        return value
    # end def

    def reset_evaluated(self):
        self.__values_calculated = False

        blocks = []
        for conn in self._conn_in:
            if conn is not None and conn.in_block not in blocks:
                blocks.append(conn.in_block)
            # end if
        # end for

        for block in blocks:
            block.reset_evaluated()
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
