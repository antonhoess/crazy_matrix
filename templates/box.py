from __future__ import annotations
from typing import Dict, List, Optional

from templates.bond import BondTemplate, BoxSide
from base.black_box import BlackBox, RepeatBox
from templates.circuit import CircuitFactory


class BlackBoxFactory(CircuitFactory):
    def __init__(self):
        CircuitFactory.__init__(self)
        self._n_in = 0
        self._n_out = 0
        self._bonds: List[BondTemplate] = list()
        self._name: Optional[str] = None  # Used as default name for instances

        # Extend the flexible list of handlers for loading data
        self._read_funcs.insert(1, {"name": "box", "func": self._read_box})
        self._read_funcs.append({"name": "bonds", "func": self._read_bonds})

        # Extend the flexible list of handlers for storing data
        self._write_funcs.insert(1, {"name": "box", "func": self._write_box})
        self._write_funcs.append({"name": "bonds", "func": self._write_bonds})

        # Extend the flexible list of handlers for instantiating
        self._inst_funcs.append({"name": "bonds", "func": self._inst_bonds})
    # end def

    @property
    def bonds(self) -> List[BondTemplate]:
        return self._bonds
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
            # Prevent from counting in-pins with multiple connections more than once.
            if len([b for b in self._bonds if b.side is BoxSide.IN and b.box_pin == bond.box_pin]) == 1:
                self._n_in += 1
        else:
            self._n_out += 1
        # end if
    # end def

    def inst(self, name: Optional[str] = None) -> BlackBox:
        inst_obj = CircuitFactory.InstHelper()
        inst_obj.box: BlackBox = BlackBox(self._n_in, self._n_out, name)
        self._do_inst(inst_obj)

        return inst_obj.box
    # end def

    def _inst_bonds(self, inst_obj: CircuitFactory.InstHelper):
        if hasattr(inst_obj, "box"):  # Avoid warnings
            for bond in self._bonds:
                block = self._get_block_by_id(inst_obj, bond.block_id)

                if bond.side is BoxSide.IN:
                    inst_obj.box.assign_conn_in(block, bond.block_pin, bond.box_pin)

                else:  # bond.side is BoxSide.OUT:
                    inst_obj.box.assign_pin_value(block, bond.block_pin, bond.box_pin)
                # end if
            # end for
        # end if
    # end def

    def load(self, filename: str, name: Optional[str] = None) -> BlackBoxFactory:
        self._load(filename, name=name)

        return self
    # end def

    def _read_box(self, value):
        self._n_in = value.get("n_in")
        self._n_out = value.get("n_out")
    # end def

    def _read_bonds(self, value):
        self._bonds = list()

        for bond in value:
            side = BoxSide(bond.get("side"))
            block_id = bond.get("block_id")
            block_pin = bond.get("block_pin")
            box_pin = bond.get("box_pin")

            self._bonds.append(BondTemplate(side, block_id, block_pin, box_pin))
        # end for
    # end def

    def _write_box(self, d: Dict):
        block_name = "box"
        box = dict()  # List of bonds

        box["n_in"] = self._n_in
        box["n_out"] = self._n_out

        d[block_name] = box
    # end def

    def _write_bonds(self, d: Dict):
        if self._bonds is not None and len(self._bonds) > 0:
            block_name = "bonds"
            bonds = list()  # List of bonds

            for bond in self._bonds:
                _bond = dict()
                _bond["side"] = bond.side.value
                _bond["block_id"] = bond.block_id
                _bond["block_pin"] = bond.block_pin
                _bond["box_pin"] = bond.box_pin

                bonds.append(_bond)
            # end for

            d[block_name] = bonds
        # end if
    # end def
# end class


class RepeatBoxFactory(BlackBoxFactory):
    def __init__(self):
        BlackBoxFactory.__init__(self)

        self._n_in_special = 1
    # end def

    def add_bond(self, bond: Optional[BondTemplate]):
        if bond is not None:
            BlackBoxFactory.add_bond(self, bond)
        else:  # An empty pin with no bond to the circuit inside the box. E.g. for the parameters specifying the number fo repetitions in a RepeatBox
            self._n_in += 1
        # end if
    # end def

    def inst(self, name: Optional[str] = None) -> RepeatBox:
        inst_obj = CircuitFactory.InstHelper()
        inst_obj.box: RepeatBox = RepeatBox(self._n_in - self._n_in_special, name)
        self._do_inst(inst_obj)

        return inst_obj.box
    # end def

    def load(self, filename: str, name: Optional[str] = None) -> RepeatBoxFactory:
        self._load(filename, name=name)

        return self
    # end def
# end class
