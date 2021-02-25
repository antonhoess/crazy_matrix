from __future__ import annotations
from typing import List, Union
import uuid
from enum import Enum

from blocks.const_var import *
from blocks.math import *
from blocks.complex import *
from blocks.bool import *
from base.block import IBlock


__author__ = "Anton Höß"
__copyright__ = "Copyright 2021"


class IdGenerator:
    def __init__(self):
        self._ids: List[str] = list()
    # end def

    def new_id(self, length: Optional[int] = None) -> str:
        while True:
            new_id = uuid.uuid4().hex

            if length is not None:
                new_id = new_id[:length]

            # Try again to find a free uuid, if this one is already in use (which is very unlikely)
            if new_id not in self._ids:
                self._ids.append(new_id)
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
    BOX = "box"
    VAL_CONST = "const"
    VAL_CONST_E = "const_e"
    VAL_CONST_PI = "const_pi"
    VAL_VAR = "var"
    MATH_ADD = "add"
    MATH_SUB = "sub"
    MATH_MUL = "mul"
    MATH_DIV = "div"
    MATH_INV = "inv"
    MATH_ABS = "abs"
    MATH_MINUS = "minus"
    MATH_MOD = "mod"
    MATH_EXP = "exp"
    MATH_LOG = "log"
    MATH_LN = "ln"
    MATH_POW = "pow"
    MATH_SQ = "sq"
    MATH_SQRT = "sqrt"
    MATH_MIN = "min"
    MATH_MAX = "max"
    MATH_SIN = "sin"
    MATH_COS = "cos"
    MATH_TAN = "tan"
    MATH_ATAN = "atan"
    MATH_ATAN2 = "atan2"
    COMPLEX_ADD = "cadd"
    COMPLEX_SUB = "csub"
    COMPLEX_MUL = "cmul"
    COMPLEX_DIV = "cdiv"
    BOOL_AND = "and"
    BOOL_OR = "or"
    BOOL_NOT = "not"
    BOOL_GT = "gt"
    BOOL_LT = "lt"
    BOOL_EQ = "eq"
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
    def __init__(self, block_type: BlockType, n_in: Optional[int], n_out: int, item_id: str, value: Optional[float] = None, box_name: Optional[str] = None, name: Optional[str] = None):
        self.__type: BlockType = block_type
        self.__n_in: Optional[int] = n_in
        self.__n_out: int = n_out
        self.__id: str = item_id
        self.__value: Optional[float] = value
        self.__box_name: Optional[str] = box_name
        self.__name = name
    # end def

    def __str__(self):
        return f"BlockTemplate of type: '{self.__type.value}', n_in: {self.__n_in}, n_out: {self.__n_out}, id: {self.__id}"
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
    def n_out(self) -> int:
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

    @property
    def box_name(self) -> Optional[str]:
        return self.__box_name
    # end def

    @property
    def name(self) -> Optional[str]:
        return self.__name
    # end def
# end class


class BlockTemplateFactory:
    def __init__(self, id_gen: IdGenerator):
        self.__id_gen: IdGenerator = id_gen
        self.__block_pin_count_templates: List[Optional[BlockPinCountTemplate]] = []

        for t in BlockType:
            if t is BlockType.SYS_IN_POS:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(0, 2))

            elif t is BlockType.SYS_OUT_DRAWER:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 0))

            elif t is BlockType.BOX:
                self.__block_pin_count_templates.append(None)  # Template not possible, since interface (pins) can differ

            elif t is BlockType.VAL_CONST:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(0, 1))

            elif t is BlockType.VAL_CONST_E:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(0, 1))

            elif t is BlockType.VAL_CONST_PI:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(0, 1))

            elif t is BlockType.VAL_VAR:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_ADD:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(None, 1))

            elif t is BlockType.MATH_SUB:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(2, 1))

            elif t is BlockType.MATH_MUL:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(None, 1))

            elif t is BlockType.MATH_DIV:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(2, 1))

            elif t is BlockType.MATH_INV:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_ABS:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_MINUS:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_MOD:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(2, 1))

            elif t is BlockType.MATH_EXP:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_LOG:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(2, 1))

            elif t is BlockType.MATH_LN:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_POW:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(2, 1))

            elif t is BlockType.MATH_SQ:
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

            elif t is BlockType.MATH_ATAN:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.MATH_ATAN2:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(2, 1))

            elif t is BlockType.COMPLEX_ADD:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(None, 2))

            elif t is BlockType.COMPLEX_SUB:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(4, 2))

            elif t is BlockType.COMPLEX_MUL:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(None, 2))

            elif t is BlockType.COMPLEX_DIV:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(4, 2))

            elif t is BlockType.BOOL_AND:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(None, 1))

            elif t is BlockType.BOOL_OR:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(None, 1))

            elif t is BlockType.BOOL_NOT:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(1, 1))

            elif t is BlockType.BOOL_GT:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(2, 1))

            elif t is BlockType.BOOL_LT:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(2, 1))

            elif t is BlockType.BOOL_EQ:
                self.__block_pin_count_templates.append(BlockPinCountTemplate(None, 1))

            else:
                raise NotImplementedError(f"Enum entry {t} not handled!")
            # end if
        # end for
    # end def

    def get_block_template(self, block_type: BlockType, value: Optional[float] = None, box_name: Optional[str] = None, name: Optional[str] = None) -> BlockTemplate:
        for t, _type in enumerate(BlockType):
            if _type is block_type:
                if _type is not BlockType.BOX:
                    block_pin_count_template: BlockPinCountTemplate = self.__block_pin_count_templates[t]
                else:
                    from templates.box import BlackBoxFactory  # Due to circular dependency

                    bf: BlackBoxFactory = BlackBoxFactory().load(box_name)
                    block_pin_count_template: BlockPinCountTemplate = BlockPinCountTemplate(bf.n_in, bf.n_out)
                # end if

                return BlockTemplate(_type, block_pin_count_template.n_in, block_pin_count_template.n_out, self.__id_gen.new_id(length=4), value, box_name, name=name)
            # end if
        # end for

        raise ValueError(f"Parameter block_type with value {block_type} is not a valid entry of BlockType.")
    # end def
# end class


class BlockFactory:
    @staticmethod
    def inst(block_template: BlockTemplate, value: Optional[float] = None, box_name: Optional[float] = None) -> Optional[IBlock]:
        if block_template.type is BlockType.SYS_IN_POS:
            return None

        elif block_template.type is BlockType.SYS_OUT_DRAWER:
            return None

        elif block_template.type is BlockType.BOX:
            from templates.box import BlackBoxFactory  # Due to circular dependency

            return BlackBoxFactory().load(box_name).inst()  # XXX Hier einen Namen mit übergeben? Wie könnte dies nützlich sein?

        elif block_template.type is BlockType.VAL_CONST:
            return Const(value)

        elif block_template.type is BlockType.VAL_CONST_E:
            return ConstE()

        elif block_template.type is BlockType.VAL_CONST_PI:
            return ConstPi()

        elif block_template.type is BlockType.VAL_VAR:
            return Variable()

        elif block_template.type is BlockType.MATH_ADD:
            return AddN()

        elif block_template.type is BlockType.MATH_SUB:
            return Sub2()

        elif block_template.type is BlockType.MATH_MUL:
            return MulN()

        elif block_template.type is BlockType.MATH_DIV:
            return Div2()

        elif block_template.type is BlockType.MATH_INV:
            return Inv()

        elif block_template.type is BlockType.MATH_ABS:
            return Abs()

        elif block_template.type is BlockType.MATH_MINUS:
            return Minus()

        elif block_template.type is BlockType.MATH_MOD:
            return Mod()

        elif block_template.type is BlockType.MATH_EXP:
            return Exp()

        elif block_template.type is BlockType.MATH_LOG:
            return Log()

        elif block_template.type is BlockType.MATH_LN:
            return Ln()

        elif block_template.type is BlockType.MATH_POW:
            return Pow()

        elif block_template.type is BlockType.MATH_SQ:
            return Sq()

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

        elif block_template.type is BlockType.MATH_ATAN:
            return Atan()

        elif block_template.type is BlockType.MATH_ATAN2:
            return Atan2()

        elif block_template.type is BlockType.COMPLEX_ADD:
            return ComplexAddN()

        elif block_template.type is BlockType.COMPLEX_SUB:
            return ComplexSub()

        elif block_template.type is BlockType.COMPLEX_MUL:
            return ComplexMulN()

        elif block_template.type is BlockType.COMPLEX_DIV:
            return ComplexDiv()

        elif block_template.type is BlockType.BOOL_AND:
            return AndN()

        elif block_template.type is BlockType.BOOL_OR:
            return OrN()

        elif block_template.type is BlockType.BOOL_NOT:
            return Not()

        elif block_template.type is BlockType.BOOL_GT:
            return Gt()

        elif block_template.type is BlockType.BOOL_LT:
            return Lt()

        elif block_template.type is BlockType.BOOL_EQ:
            return EqN()

        else:
            return None
        # end if
    # end def
# end class
