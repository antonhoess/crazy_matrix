from __future__ import annotations
from typing import List, Optional

from base.block import IBlock, IBox, BlockFixed, Conn


class _PassThroughFixed(BlockFixed):
    def __init__(self, n_in_out: int) -> None:
        BlockFixed.__init__(self, n_in_out, n_in_out)

    # end def

    @property
    def conn_in(self) -> List[Conn]:
        return self._conn_in

    # end def

    def _calc_values(self) -> None:
        for i in range(len(self._pin_value)):
            self._pin_value[i] = self._conn_in[i].value
        # end for
    # end def
# end class


class _PassThroughFixedRepeat(BlockFixed):
    # Note: n_in_out gives the number of inputs and outputs, but the inputs are 1 more, since the last one is the input for the number of repetitions
    def __init__(self, n_in_out: int, partner_block: BlockFixed) -> None:
        BlockFixed.__init__(self, n_in_out + 1, n_in_out)
        self.__cnt = 0
        self.__n_rep = 0
        self.__recursion_active = False
        self.__partner_block: BlockFixed = partner_block
    # end def

    @property
    def conn_in(self) -> List[Conn]:
        return self._conn_in
    # end def

    def _calc_values(self) -> None:
        if not self.__recursion_active:
            self.__n_rep = int(self._conn_in[self.n_in - 1].value) - 1
            self.__recursion_active = True
        # end if

        x = list()
        if self.__cnt < self.__n_rep:
            self.__cnt += 1

            for pin in range(self.n_out):
                x.append(Conn(self.__partner_block, pin).value)  # This recursively triggers _calc_values()
            # end for
            self.__partner_block.reset_evaluated()

        else:
            self.__cnt = 0
            self.__recursion_active = False
            for pin in range(self.n_out):
                x.append(self._conn_in[pin].value)
            # end for
        # end if

        for pin in range(self.n_out):
            self._pin_value[pin] = x[pin]
        # end for
    # end def

    def reset_evaluated(self) -> None:
        if not self.__recursion_active:
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
        # end if
    # end def
# end class


class BlackBox(IBlock, IBox):
    def __init__(self, n_in: int, n_out: int, name: Optional[str] = None) -> None:
        self._name = name
        self._input_layer: _PassThroughFixed = _PassThroughFixed(n_in)
        self._output_layer: _PassThroughFixed = _PassThroughFixed(n_out)
    # end def

    def __str__(self) -> str:
        return f"Black Box with {self.n_in} inputs and {self.n_out} outputs."
    # end def

    @property
    def n_in(self) -> int:
        return self._input_layer.n_in
    # end def

    @property
    def n_out(self) -> int:
        return self._output_layer.n_out
    # end def

    def assign_conn_in(self, block: IBlock, block_pin: int, in_pin: int) -> bool:
        return block.conn_to_prev_block(self._input_layer, in_pin, block_pin)
    # end def

    def assign_pin_value(self, block: IBlock, block_pin: int, out_pin: int) -> bool:
        return self._output_layer.conn_to_prev_block(block, block_pin, out_pin)
    # end def

    def conn_to_prev_block(self, prev_block: IBlock, prev_pin: Optional[int] = None, in_pin: Optional[int] = None) -> bool:
        return self._input_layer.conn_to_prev_block(prev_block, prev_pin, in_pin)
    # end def

    def value(self, pin: Optional[int] = None) -> float:
        return self._output_layer.value(pin)
    # end def

    def reset_evaluated(self) -> None:
        self._output_layer.reset_evaluated()
    # end def
# end class


class RepeatBox(BlackBox):
    def __init__(self, n_in_out: int, name: Optional[str] = None) -> None:
        BlackBox.__init__(self, n_in_out, n_in_out, name)
        self._input_layer: _PassThroughFixedRepeat = _PassThroughFixedRepeat(n_in_out, self._output_layer)
    # end def

    def __str__(self) -> str:
        return f"Repeat Box with {self.n_in} inputs and {self.n_out} outputs."
    # end def
# end class
