from __future__ import annotations
from typing import Optional
import numpy as np
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

from templates.block import IdGenerator


__author__ = "Anton Höß"
__copyright__ = "Copyright 2021"


class Editor(tk.Canvas):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._id_gen = IdGenerator()
        self._blocks = dict()

        # Move
        self._move_mode = False
        self._move_master_tag = None
        self._move_group_tag = None
        self._move_start_pos_block = None
        self._move_start_pos_mouse = None

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

    def get_current_object(self):
        object_ids = self.find_withtag(tk.CURRENT)

        if len(object_ids) == 1:
            return object_ids[0]
        else:
            return None
        # end if
    # end def

    def get_master_tag(self, object_id):
        tags = [tag for tag in self.gettags(object_id) if tag[0] == "g"]

        if len(tags) > 0:
            return tags[0][1:]
        else:
            return None
        # end if
    # end def

    def get_group_tag(self, object_id):
        tags = [tag for tag in self.gettags(object_id) if tag[0] == "g"]

        if len(tags) > 0:
            return tags[0]
        else:
            return None
        # end if
    # end def

    def get_master_id_from_group_tag(self, group_tag: Optional[str]):
        if group_tag is not None:
            tags = self.gettags(group_tag)

            for tag in tags:
                if tag[0] == "x":
                    return self.find_withtag(tag)
                # end if
            # end for
        # end if

        return None
    # end def

    def _on_button_1(self, _event):
        group_tag = self.get_group_tag(self.get_current_object())

        if group_tag is not None:
            self._move_mode = True
            self._move_master_tag = self.get_master_tag(self.get_current_object())
            self._move_group_tag = group_tag

            for block in self._blocks.values():
                block.freeze_highlighting = True

            # Bring the item under the mouse pointer to the top
            self.tag_raise(self._move_group_tag)

            self._move_start_pos_block = self.bbox(group_tag)[:2]
            self._move_start_pos_mouse = self.winfo_pointerxy()
        # end if
    # end def

    def _on_b1_motion(self, _event):
        if self._move_mode and self._move_group_tag is not None:
            pointer_x_start, pointer_y_start = self._move_start_pos_mouse
            pointer_x_cur, pointer_y_cur = self.winfo_pointerxy()
            block_pos_x_start, block_pos_y_start = self._move_start_pos_block
            block_pos_x_cur, block_pos_y_cur = self.bbox(self._move_group_tag)[:2]

            self.move(self._move_group_tag,
                      self.canvasx(pointer_x_cur - pointer_x_start, gridspacing=10) - (block_pos_x_cur - block_pos_x_start),
                      self.canvasy(pointer_y_cur - pointer_y_start, gridspacing=10) - (block_pos_y_cur - block_pos_y_start))

            # Doesn't help regarding the cropping of the rectangle while moving with gridspacing == 1:
            # self.update_idletasks()
        # end if
    # end def

    def _on_button_release_1(self, _event):
        if self._move_master_tag != self.get_master_tag(self.get_current_object()):
            block = self.get_block_by_canvas_object_tag(self._move_master_tag)
            if block is not None:
                block.do_leave()
        # end if

        self._move_mode = False
        self._move_group_tag = None

        for block in self._blocks.values():
            if block.freeze_highlighting:
                block.freeze_highlighting = False
    # end if

    def get_block_by_canvas_object_tag(self, canvas_object_tag: int):
        return self._blocks.get(canvas_object_tag)
    # end def

    def add(self, name: str, n_inputs: int, n_outputs: int, x: float, y: float, width: float, height: float):
        block_tag = self._id_gen.new_id(length=4)
        block = VBlock(self, name, tag_id=block_tag, n_inputs=n_inputs, n_outputs=n_outputs, x=x, y=y, width=width, height=height)
        self._blocks[block_tag] = block
    # end def

    def create_rectangle_rounded(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1]

        return self.create_polygon(points, **kwargs, smooth=True)
    # end def
# end class


# the main rectangle has its own tag and all elements that belong to the block (incl.the base rectangle) get a group tag
class VBlock:
    def __init__(self, editor: Editor, name: str, tag_id: str, n_inputs: int, n_outputs: int, x: float, y: float, width: float, height: float):
        self._editor = editor
        self._name = name

        self._n_inputs = n_inputs
        self._n_outputs = n_outputs

        self._freeze_highlighting = False

        self._corner_radius = 25
        # Since there might be UUID's that include only decimals and tkinter doesn't allow this, we need to add some
        # string at the beginning to distinguish these numbers from canvas object IDs.
        self._tag = "x" + tag_id
        self._group_tag = "g" + tag_id  # The (the group of) all elements that are parts of this block

        self._object_id = self._editor.create_rectangle_rounded(x, y, x + width, y + height, self._corner_radius,
                                                                outline="blue", width=1, tag=self._tag)

        self._editor.addtag_withtag(self._group_tag, self._object_id)

        self._object_id_text = self._editor.create_text(x + width // 2, y + height // 2,  font=("Arial", 20, "normal"),
                                                        fill="black", text=name)
        self._editor.addtag_withtag(self._group_tag, self._object_id_text)

        self._resize_lines = list()
        self._resize_lines.append(self._editor.create_line(x, y + self._corner_radius // 2, x + width, y + self._corner_radius // 2, fill="blue"))  # Top
        self._resize_lines.append(self._editor.create_line(x, y + height - self._corner_radius // 2, x + width, y + height - self._corner_radius // 2, fill="blue"))  # Bottom
        self._resize_lines.append(self._editor.create_line(x + self._corner_radius // 2, y, x + self._corner_radius // 2, y + height, fill="blue"))  # Left
        self._resize_lines.append(self._editor.create_line(x + width - self._corner_radius // 2, y, x + width - self._corner_radius // 2, y + height, fill="blue"))  # Right

        connector_size = 10
        connector_dist = (height - self._corner_radius - self._n_inputs * connector_size) / (self._n_inputs - 1)
        for n in range(self._n_inputs):
            input_conn = self._editor.create_rectangle(
                x + self._corner_radius // 2,
                y + self._corner_radius // 2 + n * (connector_dist + connector_size),
                x + self._corner_radius // 2 + connector_size,
                y + self._corner_radius // 2 + n * connector_dist + (n + 1) * connector_size,
                outline="blue")
            self._editor.addtag_withtag(self._group_tag, input_conn)
            self._editor.addtag_withtag(f"i{n}", input_conn)
        # end for

        connector_dist = (height - self._corner_radius - self._n_outputs * connector_size) / (self._n_outputs - 1)
        for n in range(self._n_outputs):
            output_conn = self._editor.create_rectangle(
                x + width - self._corner_radius // 2,
                y + self._corner_radius // 2 + n * (connector_dist + connector_size),
                x + width - (self._corner_radius // 2 + connector_size),
                y + self._corner_radius // 2 + n * connector_dist + (n + 1) * connector_size,
                outline="blue")
            self._editor.addtag_withtag(self._group_tag, output_conn)
            self._editor.addtag_withtag(f"o{n}", output_conn)
        # end for

        for resize_line in self._resize_lines:
            self._editor.addtag_withtag(self._group_tag, resize_line)
            self._editor.itemconfigure(resize_line, state=tk.HIDDEN)
        # end for

        self.do_leave()

        # Use unique tag in function
        self._editor.tag_bind(self._group_tag, "<Enter>", lambda event, tag=self._tag: self.on_enter_or_leave(event, tag))
        self._editor.tag_bind(self._group_tag, "<Leave>", lambda event, tag=self._tag: self.on_enter_or_leave(event, tag))
    # end if

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

    def on_enter_or_leave(self, event: tk.Event, tag):
        if not self._freeze_highlighting:
            if getattr(event, "type") == tk.EventType.Enter:
                self.do_enter()
            elif getattr(event, "type") == tk.EventType.Leave:
                self.do_leave()
            # end if
        # end if
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
