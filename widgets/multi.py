# ---------------------------------------------------------------- #

import pygame as pg
import numpy  as np

from widgets.single import *
from widgets.utils  import *

# ---------------------------------------------------------------- #

class Boxes(Box):

    def __init__(self, surface, name="", x=0, y=0, width=None, height=None,
                 scale_width=1, scale_height=1, anchor="north west",
                 members=None, mapping_position=None, mapping_bound=None, mapping_nudge=None,
                 grid_amount_rows=1, grid_amount_columns=1, grid_nudge=None,
                 grid_drawing_style=None, grid_drawing_color=pg.Color("black"), grid_drawing_nudge=None,
                 grid_name=None, grid_x=None, grid_y=None, grid_width=None, grid_height=None,
                 grid_scale_width=None, grid_scale_height=None, grid_anchor=None):

        if members is None: members = []
        if mapping_position is None: mapping_position = {}
        if mapping_bound is None: mapping_bound = {}

        assert len(members) >= len(mapping_position)
        assert len(members) >= len(mapping_bound)

        super().__init__(surface, name, x, y, width, height,
                         scale_width, scale_height, anchor)

        self.grid = {"amount": {"rows" : grid_amount_rows, "columns": grid_amount_columns},
                     "nudge": grid_nudge,
                     "drawing": {"style": grid_drawing_style, "color": grid_drawing_color, "nudge": grid_drawing_nudge},
                     "name": grid_name, "x": grid_x, "y": grid_y, "width": grid_width, "height": grid_height,
                     "scale": {"width": grid_scale_width, "height": grid_scale_height}, "anchor": grid_anchor}

        self.members = list(members)
        self.mapping = {"position": mapping_position, "bound": mapping_bound, "nudge": mapping_nudge}

        self._member_index = -1

        for member in self.members:
            assert member.surface == self.surface

    @property
    def surface(self):
        return super().surface

    @surface.setter
    def surface(self, surface):
        super(Boxes, self.__class__).surface.fset(self, surface)
        for member in self.members:
            member.surface = surface

    @property
    def x(self):
        return super().x

    @x.setter
    def x(self, x):
        super(Boxes, self.__class__).x.fset(self, x)
        self.update_members_position()
        self.update_members_bound()

    @property
    def y(self):
        return super().y

    @y.setter
    def y(self, y):
        super(Boxes, self.__class__).y.fset(self, y)
        self.update_members_position()
        self.update_members_bound()

    @property
    def width(self):
        return super().width

    @width.setter
    def width(self, width):
        super(Boxes, self.__class__).width.fset(self, width)
        self.update_members_position()
        self.update_members_bound()

    @property
    def height(self):
        return super().height

    @height.setter
    def height(self, height):
        super(Boxes, self.__class__).height.fset(self, height)
        self.update_members_position()
        self.update_members_bound()

    @property
    def scale_width(self):
        return super().scale_width

    @scale_width.setter
    def scale_width(self, scale_width):
        super(Boxes, self.__class__).scale_width.fset(self, scale_width)
        self.update_members_position()
        self.update_members_bound()

    @property
    def scale_height(self):
        return super().scale_height

    @scale_height.setter
    def scale_height(self, scale_height):
        super(Boxes, self.__class__).scale_height.fset(self, scale_height)
        self.update_members_position()
        self.update_members_bound()

    @property
    def position(self):
        return super().position

    @position.setter
    def position(self, position):
        super(Boxes, self.__class__).position.fset(self, position)
        self.update_members_position()
        self.update_members_bound()

    @property
    def dimensions(self):
        return super().dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        super(Boxes, self.__class__).dimensions.fset(self, dimensions)
        self.update_members_position()
        self.update_members_bound()

    @property
    def grid_amount_rows(self):
        return self.grid["amount"]["rows"]

    @grid_amount_rows.setter
    def grid_amount_rows(self, grid_amount_rows):
        self.grid["amount"]["rows"] = grid_amount_rows

    @property
    def grid_amount_columns(self):
        return self.grid["amount"]["columns"]

    @grid_amount_columns.setter
    def grid_amount_columns(self, grid_amount_columns):
        self.grid["amount"]["columns"] = grid_amount_columns

    @property
    def grid_nudge(self):
        return self.grid["nudge"]

    @grid_nudge.setter
    def grid_nudge(self, grid_nudge):
        self.grid["nudge"] = grid_nudge

    @property
    def grid_drawing_style(self):
        return self.grid["drawing"]["style"]

    @grid_drawing_style.setter
    def grid_drawing_style(self, grid_drawing_style):
        self.grid["drawing"]["style"] = grid_drawing_style

    @property
    def grid_drawing_color(self):
        return self.grid["drawing"]["color"]

    @grid_drawing_color.setter
    def grid_drawing_color(self, grid_drawing_color):
        self.grid["drawing"]["color"] = grid_drawing_color

    @property
    def grid_drawing_nudge(self):
        return self.grid["drawing"]["nudge"]

    @grid_drawing_nudge.setter
    def grid_drawing_nudge(self, grid_drawing_nudge):
        self.grid["drawing"]["nudge"] = grid_drawing_nudge

    @property
    def grid_name(self):
        return self.grid["name"]

    @grid_name.setter
    def grid_name(self, grid_name):
        self.grid["name"] = grid_name

    @property
    def grid_x(self):
        return self.grid["x"]

    @grid_x.setter
    def grid_x(self, grid_x):
        self.grid["x"] = grid_x

    @property
    def grid_y(self):
        return self.grid["y"]

    @grid_y.setter
    def grid_y(self, grid_y):
        self.grid["y"] = grid_y

    @property
    def grid_width(self):
        return self.grid["width"]

    @grid_width.setter
    def grid_width(self, grid_width):
        self.grid["width"] = grid_width

    @property
    def grid_height(self):
        return self.grid["height"]

    @grid_height.setter
    def grid_height(self, grid_height):
        self.grid["height"] = grid_height

    @property
    def grid_scale_width(self):
        return self.grid["scale"]["width"]

    @grid_scale_width.setter
    def grid_scale_width(self, grid_scale_width):
        self.grid["scale"]["width"] = grid_scale_width

    @property
    def grid_scale_height(self):
        return self.grid["scale"]["height"]

    @grid_scale_height.setter
    def grid_scale_height(self, grid_scale_height):
        self.grid["scale"]["height"] = grid_scale_height

    @property
    def grid_anchor(self):
        return self.grid["anchor"]

    @grid_anchor.setter
    def grid_anchor(self, grid_anchor):
        self.grid["anchor"] = grid_anchor

    @property
    def mapping_position(self):
        return self.mapping["position"]

    @mapping_position.setter
    def mapping_position(self, mapping_position):
        self.mapping["position"] = mapping_position

    @property
    def mapping_bound(self):
        return self.mapping["bound"]

    @mapping_bound.setter
    def mapping_bound(self, mapping_bound):
        self.mapping["bound"] = mapping_bound

    @property
    def mapping_nudge(self):
        return self.mapping["nudge"]

    @mapping_nudge.setter
    def mapping_nudge(self, mapping_nudge):
        self.mapping["nudge"] = mapping_nudge

    def __next__(self):

        self._member_index += 1

        if self._member_index >= len(self.members):
            self._member_index = -1
            raise StopIteration
        else:
            return self.members[self._member_index]

    @property
    def grid_amount_rows_actually(self):
        if self.grid["nudge"] is None:
            return self.grid["amount"]["rows"]
        if self.grid["nudge"] == "inner":
            return self.grid["amount"]["rows"] + 1
        if self.grid["nudge"] == "outer":
            return self.grid["amount"]["rows"] - 1

    @property
    def grid_amount_columns_actually(self):
        if self.grid["nudge"] is None:
            return self.grid["amount"]["columns"]
        if self.grid["nudge"] == "inner":
            return self.grid["amount"]["columns"] + 1
        if self.grid["nudge"] == "outer":
            return self.grid["amount"]["columns"] - 1

    @property
    def grid_name_actually(self):
        return self.grid["name"] if self.grid["name"] is not None else self.name + " " + "grid"

    @property
    def grid_x_actually(self):
        return self.grid["x"] if self.grid["x"] is not None else self.x

    @property
    def grid_y_actually(self):
        return self.grid["y"] if self.grid["y"] is not None else self.y

    @property
    def grid_width_actually(self):
        return self.grid["width"] if self.grid["width"] is not None else self.width

    @property
    def grid_height_actually(self):
        return self.grid["height"] if self.grid["height"] is not None else self.height

    @property
    def grid_scale_width_actually(self):
        return self.grid["scale"]["width"] if self.grid["scale"]["width"] is not None else self.scale["width"]

    @property
    def grid_scale_height_actually(self):
        return self.grid["scale"]["height"] if self.grid["scale"]["height"] is not None else self.scale["height"]

    @property
    def grid_anchor_actually(self):
        return self.grid["anchor"] if self.grid["anchor"] is not None else self.anchor

    @property
    def grid_actually(self):
        return Grid(self.surface, self.grid_name_actually, self.grid_x_actually, self.grid_y_actually, self.grid_width_actually, self.grid_height_actually,
                    self.grid_scale_width_actually, self.grid_scale_height_actually, self.grid_anchor_actually,
                    self.grid_amount_rows_actually, self.grid_amount_columns_actually,
                    self.grid["drawing"]["style"], self.grid["drawing"]["color"], self.grid["drawing"]["nudge"])

    @property
    def member_names(self):
        return [member.name for member in self.members]

    @property
    def amount(self):
        return len(self.members)

    def update_members_position(self, mapping_position=None):

        if mapping_position is None:
            if self.mapping["nudge"] == None:
                mapping_position = {key: self.grid_actually[j][i] for key, (i, j) in self.mapping["position"].items()}
            elif self.mapping["nudge"] == "inner":
                mapping_position = {key: self.grid_actually.inner[j][i] for key, (i, j) in self.mapping["position"].items()}
            elif self.mapping["nudge"] == "outer":
                mapping_position = {key: self.grid_actually.outer[j][i] for key, (i, j) in self.mapping["position"].items()}

        for key, value in mapping_position.items():
            self[key].position = value

    def update_members_bound(self, mapping_bound=None):

        if mapping_bound is None:
            mapping_bound = {key: self.grid_actually[j][i] for key, (i, j) in self.mapping["bound"].items()}

        for key, value in mapping_bound.items():
            self[key].bound = value

    def __getitem__(self, key):

        if type(key) in [int, np.int32]:
            return self.members[key]

        if type(key) == str:
            for member in self.members:
                if member.name == key:
                    return member

        raise IndexError(f"{key} could not be found")

    def __setitem__(self, key, value):

        if type(key) in [int, np.int32]:
            self.members[key] = value

        if type(key) == str:
            for n, member in enumerate(self.members):
                if member.name == key:
                    self.members[n] = value

    def draw(self):
        self.grid_actually.draw()
        draw(self.members)

    def update(self, event):
        self.update_members_position()
        self.update_members_bound()
        update(self.members, event)

class Labels(Boxes, Label):

    def __init__(self, surface, name="", x=0, y=0, width=None, height=None,
                 scale_width=1, scale_height=1, anchor="north west",
                 members=None, mapping_position=None, mapping_bound=None, mapping_nudge=None,
                 grid_amount_rows=1, grid_amount_columns=1, grid_nudge=None,
                 grid_drawing_style=None, grid_drawing_color=pg.Color("black"), grid_drawing_nudge=None,
                 grid_name=None, grid_x=None, grid_y=None, grid_width=None, grid_height=None,
                 grid_scale_width=None, grid_scale_height=None, grid_anchor=None,
                 filling_color=pg.Color("white"),
                 border_thickness=0, border_radius=0, border_color=pg.Color("black"),
                 image_path=None, image_scale_width=1, image_scale_height=1, image_anchor="center",
                 drawing=False):

        Boxes.__init__(self, surface, name, x, y, width, height,
                       scale_width, scale_height, anchor,
                       members, mapping_position, mapping_bound, mapping_nudge,
                       grid_amount_rows, grid_amount_columns, grid_nudge,
                       grid_drawing_style, grid_drawing_color, grid_drawing_nudge,
                       grid_name, grid_x, grid_y, grid_width, grid_height,
                       grid_scale_width, grid_scale_height, grid_anchor)

        Label.__init__(self, surface, name, x, y, width, height,
                       scale_width, scale_height, anchor,
                       filling_color,
                       border_thickness, border_radius, border_color,
                       image_path, image_scale_width, image_scale_height, image_anchor)

        self.drawing = drawing

    def draw(self):
        if self.drawing: Label.draw(self)
        Boxes.draw(self)

class Buttons(Labels, Button):

    def __init__(self, surface, name="", x=0, y=0, width=None, height=None,
                 scale_width=1, scale_height=1, anchor="north west",
                 members=None, mapping_position=None, mapping_bound=None, mapping_nudge=None,
                 grid_amount_rows=1, grid_amount_columns=1, grid_nudge=None,
                 grid_drawing_style=None, grid_drawing_color=pg.Color("black"), grid_drawing_nudge=None,
                 grid_name=None, grid_x=None, grid_y=None, grid_width=None, grid_height=None,
                 grid_scale_width=None, grid_scale_height=None, grid_anchor=None,
                 filling_color=pg.Color("white"),
                 border_thickness=0, border_radius=0, border_color=pg.Color("black"),
                 image_path=None, image_scale_width=1, image_scale_height=1, image_anchor="center",
                 drawing=False,
                 response="toggle", status="unclicked",
                 clickable=True,
                 member_clicked_index=None, tab_active=True, tab_reverse=False):

        Labels.__init__(self, surface, name, x, y, width, height,
                        scale_width, scale_height, anchor,
                        members, mapping_position, mapping_bound, mapping_nudge,
                        grid_amount_rows, grid_amount_columns, grid_nudge,
                        grid_drawing_style, grid_drawing_color, grid_drawing_nudge,
                        grid_name, grid_x, grid_y, grid_width, grid_height,
                        grid_scale_width, grid_scale_height, grid_anchor,
                        filling_color,
                        border_thickness, border_radius, border_color,
                        image_path, image_scale_width, image_scale_height, image_anchor,
                        drawing)

        Button.__init__(self, surface, name, x, y, width, height,
                        scale_width, scale_height, anchor,
                        filling_color,
                        border_thickness, border_radius, border_color,
                        response=response, status=status,
                        clickable=clickable)

        self._member_clicked_index = member_clicked_index
        self.tab = {"active": tab_active, "reverse": tab_reverse}

    @property
    def clickable(self):
        return super().clickable

    @clickable.setter
    def clickable(self, clickable):
        Button.clickable.fset(self, clickable)
        for member in self.members:
            member.clickable = clickable

    @property
    def tab_active(self):
        return self.tab["active"]

    @tab_active.setter
    def tab_active(self, tab_active):
        self.tab["active"] = tab_active

    @property
    def member_clicked_index(self):
        return self._member_clicked_index

    @member_clicked_index.setter
    def member_clicked_index(self, member_clicked_index):

        self._member_clicked_index = member_clicked_index

        for i, member in enumerate(self.members):
            if self.member_clicked_index == i:
                member.status = "clicked"
            else:
                if member.status == "clicked":
                    member.status = "unclicked"

    @property
    def member_clicked(self):
        return self.members[self.member_clicked_index]

    @property
    def targeted(self):
        return True in [member.targeted for member in self.members]

    def update_member_clicked_index(self, event):

        for i, member in enumerate(self.members):
            if member.clicked(event):
                if self.member_clicked_index not in [None, i]:
                    self.member_clicked.status = "unclicked"
                self.member_clicked_index = i

        if "clicked" not in [member.status for member in self.members]:
            self.member_clicked_index = None

    def update_tab_reverse(self, event):

        if event.type == pg.KEYDOWN:
            if event.key in {pg.K_RSHIFT, pg.K_LSHIFT}:
                self.tab["reverse"] = True

        if event.type == pg.KEYUP:
            if event.key in {pg.K_RSHIFT, pg.K_LSHIFT}:
                self.tab["reverse"] = False

    def update_tab(self, event):

        if self.tab_active and self.status == "clicked":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    if self.member_clicked_index is not None:
                        if self.members[self.member_clicked_index].status == "clicked":

                            member_clicked_index_old = self.member_clicked_index
                            tab_reverse_to_int = -1 if self.tab["reverse"] else 1
                            member_clicked_index_new = (member_clicked_index_old + tab_reverse_to_int) % self.amount

                            self.members[member_clicked_index_old].status = "unclicked"
                            self.members[member_clicked_index_new].status = "clicked"

                            self.member_clicked_index = member_clicked_index_new

    def update(self, event):

        Labels.update(self, event)
        Button.update(self, event)

        self.update_member_clicked_index(event)
        self.update_tab_reverse(event)
        self.update_tab(event)

    def clicked(self, event):
        return True in [member.clicked(event) for member in self.members]

class TextBoxes(Buttons):

    def entered(self, event):
        return True in [member.entered(event) for member in self.members]

    def content(self):
        return {member.name: member.content for member in self.members}

# ---------------------------------------------------------------- #

class Album(Boxes):

    def __init__(self, surface, name="", x=None, y=None, width=0, height=0,
                 scale_width=1, scale_height=1, anchor="center",
                 members=None):

        if x is None: x = surface.get_width() // 2
        if y is None: y = surface.get_height() // 2

        super().__init__(surface, name, x, y, width, height,
                         scale_width, scale_height, anchor,
                         members)

        if self.empty:
            self._page_index = None
        else:
            self._page_index = 0
            for page in self.pages:
                page.position = self.position

    @property
    def page_index(self):
        if self.empty: self._page_index = None
        return self._page_index

    @page_index.setter
    def page_index(self, page_index):
        self._page_index = None if self.empty else page_index

    @property
    def position(self):
        return super().position

    @position.setter
    def position(self, position):
        super(Album, self.__class__).position.fset(self, position)
        for page in self.pages:
            page.position = self.position

    def page_index_new(self, direction):
        if self.page_index is None:
            return None
        else:
            if direction == "next":
                return self.page_index + 1
            if direction == "back":
                return self.page_index - 1

    @property
    def pages(self):
        return self.members

    @pages.setter
    def pages(self, pages):
        self.pages = pages

    @property
    def pages_amount(self):
        return len(self.pages)

    @property
    def empty(self):
        return self.pages_amount == 0

    def on_page(self, index):
        return 0 <= index <= len(self.pages)-1

    @property
    def on_first_page(self):
        return self.page_index == 0

    @property
    def on_last_page(self):
        return self.page_index == len(self.pages)-1

    @property
    def on_middle_page(self):
        return 0 < self.page_index < len(self.pages)-1

    def can_move(self, direction):
        if self.page_index is None:
            return False
        else:
            return self.on_page(self.page_index_new(direction))
    
    @property
    def page_current(self):
        return self.pages[self.page_index]

    def page_new(self, direction):
        return self.pages[self.page_index_new(direction)]

    def move(self, direction):
        assert self.can_move(direction)
        self.page_index = self.page_index_new(direction)

    def draw(self):
        if not self.empty:
            self.page_current.draw()

    def update(self, event):
        if not self.empty:
            self.page_current.update(event)

# ---------------------------------------------------------------- #
