from __future__ import annotations
from typing import List
import uuid
from enum import Enum

from blocks.const_var import *
from blocks.math import *
from blocks.deprecated import *


class IdGenerator:
    def __init__(self):
        self.__ids: List[str] = []
    # end def

    def new_id(self) -> str:
        while True:
            new_id = uuid.uuid4().hex

            # Try again to find a free uuid, if this one is already in use (which is very unlikely)
            if new_id not in self.__ids:
                self.__ids.append(new_id)
                break
            else:
                continue
            # end if
        # end while

        return new_id
    # end def
# end class


class BlockType(Enum):
    SYS_IN_POS = "pos"
    SYS_OUT_DRAWER = "drawer"
    VAL_CONST = "const"
    MATH_ADD = "add"
    MATH_SUB = "sub"
    MATH_MUL = "mul"
    MATH_DIV = "div"
    MATH_ABS = "abs"
    MATH_MINUS = "minus"
    MATH_MOD = "mod"
    MATH_SQUARE = "square"
    MATH_SQRT = "sqrt"
    MATH_MIN = "min"
    MATH_MAX = "max"
    MATH_SIN = "sin"
    MATH_COS = "cos"
    MATH_TAN = "tan"
# end class


class BlockPinCountTemplate:
    def __init__(self, n_in: Optional[int], n_out: int):
        self.__n_in: Optional[int] = n_in
        self.__n_out: int = n_out
    # end def

    @property
    def n_in(self) -> Optional[int]:
        return self.__n_in
    # end def

    @property
    def n_out(self) -> Optional[int]:
        return self.__n_out
    # end def
# end class


class BlockTemplate:
    def __init__(self, block_type: BlockType, n_in: Optional[int], n_out: int, item_id: str, value: Optional[float] = None):
        self.__type: BlockType = block_type
        self.__n_in: Optional[int] = n_in
        self.__n_out: int = n_out
        self.__id: str = item_id
        self.__value: Optional[float] = value
    # end def

    def __str__(self):
        return f"BlockTemplate of type: '{self.__type.value}', n_in: {self.__n_in}, n_out: {self.__n_out}, id: {self.__id[:8]}"
    # end def

    def __repr__(self):
        return str(self)
    # end def

    @property
    def type(self) -> BlockType:
        return self.__type
    # end def

    @property
    def n_in(self) -> Optional[int]:
        return self.__n_in
    # end def

    @property
    def n_out(self) -> Optional[int]:
        return self.__n_out
    # end def

    @property
    def id(self) -> str:
        return self.__id
    # end def

    @property
    def value(self) -> Optional[float]:
        return self.__value
    # end def
# end class


class BlockTemplateFactory:
    def __init__(self, id_gen: IdGenerator):
        self.__id_gen: IdGenerator = id_gen
        self.__block_pin_count_templates: List[BlockPinCountTemplate] = []

        for t in BlockType:
            if t is BlockType.SYS_IN_POS:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(0, 2))

            elif t is BlockType.SYS_OUT_DRAWER:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 0))

            elif t is BlockType.VAL_CONST:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(0, 1))

            elif t is BlockType.MATH_ADD:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(None, 1))

            elif t is BlockType.MATH_SUB:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(2, 1))

            elif t is BlockType.MATH_MUL:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(None, 1))

            elif t is BlockType.MATH_DIV:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(2, 1))

            elif t is BlockType.MATH_ABS:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_MINUS:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_MOD:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(2, 1))

            elif t is BlockType.MATH_SQUARE:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_SQRT:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_MIN:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(None, 1))

            elif t is BlockType.MATH_MAX:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(None, 1))

            elif t is BlockType.MATH_SIN:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_COS:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_TAN:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            else:
                raise NotImplementedError(f"Enum entry {t} not handled!")
            # end if
        # end for
    # end def

    def get_block_template(self, block_type: BlockType, value: Optional[float] = None) -> BlockTemplate:
        for t, _type in enumerate(BlockType):
            if _type is block_type:
                block_pin_count_template: BlockPinCountTemplate = self.__block_pin_count_templates[t]

                return BlockTemplate(_type, block_pin_count_template.n_in, block_pin_count_template.n_out, self.__id_gen.new_id(), value)
            # end if
        # end for

        raise ValueError(f"Parameter block_type with value {block_type} is not a valid entry of BlockType.")
    # end def
# end class


class BlockFactory:
    @staticmethod
    def inst(block_template: BlockTemplate, value: Optional[float] = None) -> Optional[Block]:
        if block_template.type is BlockType.SYS_IN_POS:
            return None

        elif block_template.type is BlockType.SYS_OUT_DRAWER:
            return None

        elif block_template.type is BlockType.VAL_CONST:
            return Const(value)

        elif block_template.type is BlockType.MATH_ADD:
            return AddN()

        elif block_template.type is BlockType.MATH_SUB:
            return Sub2()

        elif block_template.type is BlockType.MATH_MUL:
            return MulN()

        elif block_template.type is BlockType.MATH_DIV:
            return Div2()

        elif block_template.type is BlockType.MATH_ABS:
            return Abs()

        elif block_template.type is BlockType.MATH_MINUS:
            return Minus()

        elif block_template.type is BlockType.MATH_MOD:
            return Mod()

        elif block_template.type is BlockType.MATH_SQUARE:
            return Square()

        elif block_template.type is BlockType.MATH_SQRT:
            return Sqrt()

        elif block_template.type is BlockType.MATH_MIN:
            return MinN()

        elif block_template.type is BlockType.MATH_MAX:
            return MaxN()

        elif block_template.type is BlockType.MATH_SIN:
            return Sin()

        elif block_template.type is BlockType.MATH_COS:
            return Cos()

        elif block_template.type is BlockType.MATH_TAN:
            return Tan()

        else:
            return None
        # end if
    # end def
# end class



