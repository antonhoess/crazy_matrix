from __future__ import annotations
from typing import Dict, List, Optional
import yaml

from base.basic import Circuit
from base.block import IBlock
from templates.block import BlockType, BlockTemplate, BlockFactory
from templates.conn import ConnTemplate


class Literal(str):
    @staticmethod
    def literal_presenter(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    # end def

    @staticmethod
    def install():
        yaml.add_representer(Literal, Literal.literal_presenter)
    # end def
# end class


class CircuitFactory:
    # This class is necessary, since objects cannot get applied properties dynamically
    class InstHelper(object):
        pass
    # end class

    def __init__(self):
        self._blocks: List[BlockTemplate] = list()
        self._conns: List[ConnTemplate] = list()
        self._n_in = None
        self._n_out = None
        self._version: str = "1.0"
        self._desc = None

        # Flexible specify functions for loading data from file
        self._read_funcs = list()
        self._read_funcs.append({"name": "meta", "func": self._read_meta})
        self._read_funcs.append({"name": "blocks", "func": self._read_blocks})
        self._read_funcs.append({"name": "conns", "func": self._read_conns})

        # Flexible specify functions for storing data to file
        self._write_funcs = list()
        self._write_funcs.append({"name": "meta", "func": self._write_meta})
        self._write_funcs.append({"name": "blocks", "func": self._write_blocks})
        self._write_funcs.append({"name": "conns", "func": self._write_conns})

        # Flexible specify functions for instantiating
        self._inst_funcs = list()
        self._inst_funcs.append({"name": "blocks", "func": self._inst_blocks})
        self._inst_funcs.append({"name": "conns", "func": self._inst_conns})
    # end def

    @property
    def blocks(self) -> List[BlockTemplate]:
        return self._blocks
    # end def

    @property
    def conns(self) -> List[ConnTemplate]:
        return self._conns
    # end def

    def add_desc(self, desc: str):
        self._desc = desc
    # end def

    def add_block(self, block: BlockTemplate) -> BlockTemplate:
        self._blocks.append(block)

        return block
    # end def

    def add_conn(self, conn: ConnTemplate):
        self._conns.append(conn)
    # end def

    def inst(self) -> Circuit:
        inst_obj = CircuitFactory.InstHelper()  # Helper object that allows the dynamic use of and sharing between instantiating functions
        inst_obj.circuit: Circuit = Circuit()
        self._do_inst(inst_obj)

        return inst_obj.circuit
    # end def

    def _do_inst(self, inst_obj: CircuitFactory.InstHelper) -> None:
        for f in self._inst_funcs:
            f["func"](inst_obj)
        # end for
    # end def

    def _inst_blocks(self, inst_obj: CircuitFactory.InstHelper):
        bf = BlockFactory()

        inst_obj.blocks: List[Dict[str, Optional[IBlock]]] = list()

        for block in self._blocks:
            inst_obj.blocks.append({"id": block.id, "block": bf.inst(block, value=block.value, box_name=block.box_name)})
        # end for
    # end def

    def _inst_conns(self, inst_obj: CircuitFactory.InstHelper):
        for conn in self._conns:
            in_block = self._get_block_by_id(inst_obj, conn.in_block_id)
            out_block = self._get_block_by_id(inst_obj, conn.out_block_id)

            out_block.conn_to_prev_block(in_block, conn.in_block_pin, conn.out_block_pin)
        # end for
    # end def

    @staticmethod
    def _get_block_by_id(inst_obj: CircuitFactory.InstHelper, block_id: str):
        if hasattr(inst_obj, "circuit"):  # Avoid warnings
            if block_id == "0":
                return inst_obj.circuit.point

            elif block_id == "1":
                return inst_obj.circuit.drawer

            elif block_id == "2":
                return inst_obj.circuit.size
            # end if

        if hasattr(inst_obj, "blocks"):
            for b in inst_obj.blocks:
                if b["id"] == block_id:
                    return b["block"]
                # end if
            # end for
        # end if

        return None
    # end def

    def load(self, filename: str) -> CircuitFactory:
        self._load(filename)

        return self
    # end def

    def _load(self, filename: str, name: Optional[str] = None) -> None:
        with open(filename) as f:
            # Reset potential previous data
            self._blocks = list()
            self._conns = list()

            self._name = name

            docs = [doc for doc in yaml.load_all(f, Loader=yaml.FullLoader)]
            doc = docs[0]

            for key, value in doc.items():
                for rf in self._read_funcs:
                    if rf["name"] == key:
                        rf["func"](value)
                        continue
                    # end if
                # end for
            # end for
        # end with
    # end def

    def _read_meta(self, value):
        version = value.get("version")

        if version != self._version:
            print(f"Version of loaded {version} file does not correspond to the internal version {self._version}.")
        # end if

        self._desc = value.get("desc")
    # end def

    def _read_blocks(self, value):
        self._blocks = list()

        for block in value:
            name = block.get("name")
            type_ = BlockType(block.get("type"))
            n_in = block.get("n_in")
            n_out = block.get("n_out")
            id_ = block.get("id")
            value = block.get("value")
            box_name = block.get("box_name")

            self._blocks.append(BlockTemplate(type_, n_in, n_out, id_, value, box_name, name=name))
        # end for
    # end def

    def _read_conns(self, value):
        self._conns = list()

        for block in value:
            in_block_id = block.get("in_block_id")
            in_block_pin = block.get("in_block_pin")
            out_block_id = block.get("out_block_id")
            out_block_pin = block.get("out_block_pin")

            self._conns.append(ConnTemplate(in_block_id, in_block_pin, out_block_id, out_block_pin))
        # end for
    # end def

    def store(self, filename: str):
        d = dict()

        for wf in self._write_funcs:
            wf["func"](d)
        # end for

        # write to file
        ###############
        with open(filename, 'w') as f:
            Literal.install()
            yaml.dump(d, f, sort_keys=False)
        # end with
    # end def

    def _write_meta(self, d: Dict):
        block_name = "meta"
        meta = dict()  # List of bonds

        meta["version"] = self._version
        meta["desc"] = Literal(self._desc)

        d[block_name] = meta
    # end def

    def _write_blocks(self, d: Dict):
        if self._blocks is not None and len(self._blocks) > 0:
            block_name = "blocks"
            blocks = list()  # List of blocks

            for block in self._blocks:
                _block = dict()
                _block["name"] = block.name
                _block["type"] = block.type.value
                _block["n_in"] = block.n_in
                _block["n_out"] = block.n_out
                _block["id"] = block.id
                if block.value is not None:
                    _block["value"] = block.value
                if block.box_name is not None:
                    _block["box_name"] = block.box_name

                blocks.append(_block)
            # end for

            d[block_name] = blocks
        # end if
    # end def

    def _write_conns(self, d: Dict):
        if self._conns is not None and len(self._conns) > 0:
            block_name = "conns"
            conns = list()  # List of conns

            for conn in self._conns:
                _conn = dict()
                _conn["in_block_id"] = conn.in_block_id
                _conn["in_block_pin"] = conn.in_block_pin
                _conn["out_block_id"] = conn.out_block_id
                _conn["out_block_pin"] = conn.out_block_pin

                conns.append(_conn)
            # end for

            d[block_name] = conns
        # end if
    # end def
# end class
