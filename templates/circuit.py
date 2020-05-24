from __future__ import annotations
from typing import Dict, List, Optional, Union

from base.basic import Circuit
from base.block import IBlock
from templates.block import BlockType, BlockTemplate, BlockFactory
from templates.conn import ConnTemplate


class CircuitFactory:
    def __init__(self):
        self._blocks: List[BlockTemplate] = []
        self._conns: List[ConnTemplate] = []
        self._n_in = None
        self._n_out = None
    # end def

    def add_block(self, block: BlockTemplate) -> BlockTemplate:
        self._blocks.append(block)

        return block
    # end def

    def add_conn(self, conn: ConnTemplate):
        self._conns.append(conn)
    # end def

    def inst(self) -> Circuit:
        blocks: List[Dict[str, Optional[IBlock]]] = list()
        circuit: Circuit = Circuit()

        def get_block_by_id(block_id: str):
            if block_id == "0":
                return circuit.point

            elif block_id == "1":
                return circuit.drawer

            elif block_id == "2":
                return circuit.size

            else:
                for b in blocks:
                    if b["id"] == block_id:
                        return b["block"]
                    # end if
                # end for
            # end if

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

        return circuit
    # end def

    def _write_blocks(self, file):
        for block in self._blocks:
            file.write(f"Block;{block.type.value};{block.n_in if block.n_in is not None else '-'};{block.n_out};{block.id};{block.value if block.value is not None else '-'}\n")
        # end for
    # end def

    def _write_conns(self, file):
        for conn in self._conns:
            file.write(f"Conn;{conn.in_block_id};{conn.in_block_pin};{conn.out_block_id};{conn.out_block_pin if conn.out_block_pin is not None else '-'}\n")
        # end for
    # end def

    def store(self, filename: str):
        with open(filename, 'w') as f:
            self._write_blocks(f)
            self._write_conns(f)
        # end with
    # end def

    def _handle_line_check_for_block(self, fields: List[str]) -> bool:
        if fields[0] == "Block" and len(fields) == 6:
            block_type: BlockType = BlockType(fields[1])

            field_5: Optional[Union[float, str]] = None

            if block_type is not BlockType.BOX:
                if fields[5] != "-":
                    field_5 = float(fields[5])
                # end if
            else:
                field_5 = fields[5]
            # end if

            self._blocks.append(BlockTemplate(block_type, int(fields[2]) if fields[2] != "-" else None, int(fields[3]), fields[4], field_5))
            return True

        else:
            return False
        # end if
    # end def

    def _handle_line_check_for_conn(self, fields: List[str]) -> bool:
        if fields[0] == "Conn" and len(fields) == 5:
            self._conns.append(ConnTemplate(fields[1], int(fields[2]), fields[3], int(fields[4]) if fields[4] != "-" else None))
            return True

        else:
            return False
        # end if
    # end def

    def load(self, filename: str) -> CircuitFactory:
        with open(filename, "r") as f:
            for line in f:
                line = line.rstrip()
                fields = line.split(";")
                if len(fields) < 1:
                    continue

                if self._handle_line_check_for_block(fields):
                    continue

                elif self._handle_line_check_for_conn(fields):
                    continue
                # end if
            # end for
        # end with

        return self
    # end def
# end class
