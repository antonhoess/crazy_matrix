from __future__ import annotations
from typing import Optional
from enum import Enum


class BoxSide(Enum):
    IN = "in"
    OUT = "out"
# end class


class BondTemplate:
    def __init__(self, side: BoxSide, block_id: str, block_pin: Optional[int], box_pin: int) -> None:
        self.__side: BoxSide = side
        self.__block_id: str = block_id
        self.__block_pin: Optional[int] = block_pin
        self.__box_pin: int = box_pin
    # end def

    def __str__(self):
        return f"BondTemplate: '{self.__block_id}:{self.__block_pin}' <=> '{self.__side}:{self.__box_pin}'"
    # end def

    @staticmethod
    def empty() -> None:
        return None
    # end def

    def __repr__(self):
        return str(self)
    # end def

    @property
    def side(self) -> BoxSide:
        return self.__side
    # end def

    @property
    def block_id(self) -> str:
        return self.__block_id
    # end def

    @property
    def block_pin(self) -> Optional[int]:
        return self.__block_pin
    # end def

    @property
    def box_pin(self) -> int:
        return self.__box_pin
    # end def
# end class
