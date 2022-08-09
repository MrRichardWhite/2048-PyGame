# ---------------------------------------------------------------- #

import pygame as pg

# ---------------------------------------------------------------- #

class Box(object):

    anchor_to_float = {"center": (1/2, 1/2),
                       "north": (1/2, 0), "east": (1, 1/2), "south": (1/2, 1), "west": (0, 1/2),
                       "north west": (0, 0), "north east": (1, 0),
                       "south east": (1, 1), "south west": (0, 1)}

    def __init__(self, surface, name="", x=0, y=0, width=None, height=None,
                 scale_width=1, scale_height=1, anchor="center"):

        if width is None: width = surface.get_width()
        if height is None: height = surface.get_height()

        self._surface = surface
        self.name = name
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.scale = {"width": scale_width, "height": scale_height}
        self.anchor = anchor

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, surface):
        self._surface = surface

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def scale_width(self):
        return self.scale["width"]

    @scale_width.setter
    def scale_width(self, scale_width):
        self.scale["width"] = scale_width

    @property
    def scale_height(self):
        return self.scale["height"]

    @scale_height.setter
    def scale_height(self, scale_height):
        self.scale["height"] = scale_height

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, position):
        self.x, self.y = position

    @property
    def dimensions(self):
        return self.width, self.height

    @dimensions.setter
    def dimensions(self, dimensions):
        self.width, self.height = dimensions

    @property
    def x_actually(self):

        width_actually = self.width_actually
        if type(width_actually) is dict: width_actually = width_actually["outer"]

        return int(self.x - width_actually * self.anchor_to_float[self.anchor][0])

    @x_actually.setter
    def x_actually(self, x_actually):

        width_actually = self.width_actually
        if type(width_actually) is dict: width_actually = width_actually["outer"]

        self.x = int(x_actually + width_actually * self.anchor_to_float[self.anchor][0])

    @property
    def y_actually(self):

        height_actually = self.height_actually
        if type(height_actually) is dict: height_actually = height_actually["outer"]
        
        return int(self.y - height_actually * self.anchor_to_float[self.anchor][1])

    @y_actually.setter
    def y_actually(self, y_actually):

        height_actually = self.height_actually
        if type(height_actually) is dict: height_actually = height_actually["outer"]

        self.y = int(y_actually + height_actually * self.anchor_to_float[self.anchor][1])

    @property
    def position_actually(self):

        x_actually = self.x_actually
        if type(x_actually) is dict: x_actually = x_actually["outer"]

        y_actually = self.y_actually
        if type(y_actually) is dict: y_actually = y_actually["outer"]

        return x_actually, y_actually

    @position_actually.setter
    def position_actually(self, position_actually):
        self.x_actually, self.y_actually = position_actually

    @property
    def width_actually(self):
        return int(self.width * self.scale["width"])

    @width_actually.setter
    def width_actually(self, width_actually):
        self.scale["width"] = width_actually / self.width

    @property
    def height_actually(self):
        return int(self.height * self.scale["height"])

    @height_actually.setter    
    def height_actually(self, height_actually):
        self.scale["height"] = height_actually / self.height

    @property
    def dimensions_actually(self):

        width_actually = self.width_actually
        if type(width_actually) is dict: width_actually = width_actually["outer"]

        height_actually = self.height_actually
        if type(height_actually) is dict: height_actually = height_actually["outer"]

        return width_actually, height_actually

    @dimensions_actually.setter
    def dimensions_actually(self, dimensions_actually):
        Box.width_actually, Box.height_actually = dimensions_actually

    @property
    def position_and_dimensions_actually(self):

        position_actually = self.position_actually
        if type(position_actually) is dict: position_actually = position_actually["outer"]

        dimensions_actually = self.dimensions_actually
        if type(dimensions_actually) is dict: dimensions_actually = dimensions_actually["outer"]

        return (*position_actually, *dimensions_actually)

    @property
    def a(self):
        return int(self.x + self.width)

    @a.setter
    def a(self, a):
        self.width = int(a - self.x)

    @property
    def b(self):
        return int(self.y + self.height)

    @b.setter
    def b(self, b):
        self.height = int(b - self.y)

    @property
    def bound(self):
        return self.a, self.b

    @bound.setter
    def bound(self, bound):
        self.a, self.b = bound

    @property
    def a_actually(self):

        x_actually = self.x_actually
        if type(x_actually) is dict: x_actually = x_actually["outer"]

        width_actually = self.width_actually
        if type(width_actually) is dict: width_actually = width_actually["outer"]

        return int(x_actually + width_actually)

    @a_actually.setter
    def a_actually(self, a_actually):

        x_actually = self.x_actually
        if type(x_actually) is dict: x_actually = x_actually["outer"]

        self.width = int(a_actually - x_actually)
        self.scale["width"] = 1

    @property
    def b_actually(self):

        y_actually = self.y_actually
        if type(y_actually) is dict: y_actually = y_actually["outer"]

        height_actually = self.height_actually
        if type(height_actually) is dict: height_actually = height_actually["outer"]

        return int(y_actually + height_actually)

    @b_actually.setter
    def b_actually(self, b_actually):

        y_actually = self.y_actually
        if type(y_actually) is dict: y_actually = y_actually["outer"]

        self.height = int(b_actually - y_actually)
        self.scale["height"] = 1

    @property
    def bound_actually(self):

        a_actually = self.a_actually
        if type(a_actually) is dict: a_actually = a_actually["outer"]

        b_actually = self.b_actually
        if type(b_actually) is dict: b_actually = b_actually["outer"]

        return a_actually, b_actually

    @bound_actually.setter
    def bound_actually(self, bound_actually):
        self.a_actually, self.b_actually = bound_actually

    def draw(self):
        pass

    def update(self, event=None):
        pass

class Label(Box):

    def __init__(self, surface, name="", x=0, y=0, width=None, height=None,
                 scale_width=1, scale_height=1, anchor="center",
                 filling_color=pg.Color("white"),
                 border_thickness=0, border_radius=0, border_color=pg.Color("black"),
                 image_path=None, image_scale_width=1, image_scale_height=1, image_anchor="center",
                 text_string="", text_color=pg.Color("black"), text_scale=None,
                 font_type="arial", font_size=24):

        super().__init__(surface, name, x, y, width, height,
                         scale_width, scale_height, anchor)

        self.filling = {"color": filling_color}
        self.border  = {"thickness": border_thickness, "radius": border_radius, "color": border_color}
        self.text    = {"string": text_string, "color":  text_color, "scale":  text_scale}
        self.font    = {"type": font_type, "size": font_size}
        self.image   = {"path": image_path, "scale": {"width": image_scale_width, "height": image_scale_height}, "anchor": image_anchor}

        if self.image["path"] is not None: self.load_image()

    @property
    def filling_color(self):
        return self.filling["color"]

    @filling_color.setter
    def filling_color(self, filling_color):
        self.filling["color"] = filling_color

    @property
    def border_color(self):
        return self.border["color"]

    @border_color.setter
    def border_color(self, border_color):
        self.border["color"] = border_color

    @property
    def text_color(self):
        return self.text["color"]

    @text_color.setter
    def text_color(self, text_color):
        self.text["color"] = text_color

    @property
    def text_string(self):
        return self.text["string"]

    @text_string.setter
    def text_string(self, text_string):
        self.text["string"] = text_string

    @property
    def font_type(self):
        return self.font["type"]

    @font_type.setter
    def font_type(self, font_type):
        self.font["type"] = font_type

    @property
    def font_size(self):
        return self.font["size"]

    @font_size.setter
    def font_size(self, font_size):
        self.font["size"] = font_size

    @property
    def image_path(self):
        return self.image["path"]

    @image_path.setter
    def image_path(self, image_path):
        self.image["path"] = image_path
        if self.image["path"] is not None: self.load_image()

    @property
    def image_scale_width(self):
        return self.image["scale"]["width"]

    @image_scale_width.setter
    def image_scale_width(self, image_scale_width):
        self.image["scale"]["width"] = image_scale_width
        if self.image["path"] is not None: self.load_image()

    @property
    def image_scale_height(self):
        return self.image["scale"]["height"]

    @image_scale_height.setter
    def image_scale_height(self, image_scale_height):
        self.image["scale"]["height"] = image_scale_height
        if self.image["path"] is not None: self.load_image()

    @property
    def image_anchor(self):
        return self.image["anchor"]

    @image_anchor.setter
    def image_anchor(self, image_anchor):
        self.image["anchor"] = image_anchor
        if self.image["path"] is not None: self.load_image()

    @property
    def image_loaded_original(self):
        return self.image["loaded"]["original"]

    @property
    def image_loaded_actually(self):
        return self.image["loaded"]["actually"]

    @property
    def x_actually(self):
        return {"outer": super().x_actually,
                "inner": super().x_actually + self.border["thickness"]}

    @x_actually.setter
    def x_actually(self, x_actually):
        super(Label, self.__class__).x_actually.fset(self, x_actually)

    @property
    def y_actually(self):
        return {"outer": super().y_actually,
                "inner": super().y_actually + self.border["thickness"]}

    @y_actually.setter
    def y_actually(self, y_actually):
        super(Label, self.__class__).y_actually.fset(self, y_actually)

    @property
    def position_actually(self):
        return {"outer": super().position_actually,
                "inner": (self.x_actually["inner"], self.y_actually["inner"])}

    @position_actually.setter
    def position_actually(self, position_actually):
        super(Label, self.__class__).position_actually.fset(self, position_actually)

    @property
    def width_actually(self):
        return {"outer": super().width_actually,
                "inner": super().width_actually - 2 * self.border["thickness"]}

    @width_actually.setter
    def width_actually(self, width_actually):
        super(Label, self.__class__).width_actually.fset(self, width_actually)

    @property
    def height_actually(self):
        return {"outer": super().height_actually,
                "inner": super().height_actually - 2 * self.border["thickness"]}

    @height_actually.setter
    def height_actually(self, height_actually):
        super(Label, self.__class__).height_actually.fset(self, height_actually)

    @property
    def dimensions_actually(self):
        return {"outer": super().dimensions_actually,
                "inner": (self.width_actually["inner"], self.height_actually["inner"])}

    @dimensions_actually.setter
    def dimensions_actually(self, dimensions_actually):
        super(Label, self.__class__).dimensions_actually.fset(self, dimensions_actually)

    @property
    def position_and_dimensions_actually(self):
        return {"outer": super().position_and_dimensions_actually,
                "inner": (self.x_actually["inner"], self.y_actually["inner"], self.width_actually["inner"], self.height_actually["inner"])}

    @property
    def a_actually(self):
        return {"outer": super().a_actually,
                "inner": super().a_actually - self.border["thickness"]}

    @a_actually.setter
    def a_actually(self, a_actually):
        super(Label, self.__class__).a_actually.fset(self, a_actually)

    @property
    def b_actually(self):
        return {"outer": super().b_actually,
                "inner": super().b_actually - self.border["thickness"]}

    @b_actually.setter
    def b_actually(self, b_actually):
        super(Label, self.__class__).b_actually.fset(self, b_actually)

    @property
    def bound_actually(self):
        return {"outer": super().bound_actually,
                "inner": (self.a_actually["inner"], self.b_actually["inner"])}

    @bound_actually.setter
    def bound_actually(self, bound_actually):
        super(Label, self.__class__).bound_actually.fset(self, bound_actually)

    @property
    def text_scale_actually(self):
        return self.text["scale"] if self.text["scale"] is not None else min(self.scale.values())

    @property
    def text_rendered(self):
        return self.font_actually.render(self.text_string, True, self.text_color)

    @property
    def text_rendered_x(self):
        return self.x_actually["outer"] + self.width_actually["outer"] // 2 - self.text_rendered.get_width() // 2

    @property
    def text_rendered_y(self):
        return self.y_actually["outer"] + self.height_actually["outer"] // 2 - self.text_rendered.get_height() // 2

    @property
    def text_rendered_position(self):
        return (self.text_rendered_x, self.text_rendered_y)

    @property
    def font_size_actually(self):
        return int(self.font_size * self.text_scale_actually)

    @property
    def font_actually(self):
        return pg.font.SysFont(self.font_type, self.font_size_actually)

    @property
    def image_width_actually(self):
        if self.image["path"] is None:
            return None
        else:
            return self.image["loaded"]["original"].get_width() * self.image["scale"]["width"]

    @property
    def image_height_actually(self):
        if self.image["path"] is None:
            return None
        else:
            return self.image["loaded"]["original"].get_height() * self.image["scale"]["height"]

    @property
    def image_dimensions_actually(self):
        if self.image["path"] is None:
            return None
        else:
            return self.image_width_actually, self.image_height_actually

    @property
    def image_x_actually(self):

        image_anchor = self.image_anchor
        if image_anchor.split(" ")[0] not in ["inner", "outer"]:
            image_anchor = "outer" + " " + image_anchor

        inner_outer = image_anchor.split(" ")[0]
        anchor = " ".join(image_anchor.split(" ")[1:])

        return int(self.x_actually[inner_outer] + self.width_actually[inner_outer] * self.anchor_to_float[anchor][0] - self.image_width_actually / 2)

    @property
    def image_y_actually(self):

        image_anchor = self.image_anchor
        if image_anchor.split(" ")[0] not in ["inner", "outer"]:
            image_anchor = "outer" + " " + image_anchor

        inner_outer = image_anchor.split(" ")[0]
        anchor = " ".join(image_anchor.split(" ")[1:])

        return int(self.y_actually[inner_outer] + self.height_actually[inner_outer] * self.anchor_to_float[anchor][1] - self.image_height_actually / 2)

    @property
    def image_position_actually(self):
        return self.image_x_actually, self.image_y_actually

    def load_image(self):
        self.image["loaded"] = {}
        self.image["loaded"]["original"] = pg.image.load(self.image_path)
        self.image["loaded"]["actually"] = pg.transform.scale(self.image["loaded"]["original"], self.image_dimensions_actually)

    def text_rendered_fits_in_box(self, text_rendered=None):

        if text_rendered is None: text_rendered = self.text_rendered

        return text_rendered.get_width()  < self.width_actually["inner"] \
           and text_rendered.get_height() < self.height_actually["inner"]

    def draw(self):

        self.body = {"outer": pg.draw.rect(self.surface, self.border_color,  self.position_and_dimensions_actually["outer"], 0, border_radius=self.border["radius"]),
                     "inner": pg.draw.rect(self.surface, self.filling_color, self.position_and_dimensions_actually["inner"], 0, border_radius=self.border["radius"])}

        if self.image["path"] is not None:
            self.surface.blit(self.image_loaded_actually, self.image_position_actually)

        if self.text["string"] != "":
            if self.text_rendered_fits_in_box:
                self.surface.blit(self.text_rendered, self.text_rendered_position)

class Button(Label):

    def __init__(self, surface, name="", x=0, y=0, width=None, height=None,
                 scale_width=1, scale_height=1, anchor="center",
                 filling_color=pg.Color("white"),
                 border_thickness=0, border_radius=0, border_color=pg.Color("black"),
                 image_path=None, image_scale_width=1, image_scale_height=1, image_anchor="center",
                 text_string="", text_color=pg.Color("black"), text_scale=None,
                 font_type="arial", font_size=24,
                 response="toggle", status="unclicked",
                 filling_color_unclicked=None, filling_color_semiclicked=None, filling_color_clicked=None,
                 border_color_unclicked=None, border_color_semiclicked=None, border_color_clicked=None,
                 text_color_unclicked=None, text_color_semiclicked=None, text_color_clicked=None,
                 text_string_unclicked=None, text_string_semiclicked=None, text_string_clicked=None,
                 font_type_unclicked=None, font_type_semiclicked=None, font_type_clicked=None,
                 font_size_unclicked=None, font_size_semiclicked=None, font_size_clicked=None,
                 clickable=True, unclickable_inside=False, unclickable_outside=True):

        if filling_color_unclicked is None:   filling_color_unclicked   = filling_color
        if filling_color_semiclicked is None: filling_color_semiclicked = filling_color
        if filling_color_clicked is None:     filling_color_clicked     = filling_color_semiclicked
        if border_color_unclicked is None:    border_color_unclicked    = border_color
        if border_color_semiclicked is None:  border_color_semiclicked  = border_color
        if border_color_clicked is None:      border_color_clicked      = border_color_semiclicked
        if text_color_unclicked is None:      text_color_unclicked      = text_color
        if text_color_semiclicked is None:    text_color_semiclicked    = text_color
        if text_color_clicked is None:        text_color_clicked        = text_color_semiclicked
        if text_string_unclicked is None:     text_string_unclicked     = text_string
        if text_string_semiclicked is None:   text_string_semiclicked   = text_string
        if text_string_clicked is None:       text_string_clicked       = text_string_semiclicked
        if font_type_unclicked is None:       font_type_unclicked       = font_type
        if font_type_semiclicked is None:     font_type_semiclicked     = font_type
        if font_type_clicked is None:         font_type_clicked         = font_type_semiclicked
        if font_size_unclicked is None:       font_size_unclicked       = font_size
        if font_size_semiclicked is None:     font_size_semiclicked     = font_size
        if font_size_clicked is None:         font_size_clicked         = font_size_semiclicked

        super().__init__(surface, name, x, y, width, height,
                         scale_width, scale_height, anchor,
                         filling_color,
                         border_thickness, border_radius, border_color,
                         image_path, image_scale_width, image_scale_height, image_anchor,
                         text_string, text_color, text_scale,
                         font_type, font_size)

        self.response = response
        self.status = status

        self.filling["color"]  = {"unclicked": filling_color_unclicked, "semiclicked": filling_color_semiclicked, "clicked": filling_color_clicked}
        self.border ["color"]  = {"unclicked": border_color_unclicked,  "semiclicked": border_color_semiclicked,  "clicked": border_color_clicked}
        self.text   ["string"] = {"unclicked": text_string_unclicked,   "semiclicked": text_string_semiclicked,   "clicked": text_string_clicked}
        self.text   ["color"]  = {"unclicked": text_color_unclicked,    "semiclicked": text_color_semiclicked,    "clicked": text_color_clicked}
        self.font   ["type"]   = {"unclicked": font_type_unclicked,     "semiclicked": font_type_semiclicked,     "clicked": font_type_clicked}
        self.font   ["size"]   = {"unclicked": font_size_unclicked,     "semiclicked": font_size_semiclicked,     "clicked": font_size_clicked}

        self._clickable = clickable
        self.unclickable = {"inside": unclickable_inside, "outside": unclickable_outside}

    @property
    def filling_color_unclicked(self):
        return self.filling["color"]["unclicked"]

    @filling_color_unclicked.setter
    def filling_color_unclicked(self, filling_color_unclicked):
        self.filling["color"]["unclicked"] = filling_color_unclicked

    @property
    def filling_color_semiclicked(self):
        return self.filling["color"]["semiclicked"]

    @filling_color_semiclicked.setter
    def filling_color_semiclicked(self, filling_color_semiclicked):
        self.filling["color"]["semiclicked"] = filling_color_semiclicked

    @property
    def filling_color_clicked(self):
        return self.filling["color"]["clicked"]

    @filling_color_clicked.setter
    def filling_color_clicked(self, filling_color_clicked):
        self.filling["color"]["clicked"] = filling_color_clicked

    @property
    def border_color_unclicked(self):
        return self.border["color"]["unclicked"]

    @border_color_unclicked.setter
    def border_color_unclicked(self, border_color_unclicked):
        self.border["color"]["unclicked"] = border_color_unclicked

    @property
    def border_color_semiclicked(self):
        return self.border["color"]["semiclicked"]

    @border_color_semiclicked.setter
    def border_color_semiclicked(self, border_color_semiclicked):
        self.border["color"]["semiclicked"] = border_color_semiclicked

    @property
    def border_color_clicked(self):
        return self.border["color"]["clicked"]

    @border_color_clicked.setter
    def border_color_clicked(self, border_color_clicked):
        self.border["color"]["clicked"] = border_color_clicked

    @property
    def text_color_unclicked(self):
        return self.text["color"]["unclicked"]

    @text_color_unclicked.setter
    def text_color_unclicked(self, text_color_unclicked):
        self.text["color"]["unclicked"] = text_color_unclicked

    @property
    def text_color_semiclicked(self):
        return self.text["color"]["semiclicked"]

    @text_color_semiclicked.setter
    def text_color_semiclicked(self, text_color_semiclicked):
        self.text["color"]["semiclicked"] = text_color_semiclicked

    @property
    def text_color_clicked(self):
        return self.text["color"]["clicked"]

    @text_color_clicked.setter
    def text_color_clicked(self, text_color_clicked):
        self.text["color"]["clicked"] = text_color_clicked

    @property
    def text_string_unclicked(self):
        return self.text["string"]["unclicked"]

    @text_string_unclicked.setter
    def text_string_unclicked(self, text_string_unclicked):
        self.text["string"]["unclicked"] = text_string_unclicked

    @property
    def text_string_semiclicked(self):
        return self.text["string"]["semiclicked"]

    @text_string_semiclicked.setter
    def text_string_semiclicked(self, text_string_semiclicked):
        self.text["string"]["semiclicked"] = text_string_semiclicked

    @property
    def text_string_clicked(self):
        return self.text["string"]["clicked"]

    @text_string_clicked.setter
    def text_string_clicked(self, text_string_clicked):
        self.text["string"]["clicked"] = text_string_clicked

    @property
    def font_type_unclicked(self):
        return self.font["type"]["unclicked"]

    @font_type_unclicked.setter
    def font_type_unclicked(self, font_type_unclicked):
        self.font["type"]["unclicked"] = font_type_unclicked

    @property
    def font_type_semiclicked(self):
        return self.font["type"]["semiclicked"]

    @font_type_semiclicked.setter
    def font_type_semiclicked(self, font_type_semiclicked):
        self.font["type"]["semiclicked"] = font_type_semiclicked

    @property
    def font_type_clicked(self):
        return self.font["type"]["clicked"]

    @font_type_clicked.setter
    def font_type_clicked(self, font_type_clicked):
        self.font["type"]["clicked"] = font_type_clicked

    @property
    def font_size_unclicked(self):
        return self.font["size"]["unclicked"]

    @font_size_unclicked.setter
    def font_size_unclicked(self, font_size_unclicked):
        self.font["size"]["unclicked"] = font_size_unclicked

    @property
    def font_size_semiclicked(self):
        return self.font["size"]["semiclicked"]

    @font_size_semiclicked.setter
    def font_size_semiclicked(self, font_size_semiclicked):
        self.font["size"]["semiclicked"] = font_size_semiclicked

    @property
    def font_size_clicked(self):
        return self.font["size"]["clicked"]

    @font_size_clicked.setter
    def font_size_clicked(self, font_size_clicked):
        self.font["size"]["clicked"] = font_size_clicked

    @property
    def clickable(self):
        return self._clickable

    @clickable.setter
    def clickable(self, clickable):
        self._clickable = clickable

    @property
    def unclickable_inside(self):
        return self.unclickable["inside"]

    @unclickable_inside.setter
    def unclickable_inside(self, unclickable_inside):
        self.font["inside"] = unclickable_inside

    @property
    def unclickable_outside(self):
        return self.unclickable["outside"]

    @unclickable_outside.setter
    def unclickable_outside(self, unclickable_outside):
        self.font["outside"] = unclickable_outside

    @property
    def filling_color(self):
        return self.filling["color"][self.status]

    @filling_color.setter
    def filling_color(self, filling_color):
        self.filling_color_unclicked   = filling_color
        self.filling_color_semiclicked = filling_color
        self.filling_color_clicked     = filling_color

    @property
    def border_color(self):
        return self.border["color"][self.status]

    @border_color.setter
    def border_color(self, border_color):
        self.border_color_unclicked   = border_color
        self.border_color_semiclicked = border_color
        self.border_color_clicked     = border_color

    @property
    def text_color(self):
        return self.text["color"][self.status]

    @text_color.setter
    def text_color(self, text_color):
        self.text_color_unclicked   = text_color
        self.text_color_semiclicked = text_color
        self.text_color_clicked     = text_color

    @property
    def text_string(self):
        return self.text["string"][self.status]

    @text_string.setter
    def text_string(self, text_string):
        self.text_string_unclicked   = text_string
        self.text_string_semiclicked = text_string
        self.text_string_clicked     = text_string

    @property
    def font_type(self):
        return self.font["type"][self.status]

    @font_type.setter
    def font_type(self, font_type):
        self.font_type_unclicked   = font_type
        self.font_type_semiclicked = font_type
        self.font_type_clicked     = font_type

    @property
    def font_size(self):
        return self.font["size"][self.status]

    @font_size.setter
    def font_size(self, font_size):
        self.font_size_unclicked   = font_size
        self.font_size_semiclicked = font_size
        self.font_size_clicked     = font_size

    @property
    def targeted(self):
        return self.body["outer"].collidepoint(
            pg.mouse.get_pos()
        )

    def update_status(self, event):

        if self.clickable:

            if event.type == pg.MOUSEMOTION:

                if self.response == "hold":
                    if self.targeted:
                        self.status = "semiclicked"
                    else:
                        self.status = "unclicked"

                if self.response == "toggle":
                    if self.status != "clicked":
                        if self.targeted:
                            self.status = "semiclicked"
                        else:
                            self.status = "unclicked"

            if event.type == pg.MOUSEBUTTONDOWN:

                if self.response == "hold":
                    if self.targeted:
                        self.status = "clicked"

                if self.response == "toggle":
                    if self.status == "clicked":
                        if self.targeted:
                            if self.unclickable["inside"]:
                                self.status = "semiclicked"
                        else:
                            if self.unclickable["outside"]:
                                self.status = "unclicked"
                    else:
                        if self.targeted:
                            self.status = "clicked"

            else:

                if self.response == "hold":
                    if self.status == "clicked":
                        if self.targeted:
                            self.status = "semiclicked"
                        else:
                            self.status = "unclicked"

    def update(self, event):
        self.update_status(event)

    def clicked(self, event=None):
        if self.clickable:
            if event is None:
                return self.status == "clicked"
            else:
                return event.type == pg.MOUSEBUTTONDOWN \
                and self.body["outer"].collidepoint(pg.mouse.get_pos())
        else:
            return False

class TextBox(Button):

    @property
    def text_string(self):
        if self.text["string"]["clicked"] != "":
            return self.text["string"]["clicked"]
        else:
            return self.text["string"][self.status]

    @text_string.setter
    def text_string(self, text_string):
        self.text_string_clicked = text_string

    @property
    def content(self):
        return self.text["string"]["clicked"]

    def update_text_string_clicked(self, event):

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                if self.text["string"]["clicked"] != "":
                    self.text["string"]["clicked"] = self.text["string"]["clicked"][:-1]
            elif event.key in [pg.K_TAB, pg.K_RETURN, pg.K_KP_ENTER]:
                pass
            elif event.key == pg.K_ESCAPE:
                self.status = "unclicked"
            else:

                text_new_string   = self.text["string"]["clicked"] + event.unicode
                text_new_rendered = self.font_actually.render(text_new_string, True, self.text_color)

                if self.text_rendered_fits_in_box(text_new_rendered):
                    self.text["string"]["clicked"] = text_new_string

    def update(self, event):

        super().update(event)

        if self.status == "clicked":
            self.update_text_string_clicked(event)

    def entered(self, event):
        return event.type == pg.KEYDOWN and event.key in [pg.K_RETURN, pg.K_KP_ENTER] \
           and self.status == "clicked"

# ---------------------------------------------------------------- #
