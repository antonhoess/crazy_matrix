from __future__ import annotations
from typing import Optional


class ConnTemplate:
    def __init__(self, in_block_id: str, in_block_pin: int, out_block_id: str, out_block_pin: Optional[int]):
        self.__in_block_id: str = in_block_id
        self.__in_block_pin: int = in_block_pin
        self.__out_block_id: str = out_block_id
        self.__out_block_pin: Optional[int] = out_block_pin
    # end def

    def __str__(self):
        return f"ConnTemplate: '{self.__in_block_id[:8]}:{self.__in_block_pin}' <- '{self.__out_block_id[:8]}:{self.__out_block_pin}'"
    # end def

    def __repr__(self):
        return str(self)
    # end def

    @property
    def in_block_id(self) -> str:
        return self.__in_block_id
    # end def

    @property
    def out_block_id(self) -> str:
        return self.__out_block_id
    # end def

    @property
    def in_block_pin(self) -> int:
        return self.__in_block_pin
    # end def

    @property
    def out_block_pin(self) -> int:
        return self.__out_block_pin
    # end def self.__id
    # end def
# end class


class ConnTemplateFactory:
    @staticmethod
    def get_conn_template(in_block_id: str, in_block_pin: int, out_block_id: str, out_block_pin: Optional[int]) -> ConnTemplate:
        return ConnTemplate(in_block_id, in_block_pin, out_block_id, out_block_pin)
    # end def
# end class
