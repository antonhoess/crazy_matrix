from __future__ import annotations
from typing import Optional, Tuple, List, Callable, Iterable
import numpy as np
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from enum import Enum, auto


__author__ = "Anton Höß"
__copyright__ = "Copyright 2021"


# Events in tkinter-Canvas
# http://books.gigatux.nl/mirror/pythoninanutshell/0596100469/pythonian-CHP-17-SECT-9.html -> 17.9.3.2. Mouse events


class ResizeDir(Enum):
    TOP = auto()
    TOP_RIGHT = auto()
    RIGHT = auto()
    BOTTOM_RIGHT = auto()
    BOTTOM = auto()
    BOTTOM_LEFT = auto()
    LEFT = auto()
    TOP_LEFT = auto()

    @staticmethod
    def get_corresponding_dir(resize_dir) -> Iterable[ResizeDir]:
        if resize_dir is ResizeDir.TOP:
            return ResizeDir.TOP_LEFT, ResizeDir.TOP, ResizeDir.TOP_RIGHT
        elif resize_dir is ResizeDir.BOTTOM:
            return ResizeDir.BOTTOM_LEFT, ResizeDir.BOTTOM, ResizeDir.BOTTOM_RIGHT
        elif resize_dir is ResizeDir.LEFT:
            return ResizeDir.TOP_LEFT, ResizeDir.LEFT, ResizeDir.BOTTOM_LEFT
        elif resize_dir is ResizeDir.RIGHT:
            return ResizeDir.TOP_RIGHT, ResizeDir.RIGHT, ResizeDir.BOTTOM_RIGHT
        else:
            return []
    # end def

    @staticmethod
    def get_neighboring_dir(resize_dir) -> Iterable[ResizeDir]:
        if resize_dir is ResizeDir.TOP:
            return ResizeDir.LEFT, ResizeDir.TOP, ResizeDir.RIGHT
        elif resize_dir is ResizeDir.BOTTOM:
            return ResizeDir.LEFT, ResizeDir.BOTTOM, ResizeDir.RIGHT
        elif resize_dir is ResizeDir.LEFT:
            return ResizeDir.TOP, ResizeDir.LEFT, ResizeDir.BOTTOM
        elif resize_dir is ResizeDir.RIGHT:
            return ResizeDir.TOP, ResizeDir.RIGHT, ResizeDir.BOTTOM
        else:
            return []
    # end def
# end class


class ConnDir(Enum):
    IN = auto()
    OUT = auto()
# end class


class MoveEvent:
    def __init__(self, dx: float, dy: float) -> None:
        self._dx = dx
        self._dy = dy
    # end def

    @property
    def dx(self) -> float:
        return self._dx
    # end def

    @property
    def dy(self) -> float:
        return self._dy
    # end def

    def __repr__(self) -> str:
        return f"MoveEvent(dx={self._dx}, dy={self._dy})"
    # end def

    def __str__(self) -> str:
        return repr(self)
    # end def
# end class


class Item:
    def __init__(self, editor: Editor, item_id: int, base_coords: Iterable[float], parent: Optional[Item] = None) -> None:
        self._editor = editor
        self._item_id = item_id
        self._base_coords = base_coords
        self._parent = parent
        self._children = list()

        if parent:
            parent._add_child(self)

        editor.add_item(self)

        # Callbacks
        self._cbs_move = list()
        self._cbs_events = list()
    # end def

    def __repr__(self) -> str:
        return f"Item(editor={self._editor}, item_id={self._item_id}, base_coords={self._base_coords}, parent={self._parent})"
    # end def

    def __str__(self) -> str:
        return repr(self)
    # end def

    @property
    def item_id(self) -> int:
        return self._item_id
    # end def

    @property
    def parent(self) -> Optional[Item]:
        return self._parent
    # end def

    # We need to use this complicated way since bbox() returns a bbox too big
    # as it considers also the rectangles line width
    @property
    def bbox(self) -> Tuple[int, int, int, int]:
        coords = self._editor.coords(self.item_id)
        x1, y1, x2, y2 = min(coords[::2]), min(coords[1::2]), max(coords[::2]), max(coords[1::2])

        return x1, y1, x2, y2
    # end def

    def check_inside_item_bbox(self, pos_x: int, pos_y: int) -> bool:
        x1, y1, x2, y2 = self.bbox

        return x1 <= pos_x <= x2 and y1 <= pos_y <= y2
    # end def

    def _add_child(self, child: Item) -> None:
        self._children.append(child)
    # end def

    def move_point(self, point_idx: int, dx: float, dy: float) -> bool:
        coords = self._editor.coords(self._item_id)

        if 0 <= point_idx < len(coords) / 2:
            coords[point_idx * 2 + 0] += dx
            coords[point_idx * 2 + 1] += dy
            self._editor.coords(self._item_id, *coords)
            return True
        else:
            return False
        # end if
    # end def

    def move(self, dx: float, dy: float, recursive: bool = False) -> None:
        self._editor.move(self._item_id, dx, dy)

        if recursive:
            for child in self._children:
                child.move(dx, dy, True)
            # end for
        # end if
    # end def

    def bind_move(self, cb: Callable[[MoveEvent], None]) -> None:
        self._cbs_move.append(cb)
    # end def

    def _fire_cbs_move(self, dx: float, dy: float) -> None:
        event = MoveEvent(dx, dy)

        for cb in self._cbs_move:
            cb(event)
        # end for
    # end def

    def bind(self, event=None, callback=None, add=None) -> None:
        self._cbs_events.append((event, callback))
        self._editor.tag_bind(self._item_id, event, callback, add)
    # end def

    def do_event(self, sequence: str, event: tk.Event):
        for s, cb in self._cbs_events:
            if s == sequence:
                cb(event)
        # end for
    # end def

    def itemconfigure(self, cnf=None, **kw) -> None:
        self._editor.itemconfigure(self._item_id, cnf, **kw)
    # end der
# end class


class Frame(Item):
    def __init__(self, editor: Editor, x: float, y: float, width: float, height: float,
                 corner_radius: float, parent_block: VBlock) -> None:
        coords = (x, y, x + width, y + height)
        item_id = editor.create_rectangle_rounded(*coords, corner_radius, outline="blue", width=1)
        super().__init__(editor, item_id, coords, None)

        self._corner_radius = corner_radius
        self._parent_block = parent_block
    # end def

    def __repr__(self) -> str:
        x1, y1, x2, y2 = self.bbox
        return f"Item(editor={self._editor}, x={x1}, y={y1}, width={x2-x1}, height={y2-y1}, corner_radius={self._corner_radius}, parent_block={self._parent_block})"
    # end def

    def __str__(self) -> str:
        return repr(self)
    # end def

    @property
    def corner_radius(self) -> float:
        return self._corner_radius
    # end def

    @property
    def parent_block(self) -> VBlock:
        return self._parent_block
    # end def
# end class


class Pin(Item):
    def __init__(self, editor: Editor, conn_dir: ConnDir, x: float, y: float, width: float, height: float, parent: Optional[Item] = None) -> None:
        coords = x, y, x + width, y + height
        item_id = editor.create_rectangle(*coords, outline="blue")
        super().__init__(editor, item_id, coords, parent)

        self._conn_dir = conn_dir

        self._conn: Optional[Connection] = None
    # end def

    def __repr__(self) -> str:
        x1, y1, x2, y2 = self.bbox
        return f"Item(editor={self._editor}, conn_dir={self._conn_dir}, x={x1}, y={y1}, width={x2-x1}, height={y2-y1}, parent={self._parent})"
    # end def

    def __str__(self) -> str:
        return repr(self)
    # end def

    @property
    def conn_dir(self) -> ConnDir:
        return self._conn_dir
    # end def

    @property
    def occupied(self) -> bool:
        return self.conn is not None
    # end def

    @property
    def center_coords(self) -> Tuple[float, float]:
        x1, y1, x2, y2 = self.bbox
        return (x2 + x1) // 2, (y2 + y1) // 2
    # end def

    @property
    def conn(self) -> Optional[Connection]:
        return self._conn
    # end def

    @conn.setter
    def conn(self, conn: Optional[Connection]) -> None:
        self._conn = conn
    # end def
# end class


class Caption(Item):
    def __init__(self, editor: Editor, x: float, y: float,
                 text: str, parent: Optional[Item] = None) -> None:
        coords = (x, y)
        item_id = editor.create_text(*coords, font=("Arial", 20, "normal"), fill="black", text=text)
        super().__init__(editor, item_id, coords, parent)

        self._text = text
    # end def

    def __repr__(self) -> str:
        x1, y1, _, _ = self.bbox
        return f"Item(editor={self._editor}, x={x1}, y={y1}, text={self._text}, parent={self._parent})"
    # end def

    def __str__(self) -> str:
        return repr(self)
    # end def

    @property
    def text(self) -> str:
        return self._text
    # end def
# end class


class ResizeLine(Item):
    def __init__(self, editor: Editor, x1: float, y1: float, x2: float, y2: float,
                 resize_dir: ResizeDir, parent: Optional[Item] = None) -> None:
        coords = x1, y1, x2, y2
        item_id = editor.create_line(*coords, fill="blue")
        super().__init__(editor, item_id, coords, parent)

        self._dir = resize_dir
    # end def

    def __repr__(self) -> str:
        x1, y1, x2, y2 = self.bbox
        return f"Item(editor={self._editor}, x1={x1}, y1={y1}, x2={x2}, y2={y2}, resize_dir={self._dir}, parent={self._parent})"
    # end def

    def __str__(self) -> str:
        return repr(self)
    # end def

    @property
    def dir(self) -> ResizeDir:
        return self._dir
    # end def
# end class


class Connection(Item):
    def __init__(self, editor: Editor, x: float, y: float, first_conn_pin: Pin, parent: Optional[Item] = None) -> None:
        coords = (x, y, x, y)
        item_id = editor.create_line(*coords, width=2, fill="blue")

        editor.tag_raise(item_id, "all")
        super().__init__(editor, item_id, coords, parent)

        self._output_pin = None
        self._input_pin = None

        if first_conn_pin.conn_dir is ConnDir.OUT:
            self._output_pin = first_conn_pin
        else:
            self._input_pin = first_conn_pin
        # end if

        self._connected = False

        self.bind("<Enter>", lambda event: self.forward_event_to_underlying_non_connector_item("<Enter>", event, forward_only_when_connected=True))
        self.bind("<Leave>", lambda event: self.forward_event_to_underlying_non_connector_item("<Leave>", event, forward_only_when_connected=True))
        self.bind("<Button-1>", lambda event: self.forward_event_to_underlying_non_connector_item("<Button-1>", event))
        self.bind("<ButtonRelease-1>", lambda event: self.forward_event_to_underlying_non_connector_item("<ButtonRelease-1>", event))
        self.bind("<B1-Motion>", lambda event: self.forward_event_to_underlying_non_connector_item("<B1-Motion>", event, item=self._editor.connect_start, forward_only_when_connected=True))
    # end def

    def __repr__(self) -> str:
        x1, y1, x2, y2 = self.bbox
        first_conn_pin = self._output_pin if self._output_pin is not None else self._input_pin
        return f"Item(editor={self._editor}, x={x1}, y={y1}, first_conn_pin={first_conn_pin}, parent={self._parent})"
    # end def

    def __str__(self) -> str:
        return repr(self)
    # end def

    @property
    def connected(self) -> bool:
        return self._connected
    # end def

    def forward_event_to_underlying_non_connector_item(self, sequence: str, event: tk.Event, item: Optional[Item] = None, forward_only_when_connected: bool = False) -> None:
        if item is None:
            x, y = getattr(event, "x"), getattr(event, "y")
            print(sequence)

            # Helps to retrieve the current topmost block under the cursor.
            # We have to do it this complicated way, since the currently drawn connector line blocks the
            # cursor's 'view' to the current item under the cursor.
            item_ids_under_cursor = list(reversed(self._editor.find_overlapping(x, y, x, y)))

            # Ignore the connection line object (which is always under the mouse cursor),
            # since we want the potentially underlying items
            while len(item_ids_under_cursor) > 0 and isinstance(self._editor.get_item_by_id(item_ids_under_cursor[0]), Connection):
                item_ids_under_cursor.pop(0)
            # end while

            if len(item_ids_under_cursor) > 0:
                print("->")
                item = self._editor.get_item_by_id(item_ids_under_cursor[0])
            # end if
        # end if

        if item is not None:
            connected = self._editor.cur_conn is not None and not self._editor.cur_conn.connected

            if forward_only_when_connected and connected or not forward_only_when_connected:
                item.do_event(sequence, event)
            # end if
        # end if
    # end def

    def open_connection_at(self, pin: Pin) -> Optional[Pin]:
        if pin in (self._output_pin, self._input_pin):
            self._connected = False

            if pin is self._output_pin:
                self._output_pin = None
                return self._input_pin

            elif pin is self._input_pin:
                self._input_pin = None
                return self._output_pin
            # end if
        # end if

        return None
    # end def

    def update_open_conn_end(self, x: float, y: float) -> None:
        if not self._connected:
            if self._output_pin is None:
                self.update_output_pos(x, y)
            else:
                self.update_input_pos(x, y)
            # end if
        # end if
    # end def

    def update_output_pos(self, x: float, y: float) -> None:
        coords = self._editor.coords(self._item_id)
        coords[0:2] = [x, y]
        self._editor.coords(self._item_id, *coords)
    # end def

    def update_input_pos(self, x: float, y: float) -> None:
        coords = self._editor.coords(self._item_id)
        coords[2:4] = [x, y]
        self._editor.coords(self._item_id, *coords)
    # end def

    def connect(self, second_conn_pin: Pin) -> bool:
        if second_conn_pin.conn_dir is ConnDir.OUT and self._output_pin is None:
            self._output_pin = second_conn_pin
            self._output_pin.conn = self
            self._connected = True
            return True

        elif second_conn_pin.conn_dir is ConnDir.IN and self._input_pin is None:
            self._input_pin = second_conn_pin
            self._input_pin.conn = self
            self._connected = True
            return True

        else:
            return False
        # end if
    # end def

    def dispose(self) -> None:
        # Disconnect already connected pin
        if self._output_pin is not None:
            self._output_pin.conn = None
        # end if

        if self._input_pin is not None:
            self._input_pin.conn = None
        # end if

        # Delete line
        self._editor.delete(self._item_id)
    # end def
# end class


class VBlock:
    def __init__(self, editor: Editor, name: str, n_inputs: int, n_outputs: int, x: float, y: float,
                 width: float, height: float, corner_radius: int = 12, connector_size: int = 10) -> None:
        self._editor = editor
        self._name = name

        self._n_inputs = n_inputs
        self._n_outputs = n_outputs

        self._corner_radius = corner_radius
        self._connector_size = connector_size

        self._freeze_highlighting = False
        self._resize_min_size_offset = [0, 0]

        # Common variables for multiple actions
        self._grid_size = 10
        self._action_base_grid_offset = None
        self._action_last_pos_mouse = None

        # Resize
        self._resize_dir = None

        # Main Frame
        self._frame = Frame(self._editor, x, y, width, height, corner_radius, self)

        # Label
        self._caption = Caption(self._editor, x + width / 2, y + height / 2, text=name, parent=self._frame)

        # Resize-lines
        self._resize_lines = list()

        self._resize_lines.append(
            ResizeLine(self._editor, *self._get_resize_line_coords(ResizeDir.TOP, x, y, width, height), resize_dir=ResizeDir.TOP, parent=self._frame))

        self._resize_lines.append(
            ResizeLine(self._editor, *self._get_resize_line_coords(ResizeDir.RIGHT, x, y, width, height), resize_dir=ResizeDir.RIGHT, parent=self._frame))

        self._resize_lines.append(
            ResizeLine(self._editor, *self._get_resize_line_coords(ResizeDir.BOTTOM, x, y, width, height), resize_dir=ResizeDir.BOTTOM, parent=self._frame))

        self._resize_lines.append(
            ResizeLine(self._editor, *self._get_resize_line_coords(ResizeDir.LEFT, x, y, width, height), resize_dir=ResizeDir.LEFT, parent=self._frame))

        # Input connectors
        self._input_pins = list()
        for n in range(self._n_inputs):
            x1, y1, x2, y2 = self._get_connect_pin_coords(x, y, x + width, y + height, self._n_inputs, n, ConnDir.IN)
            self._input_pins.append(Pin(self._editor, ConnDir.IN, x1, y1, x2 - x1, y2 - y1, parent=self._frame))
        # end for

        # Output connectors
        self._output_pins = list()
        for n in range(self._n_outputs):
            x1, y1, x2, y2 = self._get_connect_pin_coords(x, y, x + width, y + height, self._n_outputs, n, ConnDir.OUT)
            self._output_pins.append(Pin(self._editor, ConnDir.OUT, x1, y1, x2 - x1, y2 - y1, parent=self._frame))
        # end for

        # Hide elements that are only shown when the mouse hovers over the block
        self._do_leave()

        # Bind enter/leave events
        self.items = self._get_all_items()

        for item in self.items:
            item.bind("<Enter>", lambda event: self._on_enter_or_leave(event))
            item.bind("<Leave>", lambda event: self._on_enter_or_leave(event))
            item.bind("<Button-1>", lambda event: self._on_button_1(event))
            item.bind("<B1-Motion>", lambda event: self._on_b1_motion(event))
            item.bind("<ButtonRelease-1>", lambda event: self._on_button_release_1(event))
        # end for
    # end def

    def __repr__(self) -> str:
        x1, y1, x2, y2 = self._frame.bbox
        return f"Item(editor={self._editor}, name={self._name}, n_inputs={self._n_inputs}, n_outputs={self._n_outputs}, x={x1}, y={y1}, width={x2-x1}, height={y2-y1} " \
               f"corner_radius={self._corner_radius}, connector_size={self._connector_size})"
    # end def

    def __str__(self) -> str:
        return repr(self)
    # end def

    @property
    def frame(self) -> Frame:
        return self._frame
    # end def

    @property
    def freeze_highlighting(self) -> bool:
        return self._freeze_highlighting
    # end def

    @freeze_highlighting.setter
    def freeze_highlighting(self, freeze: bool) -> None:
        self._freeze_highlighting = freeze
    # end def

    def _get_all_items(self) -> List[Item]:
        items = list()
        items.append(self._frame)
        items.append(self._caption)
        items.extend(self._resize_lines)
        items.extend(self._input_pins)
        items.extend(self._output_pins)

        return items
    # end def

    def _get_resize_line_coords(self, resize_dir: ResizeDir, x: float, y: float, width: float, height: float) -> Tuple[float, float, float, float]:
        if resize_dir is ResizeDir.TOP:
            return x, y + self._corner_radius,\
                   x + width, y + self._corner_radius

        elif resize_dir is ResizeDir.RIGHT:
            return x + width - self._corner_radius, y,\
                   x + width - self._corner_radius, y + height

        elif resize_dir is ResizeDir.BOTTOM:
            return x, y + height - self._corner_radius,\
                   x + width, y + height - self._corner_radius

        else:  # if resize_dir is ResizeDir.LEFT:
            return x + self._corner_radius, y,\
                   x + self._corner_radius, y + height
    # end def

    def _get_connect_pin_coords(self, x1: float, y1: float, x2: float, y2: float, pin_cnt: int, pin_idx: int, conn_dir: ConnDir) -> Tuple[float, float, float, float]:
        height = y2 - y1
        width = x2 - x1
        connector_dist = (height - 2 * self._corner_radius - pin_cnt * self._connector_size) / (pin_cnt - 1)

        if conn_dir is ConnDir.IN:
            x = x1 + self._corner_radius
        else:
            x = x1 + width - self._corner_radius - self._connector_size
        # end if
        coords = (x,
                  y1 + self._corner_radius + pin_idx * (connector_dist + self._connector_size),
                  x + self._connector_size,
                  y1 + self._corner_radius + pin_idx * connector_dist + (pin_idx + 1) * self._connector_size)

        return coords
    # end def

    def _do_enter(self) -> None:
        self._frame.itemconfigure(fill="orange")

        for resize_line in self._resize_lines:
            resize_line.itemconfigure(state=tk.NORMAL)
        # end for
    # end for

    def _do_leave(self) -> None:
        self._frame.itemconfigure(fill="light blue")

        for resize_line in self._resize_lines:
            resize_line.itemconfigure(state=tk.HIDDEN)
        # end for
    # end for

    def _on_enter_or_leave(self, event: tk.Event) -> None:
        if not self._freeze_highlighting:
            if getattr(event, "type") == tk.EventType.Enter:
                self._do_enter()
            elif getattr(event, "type") == tk.EventType.Leave:
                self._do_leave()
            # end if
        # end if
    # end def

    def is_within_connector_area(self, pos_x: int, pos_y: int) -> Optional[Pin]:
        def is_within_connector_area(conn_dir: ConnDir) -> Optional[Pin]:
            pins = self._input_pins if conn_dir == ConnDir.IN else self._output_pins

            for n, pin in enumerate(pins):
                if pin.check_inside_item_bbox(pos_x, pos_y):
                    return pin
                # end if
            # end for

            return None
        # end def

        res = is_within_connector_area(ConnDir.IN)
        if res is not None:
            return res

        res = is_within_connector_area(ConnDir.OUT)
        if res is not None:
            return res

        return None
    # end def

    def _is_within_resize_area(self, pos_x: int, pos_y: int) -> Optional[ResizeDir]:
        x1, y1, x2, y2 = self._frame.bbox
        size = self._corner_radius

        if x1 + size < pos_x < x2 - size and pos_y < y1 + size:
            return ResizeDir.TOP

        elif x2 - size < pos_x and pos_y < y1 + size:
            return ResizeDir.TOP_RIGHT

        elif x2 - size < pos_x and y1 + size < pos_y < y2 - size:
            return ResizeDir.RIGHT

        elif x2 - size < pos_x and y2 - size < pos_y:
            return ResizeDir.BOTTOM_RIGHT

        elif x1 + size < pos_x < x2 - size and y2 - size < pos_y:
            return ResizeDir.BOTTOM

        elif pos_x < x1 + size and y2 - size < pos_y:
            return ResizeDir.BOTTOM_LEFT

        elif pos_x < x1 + size and y1 + size < pos_y < y2 - size:
            return ResizeDir.LEFT

        elif pos_x < x1 + size and pos_y < y1 + size:
            return ResizeDir.TOP_LEFT
        # end if

        return None
    # end def

    def _raise_to_top(self) -> None:
        # Bring all elements of the block to the top
        for item in self.items:
            self._editor.tag_raise(item.item_id, "all")
        # end for

        # Bring all connection lines that are connected to the current block to the very top
        for pin in self._input_pins + self._output_pins:
            if pin.occupied:
                self._editor.tag_raise(pin.conn.item_id, "all")
            # end if
        # end for
    # end def

    def _resize(self, resize_dir: ResizeDir, dx: int, dy: int) -> None:
        # Get old rectangle
        x1, y1, x2, y2 = self._frame.bbox

        # There needs to be guaranteed a minimum size even if there are no connectors placed (yet).
        # When adding connectors, adapt the minimum size.
        resize_dir_right = resize_dir in ResizeDir.get_corresponding_dir(ResizeDir.RIGHT)
        resize_dir_left = resize_dir in ResizeDir.get_corresponding_dir(ResizeDir.LEFT)
        resize_dir_top = resize_dir in ResizeDir.get_corresponding_dir(ResizeDir.TOP)
        resize_dir_bottom = resize_dir in ResizeDir.get_corresponding_dir(ResizeDir.BOTTOM)

        # Choose the minimum size in a way that there can be no problems when reducing the blocks size.
        w = x2 - x1
        h = y2 - y1
        caption_bbox = self._editor.bbox(self._caption.item_id)
        max_n_inoutputs = max(self._n_inputs, self._n_outputs)
        w_min = max((self._corner_radius + self._connector_size) * 2 + 10, caption_bbox[2] - caption_bbox[0] + (self._corner_radius + self._connector_size) * 2 + 10)
        h_min = max(self._corner_radius * 2 + 10, self._corner_radius * 2 + max_n_inoutputs * self._connector_size + (max_n_inoutputs - 1) * 2)
        diff_x = 0
        diff_y = 0

        if resize_dir_left:
            if dx > 0:
                diff_x = -min((w - dx) - w_min, 0)
            elif dx < 0:
                diff_x = -min((w - dx) - w_min, self._resize_min_size_offset[0])
            # end if

        elif resize_dir_right:
            if dx < 0:
                diff_x = min((w + dx) - w_min, 0)
            elif dx > 0:
                diff_x = min((w + dx) - w_min, -self._resize_min_size_offset[0])
            # end if
        # end if

        dx -= diff_x
        self._resize_min_size_offset[0] += diff_x

        if resize_dir_top:
            if dy > 0:
                diff_y = -min((h - dy) - h_min, 0)
            elif dy < 0:
                diff_y = -min((h - dy) - h_min, self._resize_min_size_offset[1])
            # end if

        elif resize_dir_bottom:
            if dy < 0:
                diff_y = min((h + dy) - h_min, 0)
            elif dy > 0:
                diff_y = min((h + dy) - h_min, -self._resize_min_size_offset[1])
            # end if
        # end if

        dy -= diff_y
        self._resize_min_size_offset[1] += diff_y

        if resize_dir_left:
            x1 += dx

        if resize_dir_top:
            y1 += dy

        if resize_dir_right:
            x2 += dx

        if resize_dir_bottom:
            y2 += dy

        # Create a temp. rounded rectangle to obtain the coords list
        # This is much easier than recalculate each coordinate-point's new position
        id_tmp_rect = self._editor.create_rectangle_rounded(x1, y1, x2, y2, radius=self._corner_radius, state=tk.HIDDEN)
        self._editor.coords(self._frame.item_id, *self._editor.coords(id_tmp_rect))
        self._editor.delete(id_tmp_rect)

        # Label
        self._editor.coords(self._caption.item_id, x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2)

        # Resize-lines
        for resize_line in self._resize_lines:
            _coords = self._get_resize_line_coords(resize_line.dir, x1, y1, x2 - x1, y2 - y1)
            self._editor.coords(resize_line.item_id, *_coords)
        # end for

        # Connectors
        def recalc_pin_positions(pins: List[Pin], conn_dir: ConnDir) -> None:
            for n, pin in enumerate(pins):
                coords = self._get_connect_pin_coords(x1, y1, x2, y2, len(pins), n, conn_dir)
                self._editor.coords(pin.item_id, *coords)

                # Input end of connectors
                if pin.occupied:
                    if conn_dir is ConnDir.IN:
                        pin.conn.update_input_pos(*pin.center_coords)
                    else:
                        pin.conn.update_output_pos(*pin.center_coords)
                    # end if
                # end if
            # end for
        # end def

        # Inputs
        recalc_pin_positions(self._input_pins, ConnDir.IN)

        # Outputs
        recalc_pin_positions(self._output_pins, ConnDir.OUT)
    # end def

    @staticmethod
    def get_block_from_item(item: Item) -> Optional[VBlock]:
        # Item might also be the frame itself

        if item is not None:
            while item.parent is not None:
                item = item.parent
            # end while

            if isinstance(item, Frame):
                return item.parent_block
            # end if
        # end if

        return None
    # end def

    def _on_button_1(self, event: tk.Event) -> None:
        x, y = getattr(event, "x"), getattr(event, "y")

        self._resize_dir = self._is_within_resize_area(x, y)
        pin = self.is_within_connector_area(x, y)
        self._action_base_grid_offset = [self._editor.winfo_pointerx() % self._grid_size,
                                         self._editor.winfo_pointery() % self._grid_size]
        self._action_last_pos_mouse = list(self._editor.winfo_pointerxy())

        if self._resize_dir is not None:
            self._editor.action_mode = Editor.ActionMode.RESIZE

            # Bring the item under the mouse pointer to the top
            self._raise_to_top()

        elif pin is not None:
            self._editor.action_mode = Editor.ActionMode.CONNECT

            if not pin.occupied:
                # Start a new connection
                self._editor.connect_start = pin
                conn = Connection(self._editor, *self._editor.connect_start.center_coords, first_conn_pin=self._editor.connect_start)
                self._editor.connect_start.conn = conn
                self._editor.cur_conn = conn
            else:
                # Open existing connection
                conn = pin.conn
                pin.conn = None
                other_pin = conn.open_connection_at(pin)
                conn.update_open_conn_end(x, y)

                if other_pin is not None:
                    self._editor.connect_start = other_pin
                    self._editor.connect_start.conn = conn
                    self._editor.cur_conn = conn
                # end if
            # end if

            self._do_leave()

        else:
            self._editor.action_mode = Editor.ActionMode.MOVE

            # Bring the item under the mouse pointer to the top (and keep the connector lines always on top)
            self._raise_to_top()
        # end if

        for block in self._editor.blocks:
            block.freeze_highlighting = True
    # end def

    def _on_b1_motion(self, event: tk.Event) -> None:
        x, y = getattr(event, "x"), getattr(event, "y")

        # Adjust mouse position to grid size (so we don't need the Canvas.move()'s gridspacing parameter anymore)
        pointer_x_cur = self._editor.winfo_pointerx() - self._action_base_grid_offset[0] + self._grid_size // 2
        pointer_x_cur = pointer_x_cur // self._grid_size * self._grid_size + self._action_base_grid_offset[0]

        pointer_y_cur = self._editor.winfo_pointery() - self._action_base_grid_offset[1] + self._grid_size // 2
        pointer_y_cur = pointer_y_cur // self._grid_size * self._grid_size + self._action_base_grid_offset[1]

        # Calculate the grid-ed mouse position difference
        dx = pointer_x_cur - self._action_last_pos_mouse[0]
        dy = pointer_y_cur - self._action_last_pos_mouse[1]
        self._action_last_pos_mouse = [pointer_x_cur, pointer_y_cur]

        if self._editor.action_mode is Editor.ActionMode.RESIZE:
            self._resize(self._resize_dir, dx, dy)

        elif self._editor.action_mode is Editor.ActionMode.CONNECT:
            # The connector line is defined to start at the OUT pin and ends at a IN pin.
            # This is necessary to update the line's correct endpoint coordinates during the connection process
            if self._editor.cur_conn is not None:
                self._editor.cur_conn.update_open_conn_end(x, y)
            # end if

        elif self._editor.action_mode is Editor.ActionMode.MOVE:
            # Move rectangle and all its children
            for item in self.items:
                item.move(dx, dy)
            # end for

            for pin in self._input_pins:
                if pin.occupied:
                    pin.conn.update_input_pos(*pin.center_coords)
                # end if
            # end for

            for pin in self._output_pins:
                if pin.occupied:
                    pin.conn.update_output_pos(*pin.center_coords)
                # end if
            # end for

            # Doesn't help regarding the cropping of the rectangle while moving with gridspacing == 1:
            # self.update_idletasks()
        # end if
    # end def

    def do_button_release_1(self, event) -> None:
        self._on_button_release_1(event)
    # end if

    def _on_button_release_1(self, event) -> None:
        x, y = getattr(event, "x"), getattr(event, "y")
        print(self._name)

        if self._editor.action_mode is Editor.ActionMode.RESIZE:
            self._resize_min_size_offset = [0, 0]
            self._resize_dir = None
            self._action_last_pos_mouse = None

        elif self._editor.action_mode is Editor.ActionMode.CONNECT:
            connect_start_block = VBlock.get_block_from_item(self._editor.connect_start)

            if connect_start_block is not self:  # Prevent connecting within the same block
                connect_end = self.is_within_connector_area(x, y)
                if connect_end is not None:
                    if connect_end.occupied:
                        connect_end = None

                    # Don't allow to connect IN with IN or OUT with OUT
                    if self._editor.connect_start and connect_end and \
                            self._editor.connect_start.conn_dir is not connect_end.conn_dir:
                        # Place the end of the connector line in the center of the connector pin
                        self._editor.cur_conn.update_open_conn_end(*connect_end.center_coords)

                        # Assign the connector with the connect-end-pin
                        self._editor.cur_conn.connect(connect_end)
                    # end if
                # end if
            # end if

            # Or delete the temp. connector line if if was not connected properly
            if not self._editor.cur_conn.connected:
                self._editor.cur_conn.dispose()
            # end if

            # Remove handle in editor
            self._editor.cur_conn = None

            # Remove reference os the connect-start-pin
            self._editor.connect_start = None

            connect_start_block._do_leave()

        elif self._editor.action_mode is Editor.ActionMode.MOVE:
            pass
        # end if

        for block in self._editor.blocks:
            block.freeze_highlighting = False
        # end for

        self._editor.action_mode = Editor.ActionMode.NONE
    # end if
# end class


class Editor(tk.Canvas):
    class ActionMode(Enum):
        NONE = auto()
        MOVE = auto()
        RESIZE = auto()
        CONNECT = auto()
    # end class

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self._blocks = list()
        self._items = list()  # A list of all Items created on this editor. Necessary to handle some events.

        self._action_mode = Editor.ActionMode.NONE

        # Connect
        self._cur_conn = None
        self._connect_start = None

        # Special handling for button release event
        # There is a problem with <ButtonRelease-1>: it will return the same item where the corresponding <B1-Motion> happened before,
        # instead of the item under the cursor when releasing the mouse button. That's why we need to hook the button release event.
        self._button_release_1_event_bindings = list()
        self.bind("<ButtonRelease-1>", self._on_button_release_1)
    # end def

    @property
    def blocks(self) -> List[VBlock]:
        return self._blocks
    # end def

    @property
    def items(self) -> List[Item]:
        return self._items
    # end def

    @property
    def cur_conn(self) -> Optional[Connection]:
        return self._cur_conn
    # end def

    @cur_conn.setter
    def cur_conn(self, conn: Optional[Connection]) -> None:
        self._cur_conn = conn
    # end def

    @property
    def action_mode(self) -> Editor.ActionMode:
        return self._action_mode
    # end def

    @action_mode.setter
    def action_mode(self, action_mode: Editor.ActionMode) -> None:
        self._action_mode = action_mode
    # end def

    @property
    def connect_start(self) -> Pin:
        return self._connect_start
    # end def

    @connect_start.setter
    def connect_start(self, pin: Pin) -> None:
        self._connect_start = pin
    # end def

    def tag_bind(self, tagOrId, sequence=None, func=None, add=None):
        if sequence == "<ButtonRelease-1>":
            if not add:  # Delete all old ones
                for i in reversed(range(len(self._button_release_1_event_bindings))):
                    if self._button_release_1_event_bindings[i][0] == tagOrId:
                        self._button_release_1_event_bindings.pop(i)
                    # end if
                # end for
            # end if
            self._button_release_1_event_bindings.append((tagOrId, func))

        else:
            super().tag_bind(tagOrId, sequence, func, add)
        # end if
    # end if

    def _on_button_release_1(self, event) -> None:
        x, y = getattr(event, "x"), getattr(event, "y")

        item_ids_under_cursor = list(reversed(self.find_overlapping(x, y, x, y)))

        if len(item_ids_under_cursor) > 0:
            item_id = item_ids_under_cursor[0]

            for tag, cb in self._button_release_1_event_bindings:
                if tag == item_id:
                    cb(event)
                # end if
            # end for
        # end if
    # end def

    def add_item(self, item: Item) -> None:
        self._items.append(item)
    # end def

    def get_item_by_id(self, item_id) -> Optional[Item]:
        for item in self._items:
            if item.item_id == item_id:
                return item
            # end if
        # end for

        return None
    # end der

    def add_block(self, name: str, n_inputs: int, n_outputs: int, x: float, y: float, width: float, height: float) -> None:
        block = VBlock(self, name, n_inputs=n_inputs, n_outputs=n_outputs, x=x, y=y, width=width, height=height)
        self._blocks.append(block)
    # end def

    @staticmethod
    def hex2rgb(str_rgb) -> Tuple[int, int, int]:
        try:
            rgb = str_rgb[1:]

            if len(rgb) == 6:
                r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
            elif len(rgb) == 3:
                r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
            else:
                raise ValueError()
        except Exception:
            raise ValueError("Invalid value %r provided for rgb color." % str_rgb)

        return int(r, 16), int(g, 16), int(b, 16)
    # end def

    def _on_configure(self, event) -> None:
        width = event.width
        height = event.height
        orient = tk.HORIZONTAL
        steps = None
        from_color = "#D0D3D4"
        to_color = "#FFFFFF"

        if steps is None:
            if orient == tk.HORIZONTAL:
                steps = height
            else:
                steps = width

        if isinstance(from_color, str):
            from_color = self.hex2rgb(from_color)

        if isinstance(to_color, str):
            to_color = self.hex2rgb(to_color)

        r, g, b = from_color
        dr = float(to_color[0] - r) / steps
        dg = float(to_color[1] - g) / steps
        db = float(to_color[2] - b) / steps

        img_height = height
        img_width = width

        image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
        draw = ImageDraw.Draw(image)

        if orient == tk.HORIZONTAL:
            for i in range(steps):
                r, g, b = r + dr, g + dg, b + db
                y0 = int(float(img_height * i) / steps)
                y1 = int(float(img_height * (i + 1)) / steps)

                draw.rectangle((0, y0, img_width, y1), fill=(int(r), int(g), int(b)))
            # end for

        else:
            for i in range(steps):
                r, g, b = r + dr, g + dg, b + db
                x0 = int(float(img_width * i) / steps)
                x1 = int(float(img_width * (i + 1)) / steps)

                draw.rectangle((x0, 0, x1, img_height), fill=(int(r), int(g), int(b)))
            # end for

        self._gradient_photo_image = ImageTk.PhotoImage(image)

        x = self.create_image(0, 0, anchor=tk.NW, image=self._gradient_photo_image)
        self.lower(x)
    # end def

    def create_rectangle_rounded(self, x1: float, y1: float, x2: float, y2: float, radius: float = 25., **kwargs) -> int:
        points = [x1 + radius * 2, y1,
                  x2 - radius * 2, y1,
                  x2, y1,
                  x2, y1 + radius * 2,
                  x2, y2 - radius * 2,
                  x2, y2,
                  x2 - radius * 2, y2,
                  x1 + radius * 2, y2,
                  x1, y2,
                  x1, y2 - radius * 2,
                  x1, y1 + radius * 2,
                  x1, y1]

        return self.create_polygon(points, **kwargs, smooth=True)
    # end def
# end class


class Gui:
    def __init__(self) -> None:
        self._root = tk.Tk()
        self._root.geometry(f"{500}x{500}")

        self._editor = Editor(bg="white")
        self._editor.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

        # Horizontal separator
        sep_hor = tk.Frame(self._root, height=2, bd=1, relief=tk.SUNKEN)
        sep_hor.pack(expand=False, fill=tk.X, side=tk.TOP, pady=5)

        self._visu = tk.Canvas()
        self._visu.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        self._visu.bind("<Configure>", self._on_visu_configure)

        # --

        self._image = None
        self._image_mod = None
    # end def

    def load_test(self) -> None:
        self._editor.add_block(name="test1", n_inputs=3, n_outputs=5, x=10, y=30, width=180, height=400)
        self._editor.add_block(name="test2", n_inputs=5, n_outputs=4, x=310, y=50, width=250, height=300)
    # end def

    def _on_visu_configure(self, _event: tk.Event) -> None:
        self._show_image()
    # end def

    def show_image(self, image: np.ndarray) -> None:
        self._image = image

        self._show_image()
    # end def

    def _show_image(self) -> None:
        if self._image is not None:
            min_val = np.min(self._image)
            max_val = np.max(self._image)

            # We need to keep the original image unmodified to know the values
            # (which can also be of negative value or larger than 255).
            image_mod = Image.fromarray((self._image - min_val) * (255. / (max_val - min_val)))

            # Calculate ratios and size
            canvas_width = self._visu.winfo_width()
            canvas_height = self._visu.winfo_height()
            canvas_ratio = canvas_width / canvas_height

            image_width = self._image.shape[1]
            image_height = self._image.shape[0]
            image_ratio = image_width / image_height

            if canvas_ratio > image_ratio:
                scale = canvas_height / image_height
            else:
                scale = canvas_width / image_width
            # end if

            width = int(image_mod.size[0] * scale)
            height = int(image_mod.size[1] * scale)

            if width >= 1 and height >= 1:
                image_mod = image_mod.resize((width, height), Image.ANTIALIAS)

                # This reference needs to hold, otherwise there will no image be displayed.
                self._image_mod = ImageTk.PhotoImage(image_mod)
                self._visu.create_image((canvas_width - width) // 2, (canvas_height - height) // 2, anchor=tk.NW,
                                        image=self._image_mod)
            # end if
        # end if
    # end def

    @staticmethod
    def run() -> None:
        tk.mainloop()
    # end if
# end class


if __name__ == "__main__":
    gui = Gui()
    gui.load_test()
    gui.run()
# end if
