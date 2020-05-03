from __future__ import annotations
from typing import List, Optional

from base.block import IBlock, IBox, BlockFixed, Conn


class BlackBox(IBlock, IBox):
    class __PassThroughFixed(BlockFixed):
        def __init__(self, n_in_out: int) -> None:
            BlockFixed.__init__(self, n_in_out, n_in_out)
        # end def

        @ property
        def conn_in(self) -> List[Conn]:
            return self._conn_in
        # end def

        def _calc_values(self) -> None:
            for i in range(len(self._pin_value)):
                self._pin_value[i] = self._conn_in[i].value
            # end for
        # end def
    # end class

    def __init__(self, n_in: int, n_out: int, name: Optional[str] = None) -> None:
        self._name = name

        self._values_calculated = False
        self._input_layer: BlackBox.__PassThroughFixed = BlackBox.__PassThroughFixed(n_in)
        self._output_layer: BlackBox.__PassThroughFixed = BlackBox.__PassThroughFixed(n_out)
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

    def assign_conn_in(self, block: BlockFixed, block_pin: int, in_pin: int) -> bool:
        return block.conn_to_prev_block(self._input_layer, in_pin, block_pin)
    # end def

    def assign_pin_value(self, block: BlockFixed, block_pin: int, out_pin: int) -> bool:
        return self._output_layer.conn_to_prev_block(block, block_pin, out_pin)
    # end def

    def add_conn_to_prev_block(self, prev_block: BlockFixed, prev_pin: Optional[int] = None) -> None:
        return self._input_layer.add_conn_to_prev_block(prev_block, prev_pin)
    # end def

    def conn_to_prev_block(self, prev_block: BlockFixed, prev_pin: Optional[int] = None, in_pin: Optional[int] = None) -> bool:
        return self._input_layer.conn_to_prev_block(prev_block, prev_pin, in_pin)
    # end def

    def value(self, pin: Optional[int] = None) -> float:
        return self._output_layer.value(pin)
    # end def

    def reset_evaluated(self) -> None:
        self._output_layer.reset_evaluated()
    # end def
# end class
