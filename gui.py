from __future__ import annotations
from typing import Optional, Union, Tuple, List
import numpy as np
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from enum import Enum, auto

from templates.block import IdGenerator


__author__ = "Anton Höß"
__copyright__ = "Copyright 2021"


class ResizeDir(Enum):
    TOP = auto()
    TOP_RIGHT = auto()
    RIGHT = auto()
    BOTTOM_RIGHT = auto()
    BOTTOM = auto()
    BOTTOM_LEFT = auto()
    LEFT = auto()
    TOP_LEFT = auto()
# end class


class ConnDir(Enum):
    IN = auto()
    OUT = auto()
# end class


class Editor(tk.Canvas):
    class SrcDstType(Enum):
        TAG_ID = auto()
        MASTER_TAG = auto()
        GROUP_TAG = auto()
        MASTER_ID = auto()
        # XXX What about the current object id (tk.CURRENT)? It might reduce nested expressions.
        # XXX What about the id of a certain object in the group ?
    # end class

    class ActionMode(Enum):
        NONE = auto()
        MOVE = auto()
        RESIZE = auto()
        CONNECT = auto()
    # end class

    class ConnectInfo:
        def __init__(self, inout_dir: ConnDir, idx: int, item_id, center_coords: Tuple[int, int], occupied: bool):
            self.inout_dir = inout_dir
            self.idx = idx
            self.center_coords = center_coords
            self.item_id = item_id
            self.occupied = occupied
        # end def
    # end class

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._id_gen = IdGenerator()
        self._blocks = dict()

        # Common variables for multiple actions
        self._grid_size = 10
        self._action_mode = Editor.ActionMode.NONE
        self._action_base_grid_offset = None
        self._action_last_pos_mouse = None

        # Move
        self._move_tag_id = None
        self._move_group_tag = None

        # Resize
        self._resize_tag_id = None
        self._resize_group_tag = None
        self._resize_dir = None

        # Connect
        self._connect_start = None
        self._connect_line_id = None
        self._connect_start_block = None

        self.bind("<Configure>", self._on_configure)
        self.bind("<Button-1>", self._on_button_1)
        self.bind("<ButtonRelease-1>", self._on_button_release_1)
        self.bind("<B1-Motion>", self._on_b1_motion)
    # end def

    @staticmethod
    def hex2rgb(str_rgb):
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

        return tuple(int(v, 16) for v in (r, g, b))
    # end def

    def _on_configure(self, event):
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

    # XXX Rename this function
    def _resolve(self, src: Union[int, str], src_type: SrcDstType, dst_type: SrcDstType) -> Optional[Union[int, str]]:
        master_id = None  # This is the central information (i.e. the bridge between source and destination)

        # Step I: Resolve the source
        # --------------------------
        if src_type in (Editor.SrcDstType.TAG_ID, Editor.SrcDstType.MASTER_TAG, Editor.SrcDstType.GROUP_TAG):
            master_tag = None

            if src_type is Editor.SrcDstType.TAG_ID:
                master_tag = "x" + src

            elif src_type is Editor.SrcDstType.MASTER_TAG:
                master_tag = src

            elif src_type is Editor.SrcDstType.GROUP_TAG:
                found = False
                group_objects_ids = self.find_withtag(src)

                for group_objects_id in group_objects_ids:
                    if found:
                        break

                    tags = self.gettags(group_objects_id)

                    for tag in tags:
                        if tag[0] == "x":
                            found = True
                            master_tag = tag
                            break
                        # end if
                    # end for
                # end for
            # end if

            ids = self.find_withtag(master_tag)

            if len(ids) == 1:
                master_id = ids[0]

        elif src_type is Editor.SrcDstType.MASTER_ID:
            master_id = src
        # end if

        if master_id is None:
            return None

        # Step II: Resolve the destination
        # --------------------------------
        if dst_type in (Editor.SrcDstType.TAG_ID, Editor.SrcDstType.MASTER_TAG, Editor.SrcDstType.GROUP_TAG):
            master_tag = None

            tags = self.gettags(master_id)

            for tag in tags:
                if tag[0] == "x":
                    master_tag = self.find_withtag(tag)
                    return
                # end if
            # end for

            if dst_type is Editor.SrcDstType.TAG_ID:
                return master_tag[1:]

            elif dst_type is Editor.SrcDstType.MASTER_TAG:
                return master_tag

            elif dst_type is Editor.SrcDstType.GROUP_TAG:
                return "g" + master_tag[1:]

        elif dst_type is Editor.SrcDstType.MASTER_ID:
            return master_id
        # end if

        return None
    # end def

    def get_current_object_id(self):
        object_ids = self.find_withtag(tk.CURRENT)

        if len(object_ids) == 1:
            return object_ids[0]
        else:
            return None
        # end if
    # end def

    def get_tag_id(self, object_id: Optional[int]):
        if object_id is not None:
            tags = [tag for tag in self.gettags(object_id) if tag[0] == "g"]

            if len(tags) > 0:
                return tags[0][1:]
        # end if

        return None
    # end def

    def get_group_tag(self, object_id: Optional[int]):
        if object_id is not None:
            tags = [tag for tag in self.gettags(object_id) if tag[0] == "g"]

            if len(tags) > 0:
                return tags[0]
        # end if

        return None
    # end def

    def get_master_tag_id_from_group_tag(self, group_tag: Optional[str]) -> Optional[str]:
        if group_tag is not None:
            group_object_ids = self.find_withtag(group_tag)

            for group_object_id in group_object_ids:
                tags = self.gettags(group_object_id)

                for tag in tags:
                    if tag[0] == "x":
                        return tag[1:]
                    # end if
                # end for
            # end for
        # end if

        return None
    # end def

    def get_master_tag_from_group_tag(self, group_tag: Optional[str]):
        group_object_ids = self.find_withtag(group_tag)

        for group_object_id in group_object_ids:
            tags = self.gettags(group_object_id)

            for tag in tags:
                if tag[0] == "x":
                    return tag
                # end if
            # end for
        # end for

        return None
    # end def

    def get_master_id_from_group_tag(self, group_tag: Optional[str]):
        group_object_ids = self.find_withtag(group_tag)

        for group_object_id in group_object_ids:
            tags = self.gettags(group_object_id)

            for tag in tags:
                if tag[0] == "x":
                    return group_object_id
                # end if
            # end for
        # end for

        return None
    # end def

    def _on_button_1(self, event):
        x, y = getattr(event, "x"), getattr(event, "y")

        cur_obj_id = self.get_current_object_id()
        group_tag = self.get_group_tag(cur_obj_id)

        if group_tag is not None:
            block = self.get_block_by_canvas_object_tag_id(self.get_master_tag_id_from_group_tag(group_tag))
            self._resize_dir = block.is_within_resize_area(x, y)
            self._connect_start = block.is_within_connector_area(x, y)
            self._action_base_grid_offset = [self.winfo_pointerx() % self._grid_size, self.winfo_pointery() % self._grid_size]
            self._action_last_pos_mouse = list(self.winfo_pointerxy())

            if self._resize_dir is not None:
                self._action_mode = Editor.ActionMode.RESIZE
                self._resize_tag_id = self.get_tag_id(cur_obj_id)
                self._resize_group_tag = group_tag

                # Bring the item under the mouse pointer to the top
                self.tag_raise(self._resize_group_tag)

            elif self._connect_start is not None:
                if self._connect_start.occupied:
                    self._connect_start = None
                    return
                # end if
                self._action_mode = Editor.ActionMode.CONNECT
                x_center, y_center = self._connect_start.center_coords
                self._connect_line_id = self.create_line(x_center, y_center, x_center, y_center, width=2, fill="blue")
                self._connect_start_block = block

            else:
                self._action_mode = Editor.ActionMode.MOVE
                self._move_tag_id = self.get_tag_id(cur_obj_id)
                self._move_group_tag = group_tag

                for block in self._blocks.values():
                    block.freeze_highlighting = True

                # Bring the item under the mouse pointer to the top
                self.tag_raise(self._move_group_tag)
                # ... and keep the connector lines always on top
                for item in self.find_withtag(self._move_group_tag):
                    for tag in self.gettags(item):
                        if tag.startswith("c"):
                            self.tag_raise(tag[1:])
                    # end for
                # end for
            # end if
        # end if
    # end def

    def _on_b1_motion(self, event):
        x, y = getattr(event, "x"), getattr(event, "y")

        # Adjust mouse position to grid size (so we don't need the Canvas.move()'s gridspacing parameter anymore)
        pointer_x_cur = self.winfo_pointerx() - self._action_base_grid_offset[0] + self._grid_size // 2
        pointer_x_cur = pointer_x_cur // self._grid_size * self._grid_size + self._action_base_grid_offset[0]

        pointer_y_cur = self.winfo_pointery() - self._action_base_grid_offset[1] + self._grid_size // 2
        pointer_y_cur = pointer_y_cur // self._grid_size * self._grid_size + self._action_base_grid_offset[1]

        # Calculate the grid-ed mouse position difference
        dx = pointer_x_cur - self._action_last_pos_mouse[0]
        dy = pointer_y_cur - self._action_last_pos_mouse[1]
        self._action_last_pos_mouse = [pointer_x_cur, pointer_y_cur]

        if self._action_mode is Editor.ActionMode.RESIZE:
            block = self.get_block_by_canvas_object_tag_id(self._resize_tag_id)
            block.resize(self._resize_dir, dx, dy)

        elif self._action_mode is Editor.ActionMode.CONNECT:
            # The connector line is defined to start at the OUT pin and ends at a IN pin.
            # This is necessary to update the line's correct endpoint coordinates  during the connection process
            self.move_connector_line_end(self._connect_line_id, self._connect_start.inout_dir, x, y)

        elif self._action_mode is Editor.ActionMode.MOVE:
            # Move rectangle and pins
            self.move(self._move_group_tag, dx, dy)

            def get_conn_ids(tag_indicator: str) -> List[int]:
                pin_ids = list()

                for pin in self.find_withtag(self._move_group_tag):
                    found = False

                    for tag in self.gettags(pin):
                        if found:
                            break

                        if tag.startswith(tag_indicator):  # In- or Out-pin
                            for conn_tag in self.gettags(pin):
                                if conn_tag.startswith("c"):  # Is already connected?
                                    pin_ids.append(int(conn_tag[1:]))
                                    found = True
                                    break
                                # end if
                            # end for
                        # end if
                    # end for
                # end if

                return pin_ids
            # end def

            # Move connector lines
            conn_ids = get_conn_ids("i")
            for conn_id in conn_ids:
                coords = list(self.coords(conn_id))
                coords[2] += dx
                coords[3] += dy
                self.coords(conn_id, *coords)
            # end for

            conn_ids = get_conn_ids("o")
            for conn_id in conn_ids:
                coords = list(self.coords(conn_id))
                coords[0] += dx
                coords[1] += dy
                self.coords(conn_id, *coords)
            # end for

            # Doesn't help regarding the cropping of the rectangle while moving with gridspacing == 1:
            # self.update_idletasks()
        # end if
    # end def

    def move_connector_line_end(self, connector_line_id: int, conn_dir: ConnDir, x: float, y: float):
        coords = list(self.coords(connector_line_id))

        if conn_dir is ConnDir.OUT:
            coords[2] = x
            coords[3] = y
        else:
            coords[0] = x
            coords[1] = y
        # end if

        self.coords(connector_line_id, *coords)

    # end def

    def _on_button_release_1(self, event):
        x, y = getattr(event, "x"), getattr(event, "y")

        if self._action_mode is Editor.ActionMode.RESIZE:
            block = self.get_block_by_canvas_object_tag_id(self._resize_tag_id)
            block._resize_min_size_offset = [0, 0]
            self._resize_tag_id = None
            self._resize_group_tag = None
            self._resize_dir = None
            self._action_last_pos_mouse = None

        elif self._action_mode is Editor.ActionMode.CONNECT:
            # Retrieve the current topmost block under the cursor.
            # We have to do it this complicated way, since the currently drawn connector line blocks the
            # cursor's 'view' to the current item under the cursor.
            items_under_cursor = reversed(self.find_overlapping(x, y, x, y))

            # Ignore the line object (which is always under the mouse cursor),
            # since we want the underlying connector rectangle
            cur_obj_id = None
            found = False
            for item in items_under_cursor:
                if found:
                    break

                all_tags = self.gettags(item)
                for t in all_tags:
                    if t.startswith("x"):
                        cur_obj_id = item
                        found = True
                        break
                    # end if
                # end for
            # end for

            group_tag = self.get_group_tag(cur_obj_id)

            # Check if the mouse was released under a (valid) connector
            success = False

            if group_tag is not None:
                block = self.get_block_by_canvas_object_tag_id(self.get_master_tag_id_from_group_tag(group_tag))
                # Don't allow to connect within the same block
                if block is not self._connect_start_block:
                    connect_end = block.is_within_connector_area(x, y)
                    if connect_end.occupied:
                        connect_end = None

                    # Don't allow to connect IN with IN or OUT with OUT
                    if self._connect_start and connect_end and \
                            self._connect_start.inout_dir is not connect_end.inout_dir:
                        # Place the end of the connector line in the center of the connector pin
                        self.move_connector_line_end(self._connect_line_id, self._connect_start.inout_dir, *connect_end.center_coords)

                        # Assign the connector line ID to the corresponding block pins
                        self.addtag_withtag(f"c{self._connect_line_id}", self._connect_start.item_id)
                        self.addtag_withtag(f"c{self._connect_line_id}", connect_end.item_id)

                        success = True
                    # end if
                # end if
            # end if

            # Or delete the temp. connector line if if was not connected properly
            if not success:
                self.delete(self._connect_line_id)
            # end if

            self._connect_start = None
            self._connect_line_id = None
            self._connect_start_block = None

        elif self._action_mode is Editor.ActionMode.MOVE:
            if self._move_tag_id != self.get_tag_id(self.get_current_object_id()):
                block = self.get_block_by_canvas_object_tag_id(self._move_tag_id)
                if block is not None:
                    block.do_leave()
            # end if

            for block in self._blocks.values():
                if block.freeze_highlighting:
                    block.freeze_highlighting = False
            # end for
        # end if

        self._action_mode = Editor.ActionMode.NONE
        self._move_group_tag = None
    # end if

    def get_block_by_canvas_object_tag_id(self, canvas_object_tag: str) -> VBlock:
        return self._blocks.get(canvas_object_tag)
    # end def

    def add(self, name: str, n_inputs: int, n_outputs: int, x: float, y: float, width: float, height: float):
        tag_id = self._id_gen.new_id(length=4)
        block = VBlock(self, name, tag_id=tag_id, n_inputs=n_inputs, n_outputs=n_outputs, x=x, y=y, width=width, height=height)
        self._blocks[tag_id] = block
    # end def

    def create_rectangle_rounded(self, x1, y1, x2, y2, radius=25, **kwargs):
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


# The main rectangle has its own tag and all elements that belong to the block
# (incl. the base rectangle) get a group tag
class VBlock:
    def __init__(self, editor: Editor, name: str, tag_id: str, n_inputs: int, n_outputs: int, x: float, y: float,
                 width: float, height: float, corner_radius: int = 12, connector_size: int = 10):
        self._editor = editor
        self._name = name

        self._n_inputs = n_inputs
        self._n_outputs = n_outputs

        self._corner_radius = corner_radius
        self._connector_size = connector_size

        self._freeze_highlighting = False
        self._resize_min_size_offset = [0, 0]

        # Draw block and assign tags
        ############################
        # Since there might be UUID's that include only decimals and tkinter doesn't allow this, we need to add some
        # string at the beginning to distinguish these numbers from canvas object IDs.
        self._tag = "x" + tag_id
        self._group_tag = "g" + tag_id  # The (the group of) all elements that are parts of this block

        # Rectangle
        self._object_id = self._editor.create_rectangle_rounded(x, y, x + width, y + height, self._corner_radius,
                                                                outline="blue", width=1, tag=self._tag)

        self._editor.addtag_withtag(self._group_tag, self._object_id)

        # Label
        self._object_id_text = self._editor.create_text(x + width // 2, y + height // 2,  font=("Arial", 20, "normal"),
                                                        fill="black", text=name)
        self._editor.addtag_withtag(self._group_tag, self._object_id_text)

        # Resize-lines
        self._resize_lines = list()
        self._resize_lines.append(
            self._editor.create_line(x, y + self._corner_radius,
                                     x + width, y + self._corner_radius, fill="blue"))  # Top
        self._resize_lines.append(
            self._editor.create_line(x + width - self._corner_radius, y,
                                     x + width - self._corner_radius, y + height, fill="blue"))  # Right
        self._resize_lines.append(
            self._editor.create_line(x, y + height - self._corner_radius,
                                     x + width, y + height - self._corner_radius, fill="blue"))  # Bottom
        self._resize_lines.append(
            self._editor.create_line(x + self._corner_radius, y,
                                     x + self._corner_radius, y + height, fill="blue"))  # Left

        # Connectors
        connector_dist = (height - 2 * self._corner_radius - self._n_inputs * self._connector_size) / (self._n_inputs - 1)
        for n in range(self._n_inputs):
            input_conn = self._editor.create_rectangle(
                x + self._corner_radius,
                y + self._corner_radius + n * (connector_dist + self._connector_size),
                x + self._corner_radius + self._connector_size,
                y + self._corner_radius + n * connector_dist + (n + 1) * self._connector_size,
                outline="blue")
            self._editor.addtag_withtag(self._group_tag, input_conn)
            self._editor.addtag_withtag(f"i{n}", input_conn)
        # end for

        connector_dist = (height - 2 * self._corner_radius - self._n_outputs * self._connector_size) / (self._n_outputs - 1)
        for n in range(self._n_outputs):
            output_conn = self._editor.create_rectangle(
                x + width - self._corner_radius,
                y + self._corner_radius + n * (connector_dist + self._connector_size),
                x + width - (self._corner_radius + self._connector_size),
                y + self._corner_radius + n * connector_dist + (n + 1) * self._connector_size,
                outline="blue")
            self._editor.addtag_withtag(self._group_tag, output_conn)
            self._editor.addtag_withtag(f"o{n}", output_conn)
        # end for

        for resize_line in self._resize_lines:
            self._editor.addtag_withtag(self._group_tag, resize_line)
            self._editor.itemconfigure(resize_line, state=tk.HIDDEN)
        # end for

        # Hide elements that are only shown when the mouse hovers over the block
        self.do_leave()

        # Use unique tag in function
        self._editor.tag_bind(self._group_tag, "<Enter>",
                              lambda event, tag=self._tag: self.on_enter_or_leave(event, tag))
        self._editor.tag_bind(self._group_tag, "<Leave>",
                              lambda event, tag=self._tag: self.on_enter_or_leave(event, tag))
    # end if

    @property
    def corner_radius(self):
        return self._corner_radius
    # end def

    @property
    def object_id(self):
        return self._object_id
    # end def

    @property
    def freeze_highlighting(self):
        return self._freeze_highlighting
    # end def

    @freeze_highlighting.setter
    def freeze_highlighting(self, value):
        self._freeze_highlighting = value
    # end def

    def do_enter(self):
        self._editor.itemconfig(self._object_id, fill="orange")

        for resize_line in self._resize_lines:
            self._editor.itemconfigure(resize_line, state=tk.NORMAL)
        # end for
    # end for

    def do_leave(self):
        self._editor.itemconfig(self._object_id, fill="light blue")

        for resize_line in self._resize_lines:
            self._editor.itemconfigure(resize_line, state=tk.HIDDEN)
        # end for
    # end for

    def on_enter_or_leave(self, event: tk.Event, _tag):
        if self._editor._action_mode is not Editor.ActionMode.RESIZE:
            if not self._freeze_highlighting:
                if getattr(event, "type") == tk.EventType.Enter:
                    self.do_enter()
                elif getattr(event, "type") == tk.EventType.Leave:
                    self.do_leave()
                # end if
            # end if
        # end if
    # end def

    def is_within_resize_area(self, pos_x: int, pos_y: int) -> Optional[ResizeDir]:
        x1, y1, x2, y2 = self.get_bbox()
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

    def is_within_connector_area(self, pos_x: int, pos_y: int) -> Optional[Editor.ConnectInfo]:
        def is_within_connector_group_area(conn_dir: ConnDir) -> Optional[Editor.ConnectInfo]:
            tag_indicator = "i" if conn_dir is ConnDir.IN else "o"

            for block_part_id in self._editor.find_withtag(self._group_tag):
                n = -1
                pin_is_occupied = False

                for block_part_tag in self._editor.gettags(block_part_id):
                    if block_part_tag.startswith(tag_indicator):  # It is a pin
                        n = int(block_part_tag[1:])

                        # Check if pin is already occupied
                        pin_is_occupied = any([x.startswith("c") for x in self._editor.gettags(block_part_id)])

                        break
                    # end if
                # end for

                if n >= 0:
                    x1, y1, x2, y2 = self._editor.coords(block_part_id)

                    if x1 <= pos_x <= x2 and y1 <= pos_y <= y2:
                        return Editor.ConnectInfo(inout_dir=conn_dir, idx=n, item_id=block_part_id,
                                                  center_coords=((x2 + x1) // 2, (y2 + y1) // 2),
                                                  occupied=pin_is_occupied)
                    # end if
                # end if
            # end for

            return None
        # end def

        res = is_within_connector_group_area(ConnDir.IN)
        if res is not None:
            return res

        res = is_within_connector_group_area(ConnDir.OUT)
        if res is not None:
            return res

        return None
    # end def

    # We need to use this complicated way since bbox() returns a bbox too big
    # as it considers also the rectangles line width
    def get_bbox(self) -> Tuple[int, int, int, int]:
        coords = self._editor.coords(self._object_id)
        x1, y1, x2, y2 = min(coords[::2]), min(coords[1::2]), max(coords[::2]), max(coords[1::2])

        return x1, y1, x2, y2
    # end def

    def resize(self, resize_dir: ResizeDir, dx: int, dy: int) -> None:
        # Get old rectangle
        x1, y1, x2, y2 = self.get_bbox()

        # XXX Choose the minimum size in a way that there can be no problems when reducing the blocks size.
        # There needs to be guaranteed a minimum size even if there are no connectors placed (yet).
        # When adding connectors, adapt the minimum size.
        resize_dir_right = resize_dir in (ResizeDir.RIGHT, ResizeDir.TOP_RIGHT, ResizeDir.BOTTOM_RIGHT)
        resize_dir_left = resize_dir in (ResizeDir.LEFT, ResizeDir.TOP_LEFT, ResizeDir.BOTTOM_LEFT)
        resize_dir_top = resize_dir in (ResizeDir.TOP, ResizeDir.TOP_LEFT, ResizeDir.TOP_RIGHT)
        resize_dir_bottom = resize_dir in (ResizeDir.BOTTOM, ResizeDir.BOTTOM_LEFT, ResizeDir.BOTTOM_RIGHT)

        # XXX Static test values
        w = x2 - x1
        h = y2 - y1
        w_min = 50
        h_min = 150  # XXX Set the size in dependence of the number of connectors
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
        self._editor.coords(self._object_id, *self._editor.coords(id_tmp_rect))
        self._editor.delete(id_tmp_rect)

        # Label
        self._editor.coords(self._object_id_text, x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2)

        # Resize-lines
        # XXX On fast movements (one might need several tries) which reduces the size of the block (exceeding its
        # minimal size) it might happen that one vertical line stays in a place where it doesn't belong
        def resize_resize_lines(x_positive: Optional[bool], y_positive: Optional[bool]) -> None:
            for resize_line_id in self._resize_lines:
                _coords = self._editor.coords(resize_line_id)

                if x_positive is not None:
                    for k in (0, 2):
                        if x_positive == (_coords[k] > x1 + (x2 - x1) // 2):
                            _coords[k] += dx
                    # end for
                # end if

                if y_positive is not None:
                    for k in (1, 3):
                        if y_positive == (_coords[k] > y1 + (y2 - y1) // 2):
                            _coords[k] += dy
                    # end for
                # end if

                self._editor.coords(resize_line_id, *_coords)
            # end for
        # end def

        if resize_dir_left:
            resize_resize_lines(x_positive=False, y_positive=None)

        if resize_dir_top:
            resize_resize_lines(x_positive=None, y_positive=False)

        if resize_dir_right:
            resize_resize_lines(x_positive=True, y_positive=None)

        if resize_dir_bottom:
            resize_resize_lines(x_positive=None, y_positive=True)

        # Connectors
        # XXX Eliminate double code (by using helper functions)
        height = y2 - y1
        width = x2 - x1

        # Inputs
        connector_dist = (height - 2 * self._corner_radius - self._n_inputs * self._connector_size) / (self._n_inputs - 1)
        for inp in self._editor.find_withtag(self._group_tag):
            n = -1
            for tag in self._editor.gettags(inp):
                if tag.startswith("i"):
                    n = int(tag[1:])
                    break
                # end if
            # end for

            if n >= 0:
                coords = [x1 + self._corner_radius,
                          y1 + self._corner_radius + n * (connector_dist + self._connector_size),
                          x1 + self._corner_radius + self._connector_size,
                          y1 + self._corner_radius + n * connector_dist + (n + 1) * self._connector_size]
                self._editor.coords(inp, *coords)

                # Input end of connectors
                for tag in self._editor.gettags(inp):
                    if tag.startswith("c"):
                        conn_id = tag[1:]
                        coords_conn = self._editor.coords(conn_id)
                        coords_conn[2] = coords[0] + self._connector_size // 2
                        coords_conn[3] = coords[1] + self._connector_size // 2
                        self._editor.coords(conn_id, *coords_conn)
                        self._editor.tag_raise(conn_id)
                    # end if
                # end for
            # end if
        # end for

        # Outputs
        connector_dist = (height - 2 * self._corner_radius - self._n_outputs * self._connector_size) / (self._n_outputs - 1)
        for outp in self._editor.find_withtag(self._group_tag):
            n = -1
            for tag in self._editor.gettags(outp):
                if tag.startswith("o"):
                    n = int(tag[1:])
                    break
                # end if
            # end for

            if n >= 0:
                coords = [x1 + width - self._corner_radius - self._connector_size,
                          y1 + self._corner_radius + n * (connector_dist + self._connector_size),
                          x1 + width - self._corner_radius,
                          y1 + self._corner_radius + n * connector_dist + (n + 1) * self._connector_size]
                self._editor.coords(outp, *coords)

                # Output end of connectors
                for tag in self._editor.gettags(outp):
                    if tag.startswith("c"):
                        conn_id = tag[1:]
                        coords_conn = self._editor.coords(conn_id)
                        coords_conn[0] = coords[0] + self._connector_size // 2
                        coords_conn[1] = coords[1] + self._connector_size // 2
                        self._editor.coords(conn_id, *coords_conn)
                        self._editor.tag_raise(conn_id)
                    # end if
                # end for
            # end if
        # end for
    # end def
# end class


class Gui:
    def __init__(self):
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

    def load_test(self):
        self._editor.add(name="test1", n_inputs=5, n_outputs=2, x=10, y=10, width=200, height=300)
        self._editor.add(name="test2", n_inputs=10, n_outputs=10, x=110, y=30, width=200, height=400)
    # end def

    def _on_visu_configure(self, event: tk.Event):
        self._show_image()
    # end def

    def show_image(self, image: np.ndarray) -> None:
        self._image = image

        self._show_image()
    # end def

    def _show_image(self):
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
    def run():
        tk.mainloop()
    # end if
# end class


if __name__ == "__main__":
    gui = Gui()
    gui.load_test()
    gui.run()
# end if
