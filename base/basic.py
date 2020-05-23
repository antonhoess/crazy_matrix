from base.block import BlockFixed


class Drawer(BlockFixed):
    def __init__(self):
        BlockFixed.__init__(self, 1, 0)
    # end def

    def __str__(self):
        return f"Drawer that evaluates the circuit for each point. Has only a single input."
    # end def

    def _calc_values(self):
        pass
    # end def

    def val(self) -> float:
        return self._conn_in[0].value if self._conn_in[0] is not None else None
# end class


class Point(BlockFixed):
    def __init__(self, x: int, y: int):
        BlockFixed.__init__(self, 0, 2)
        self._pin_value[0] = x
        self._pin_value[1] = y
    # end def

    @property
    def x(self) -> int:
        return int(self._pin_value[0])
    # end def

    @property
    def y(self) -> int:
        return int(self._pin_value[1])
    # end def

    def _calc_values(self):
        pass
    # end def
# end class


class DynamicPoint(Point):
    def __init__(self, x: int, y: int):
        Point.__init__(self, x, y)
    # end def

    def set_x(self, value: int):
        self._pin_value[0] = value
    # end def

    def set_y(self, value: int):
        self._pin_value[1] = value
    # end def
# end class


class Size(BlockFixed):
    def __init__(self, width: int = 0, height: int = 0):
        BlockFixed.__init__(self, 0, 2)

        self.set_size(width, height)
    # end def

    @property
    def width(self) -> int:
        return int(self._pin_value[0])
    # end def

    @property
    def height(self) -> int:
        return int(self._pin_value[1])
    # end def

    def set_size(self, width: int, height: int):
        self._pin_value[0] = width
        self._pin_value[1] = height
    # end def

    def _calc_values(self):
        pass
    # end def
# end class


class Circuit:
    def __init__(self):
        self.__cur_pos = DynamicPoint(0, 0)
        self.__drawer = Drawer()
        self.__size = Size()
    # end def

    def set_size(self, width: int, height: int):
        self.__size.set_size(width, height)
    # end def

    @property
    def point(self):
        return self.__cur_pos
    # end def

    @property
    def size(self):
        return self.__size
    # end def

    @property
    def drawer(self):
        return self.__drawer
    # end def

    def eval(self, x: int, y: int) -> float:
        self.__cur_pos.set_x(x)
        self.__cur_pos.set_y(y)

        res = self.__drawer.val()

        self.drawer.reset_evaluated()

        return res
    # end def
# end class
