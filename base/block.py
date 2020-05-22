from __future__ import annotations
from typing import List, Optional
from abc import ABC, abstractmethod


class IBlock(ABC):
    @property
    @abstractmethod
    def n_in(self) -> int:
        raise NotImplementedError
    # end def

    @property
    @abstractmethod
    def n_out(self) -> int:
        raise NotImplementedError
    # end def

    @abstractmethod
    def add_conn_to_prev_block(self, prev_block: BlockFixed, prev_pin: Optional[int] = None) -> None:
        raise NotImplementedError
    # end def

    @abstractmethod
    def conn_to_prev_block(self, prev_block: BlockFixed, prev_pin: Optional[int] = None, in_pin: Optional[int] = None) -> bool:
        raise NotImplementedError
    # end def

    @abstractmethod
    def value(self, pin: Optional[int] = None) -> float:
        raise NotImplementedError
    # end def

    @abstractmethod
    def reset_evaluated(self) -> None:
        raise NotImplementedError
    # end def
# end class


class IBox(ABC):
    @abstractmethod
    def assign_conn_in(self, block: BlockFixed, block_pin: int, in_pin: int) -> bool:
        raise NotImplementedError
    # end def

    @abstractmethod
    def assign_pin_value(self, block: BlockFixed, block_pin: int, out_pin: int) -> bool:
        raise NotImplementedError
    # end def
# end class


class Block(IBlock):
    def __init__(self, n_in: Optional[int], n_out: Optional[int], name: Optional[str] = None) -> None:
        self._pin_value: List[Optional[float]] = []
        self._conn_in: List[Optional[Conn]] = []

        # Connection from previous block into this one
        if n_in is not None:
            self._n_in_fixed = True
            self._n_in = n_in

            for i in range(self._n_in):
                self._conn_in.append(None)
            # end for
        else:
            self._n_in_fixed = False
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

        self._name = name
        self._values_calculated = False
    # end def

    def __str__(self) -> str:
        return f"Block with {self._n_in} inputs and {self._n_out} outputs."
    # end def

    @property
    def n_in(self) -> int:
        return self._n_in
    # end def

    @property
    def n_out(self) -> int:
        return self._n_out
    # end def

    def add_conn_to_prev_block(self, prev_block: IBlock, prev_pin: Optional[int] = None) -> bool:
        self._conn_in.append(None)
        self._n_in += 1
        return self.conn_to_prev_block(prev_block, prev_pin, len(self._conn_in) - 1)
    # end def

    def conn_to_prev_block(self, prev_block: IBlock, prev_pin: Optional[int] = None, in_pin: Optional[int] = None) -> bool:
        if prev_pin is None:
            prev_pin = 0

        if in_pin is None:
            if self._n_in_fixed:
                in_pin = 0
            else:
                in_pin = self.n_in
                self._conn_in.append(None)
                self._n_in += 1
            # end if
        # end if

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

    def value(self, pin: Optional[int] = None) -> float:
        if pin is None:
            pin = 0

        value = None  # stattdessen besser eine exception machen?`Und/oder einen checker, der prüft, ob alle connections gesetzt sind, so dass keine fehler passieren können? Was ist mit div0 und anderen Fehlern?

        if 0 <= pin < self._n_out:
            if not self._values_calculated:
                self._calc_values()
                self._values_calculated = True  # Das klappt nicht mehr so einfach bei einer BlackBox
            # end if

            value = self._pin_value[pin]
        # end if

        return value
    # end def

    def reset_evaluated(self) -> None:
        self._values_calculated = False

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

    @abstractmethod
    def _calc_values(self) -> None:
        raise NotImplementedError
    # end def
# end class


class BlockFixed(Block):
    def __init__(self, n_in: int, n_out: int, name: Optional[str] = None):
        Block.__init__(self, n_in, n_out, name)
    # end def

    @abstractmethod
    def _calc_values(self) -> None:
        raise NotImplementedError
    # end def
# end class


class Conn:
    def __init__(self, in_block: IBlock, in_pin: int):
        self.__in_block: IBlock = in_block
        self.__in_pin: int = in_pin
    # end def

    @property
    def in_block(self) -> IBlock:
        return self.__in_block
    # end def

    @property
    def value(self) -> float:
        return self.__in_block.value(self.__in_pin)
    # end def
# end class
