from typing import Optional, Sequence

from base.block import BlockFixed, Block, IBlock


class AndN(Block):
    def __init__(self, prev_blocks: Sequence[IBlock] = None, name: Optional[str] = None):
        Block.__init__(self, None, 1, name=name)

        if prev_blocks is not None:
            for b in prev_blocks:
                if b is not None:
                    self.conn_to_prev_block(b)
                # end if
            # end for
        # end if
    # end def

    def _calc_values(self):
        value = True
        value_calculated = False

        for conn_in in self._conn_in:
            if conn_in.value is None:
                self._pin_value[0] = None
                return
            else:
                value = value and conn_in.value
                value_calculated = True
            # end if
        # end for

        self._pin_value[0] = int(value) if value_calculated else None
    # end def
# end class


class OrN(Block):
    def __init__(self, prev_blocks: Sequence[IBlock] = None, name: Optional[str] = None):
        Block.__init__(self, None, 1, name=name)

        if prev_blocks is not None:
            for b in prev_blocks:
                if b is not None:
                    self.conn_to_prev_block(b)
                # end if
            # end for
        # end if
    # end def

    def _calc_values(self):
        value = False
        value_calculated = False

        for conn_in in self._conn_in:
            if conn_in.value is None:
                self._pin_value[0] = None
                return
            else:
                value = value or conn_in.value
                value_calculated = True
            # end if
        # end for

        self._pin_value[0] = int(value) if value_calculated else None
    # end def
# end class


class Not(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 1, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None:
            self._pin_value[0] = int(not self._conn_in[0].value)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Gt(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, prev_block2: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 2, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if

        if prev_block2 is not None:
            self.conn_to_prev_block(prev_block2)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None:
            self._pin_value[0] = int(self._conn_in[0].value > self._conn_in[1].value)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class Lt(BlockFixed):
    def __init__(self, prev_block: Optional[IBlock] = None, prev_block2: Optional[IBlock] = None, name: Optional[str] = None):
        BlockFixed.__init__(self, 2, 1, name=name)

        if prev_block is not None:
            self.conn_to_prev_block(prev_block)
        # end if

        if prev_block2 is not None:
            self.conn_to_prev_block(prev_block2)
        # end if
    # end def

    def _calc_values(self):
        if self._conn_in[0].value is not None:
            self._pin_value[0] = int(self._conn_in[0].value < self._conn_in[1].value)
        else:
            self._pin_value[0] = None
        # end if
    # end def
# end class


class EqN(Block):
    def __init__(self, prev_blocks: Sequence[IBlock] = None, name: Optional[str] = None):
        Block.__init__(self, None, 1, name=name)

        if prev_blocks is not None:
            for b in prev_blocks:
                if b is not None:
                    self.conn_to_prev_block(b)
                # end if
            # end for
        # end if
    # end def

    def _calc_values(self):
        eq = True
        value = None
        value_calculated = False

        for conn_in in self._conn_in:
            if conn_in.value is None:
                self._pin_value[0] = None
                return
            else:
                if not value_calculated:
                    value = conn_in.value
                    value_calculated = True
                else:
                    if conn_in.value != value:
                        eq = False
                    # end if
                # end if
            # end if
        # end for

        self._pin_value[0] = int(eq) if value_calculated else None
    # end def
# end class
