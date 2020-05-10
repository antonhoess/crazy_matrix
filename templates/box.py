from templates.circuit import *
from templates.bond import *
from base.block import *
from base.black_box import *


# XXX was ist mit repeatbox
class BoxFactory(CircuitFactory):
    def __init__(self):
        CircuitFactory.__init__(self)
        # self.__n_in = n_in  # xXX diese klasse evtl. komplett neu implementieren oder die parameter in den konstrultor nehmen anstatt bei inst() zu übergeben, da dort die signatur nicht zusammenpasst - oder noch ganzt andere lösung?
        # self.__n_in = n_in
        # self.__name = name
        self._bonds: List[BondTemplate] = []
    # end def

    def add_bond(self, bond: BondTemplate):
        self._bonds.append(bond)
    # end def

    def inst(self, n_in: int, n_out: int, name: Optional[str] = None) -> BlackBox:
        blocks: List[Dict[str, Block]] = []
        #box: IBox = IBox()
        box: BlackBox = BlackBox(n_in, n_out, name)

        def get_block_by_id(block_id: str):
            for block in blocks:
                if block["id"] == block_id:
                    return block["block"]
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

            if conn.out_block_pin is not None:
                out_block.conn_to_prev_block(in_block, conn.in_block_pin, conn.out_block_pin)
            else:
                out_block.add_conn_to_prev_block(in_block, conn.in_block_pin)
            # end if
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

    def _write_bonds(self, file):
        for bond in self._bonds:
            file.write(f"Bond;{bond.side.value};{bond.block_id};{bond.block_pin if bond.block_pin is not None else '-'};{bond.box_pin}\n")
        # end for
    # end def

    def store(self, filename: str):
        with open(filename, 'w') as f:
            self._write_blocks(f)
            self._write_conns(f)
            self._write_bonds(f)
        # end with
    # end def

    def _handle_line_check_for_bond(self, fields: List[str]) -> bool:
        if fields[0] == "Bond" and len(fields) == 5:
            self._bonds.append(BondTemplate(BoxSide(fields[1]), fields[2], int(fields[3]) if fields[3] != "-" else None, int(fields[4])))
            return True

        else:
            return False
        # end if
    # end def

    def load(self, filename: str):
        with open(filename, 'r') as f:
            for line in f:
                line = line.rstrip()
                fields = line.split(";")
                if len(fields) < 1:
                    continue

                if self._handle_line_check_for_block(fields):
                    continue

                elif self._handle_line_check_for_conn(fields):
                    continue

                elif self._handle_line_check_for_bond(fields):
                    continue
                # end if
            # end for
    # end def
# end class
