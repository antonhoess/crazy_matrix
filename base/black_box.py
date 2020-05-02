from __future__ import annotations
from typing import Optional

from base.block import Block, Conn, PassThroughNFix


# XXX müsste man nicht die black box als Block machen und die inputs und outputs (z.b. durch überschreiben der memberfunktionen) umdrehen - aber dafür __input_layer und __output_layer sparen?
class BlackBox(Block):
    def __init__(self, n_in: int, n_out: int, name: Optional[str] = None):
        Block.__init__(self, n_in, n_out, name)  # anstatt diesen konstrktor, besser folgenden aufrufen: FlexibleBlock(self, None, None, name) # und dafür die properties n_in, n_out überschreiben # - evtl.doch eins abstrakte klasse machen, die die schnittstellen für alle alten bon block (inkl. blackbox) vorgibt
        self.__input_layer: PassThroughNFix = PassThroughNFix(n_in)
        self.__output_layer: PassThroughNFix = PassThroughNFix(n_out)
    # end def

    def __str__(self):
        return f"Black Box with {self._n_in} inputs and {self._n_out} outputs."
    # end def

    @property
    def _values_calculated(self) -> bool:
        return self.__output_layer._values_calculated
    # end def

    @_values_calculated.setter
    def _values_calculated(self, value: bool) -> None:
        self.__output_layer._values_calculated = value
    # end def

    def assign_conn_in(self, block: Block, block_pin: int, in_pin: int):
        block.conn_to_prev_block(self.__input_layer, in_pin, block_pin)
    # end def

    def assign_pin_value(self, block: Block, block_pin: int, out_pin: int):
        self.__output_layer.conn_to_prev_block(block, block_pin, out_pin)
    # end def

    def _get_pin_value(self, pin: int) -> float:
        return self.__output_layer._pin_value[pin]
    # end def

    def _get_conn_in(self, pin: int) -> Optional[Conn]:
        return self.__input_layer._conn_in[pin]
    # end def

    def _get_reset_evaluated_propagation_pins(self) -> List[Conn]:
        return self.__output_layer._conn_in
    # end def

    def _set_conn_in(self, pin: int, conn: Conn) -> None:
        self.__input_layer._conn_in[pin] = conn
    # end def

    def _calc_values(self):
        self.__output_layer._calc_values()
    # end def
# end class
