from __future__ import annotations
from typing import Dict, List, Optional

from templates.bond import BondTemplate, BoxSide
from base.black_box import BlackBox, IBlock
from templates.block import BlockFactory
from templates.circuit import CircuitFactory


class BoxFactory(CircuitFactory):
    def __init__(self):
        CircuitFactory.__init__(self)
        self._n_in = 0
        self._n_out = 0
        self._bonds: List[BondTemplate] = []
    # end def

    @property
    def n_in(self) -> int:
        return self._n_in
    # end def

    @property
    def n_out(self) -> int:
        return self._n_out
    # end def

    def add_bond(self, bond: BondTemplate):
        self._bonds.append(bond)

        if bond.side is BoxSide.IN:
            if len([b for b in self._bonds if b.side is BoxSide.IN and b.box_pin == bond.box_pin]) == 1:  # Prevent from counting in-pins with multiple connections more than once.
                self._n_in += 1
        else:
            self._n_out += 1
        # end if
    # end def

    def inst(self, name: Optional[str] = None) -> BlackBox:
        blocks: List[Dict[str, IBlock]] = list()
        # XXX box: IBox = IBox()
        box: BlackBox = BlackBox(self._n_in, self._n_out, name)

        def get_block_by_id(block_id: str) -> Optional[IBlock]:
            for b in blocks:
                if b["id"] == block_id:
                    return b["block"]
                # end if
            # end for

            return None
        # end def

        bf = BlockFactory()

        for block in self._blocks:
            blocks.append({"id": block.id, "block": bf.inst(block, block.value)})
        # end for

        for conn in self._conns:
            in_block = get_block_by_id(conn.in_block_id)
            out_block = get_block_by_id(conn.out_block_id)

            out_block.conn_to_prev_block(in_block, conn.in_block_pin, conn.out_block_pin)
        # end for

        for bond in self._bonds:
            block = get_block_by_id(bond.block_id)

            if bond.side is BoxSide.IN:
                box.assign_conn_in(block, bond.block_pin, bond.box_pin)

            else:  # bond.side is BoxSide.OUT:
                box.assign_pin_value(block, bond.block_pin, bond.box_pin)
            # end if
        # end for

        return box
    # end def

    def _write_meta_information(self, file):
        file.write(f"Meta;{self._n_in if self._n_in is not None else '-'};{self._n_out if self._n_out is not None else '-'}\n")
    # end def

    def _write_bonds(self, file):
        for bond in self._bonds:
            file.write(f"Bond;{bond.side.value};{bond.block_id};{bond.block_pin if bond.block_pin is not None else '-'};{bond.box_pin}\n")
        # end for
    # end def

    def store(self, filename: str):
        with open(filename, 'w') as f:
            self._write_meta_information(f)
            self._write_blocks(f)
            self._write_conns(f)
            self._write_bonds(f)
        # end with
    # end def

    def _handle_line_check_for_meta_information(self, fields: List[str]) -> bool:
        if fields[0] == "Meta" and len(fields) == 3:
            self._n_in = int(fields[1]) if fields[1] != "-" else None
            self._n_out = int(fields[2]) if fields[2] != "-" else None
            return True

        else:
            return False
        # end if
    # end def

    def _handle_line_check_for_bond(self, fields: List[str]) -> bool:
        if fields[0] == "Bond" and len(fields) == 5:
            self._bonds.append(BondTemplate(BoxSide(fields[1]), fields[2], int(fields[3]) if fields[3] != "-" else None, int(fields[4])))
            return True

        else:
            return False
        # end if
    # end def

    def load(self, filename: str) -> BoxFactory:
        with open(filename, 'r') as f:
            for line in f:
                line = line.rstrip()
                fields = line.split(";")
                if len(fields) < 1:
                    continue

                if self._handle_line_check_for_meta_information(fields):
                    continue

                if self._handle_line_check_for_block(fields):
                    continue

                elif self._handle_line_check_for_conn(fields):
                    continue

                elif self._handle_line_check_for_bond(fields):
                    continue
                # end if
            # end for
        # end with

        return self
    # end def
# end class
