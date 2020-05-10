from __future__ import annotations
from typing import Dict
from base.basic import Circuit
from templates.block import *
from templates.conn import *


# XXX Auch eine Funktion machen zum prüfen, ob alle pins belegt sind, auch ovm drawer, damit sichergestellt ist, dass er überhaupt funktionieren kann
class CircuitFactory:
    def __init__(self):
        self.__blocks: List[BlockTemplate] = []
        self.__conns: List[ConnTemplate] = []
    # end def

    def add_block(self, block: BlockTemplate):
        self.__blocks.append(block)
    # end def

    def add_conn(self, conn: ConnTemplate):
        self.__conns.append(conn)
    # end def

    def inst(self) -> Circuit:
        blocks: List[Dict[str, Block]] = []
        circuit: Circuit = Circuit()

        def get_block_by_id(block_id: str):
            if block_id == "0":
                return circuit.point

            elif block_id == "1":
                return circuit.drawer

            else:
                for block in blocks:
                    if block["id"] == block_id:
                        return block["block"]
                    # end if
                # end for
            # end if

            return None
        # end def

        bf = BlockFactory()

        for block in self.__blocks:
            blocks.append({"id": block.id, "block": bf.inst(block, block.value)})
        # end for

        for conn in self.__conns:
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

    def store(self, filename: str):
        with open(filename, 'w') as f:
            for block in self.__blocks:
                f.write(f"Block;{block.type.value};{block.n_in if block.n_in is not None else -1};{block.n_out};{block.id};{block.value if block.value is not None else '-'}\n")
            # end for

            for conn in self.__conns:
                f.write(f"Conn;{conn.in_block_id};{conn.in_block_pin};{conn.out_block_id};{conn.out_block_pin if conn.out_block_pin is not None else -1}\n")
            # end for
        # end with
    # end def

    def load(self, filename: str):
        with open(filename, 'r') as f:
            for line in f:
                line = line.rstrip()
                fields = line.split(";")
                if len(fields) < 1:
                    continue

                elif fields[0] == "Block" and len(fields) == 6:
                    self.__blocks.append(BlockTemplate(BlockType(fields[1]), int(fields[2]) if int(fields[2]) > 0 else None, int(fields[3]), fields[4], float(fields[5]) if fields[5] != "-" else None))

                elif fields[0] == "Conn" and len(fields) == 5:
                    self.__conns.append(ConnTemplate(fields[1], int(fields[2]), fields[3], int(fields[4]) if int(fields[4]) >= 0 else None))
                # end if
            # end for
    # end def
# end class
