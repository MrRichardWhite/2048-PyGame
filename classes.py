# ---------------------------------------------------------------- #

import random
import csv

import pygame as pg
import numpy  as np

from widgets.single import *
from widgets.utils  import *
from widgets.multi  import *

from constants import *

# ---------------------------------------------------------------- #

def save_to_boards_file(b, p, overwrite=False):

    if type(b) is list and type(p) is list:

        if overwrite:
            with open("boards.csv", "w") as csv_file:
                csv_file.write("player;name;skin;contents")


        for board, player in zip(b, p):
            save_to_boards_file(board, player)

    else:

        board = b; player = p
        with open("boards.csv", "a") as csv_file:
            csv_file.write("\n" + f"{player.name};{board.name};{board.skin};{[field.id for field in board]}")

# ---------------------------------------------------------------- #

class Tile(Label):

    def __init__(self, surface, name="", x=0, y=0, width=64, height=64,
                 scale_width=1, scale_height=1,
                 id=0, skin="standard"):

        self.id = id

        if self.id == 0:
            super().__init__(surface, name, x, y, width, height,
                             scale_width, scale_height,
                             border_radius=4,
                             filling_color=colors["light grey"])
        else:
            super().__init__(surface, name, x, y, width, height,
                             scale_width, scale_height,
                             filling_color=colors[2**id], border_radius=4,
                             text_string=skins[skin][2**id], text_color=text_colors[2**id],
                             font_type=clear_sans["bold"], font_size=font_sizes[skin][2**id])

class Board(Labels):

    def __init__(self, surface, name, x=0, y=0,
                 scale_width=1, scale_height=1, anchor="center",
                 members=None,
                 dimension=4, skin="standard"):

        if members is None:
            members = [Tile(surface, f"field ({n % dimension}, {n // dimension})", skin=skin) for n in range(dimension ** 2)]
        else:
            assert type(members) is list
            assert dimension == int(np.sqrt(len(members)))

        self.dimension = dimension
        self.skin = skin

        width = height = dimension * 64 + dimension * 16
        border_radius = 4
        grid_amount_columns = grid_amount_rows = dimension + 1
        grid_width  = width  - 8
        grid_height = height - 8
        filling_color = colors["grey"]
        mapping_position = {n: (n % dimension, n // dimension) for n in range(dimension ** 2)}
        mapping_nudge = "inner"
        drawing = True

        super().__init__(surface, name, x, y, width, height,
                         scale_width, scale_height, anchor,
                         grid_amount_rows=grid_amount_rows, grid_amount_columns=grid_amount_columns, grid_nudge=None,
                         grid_drawing_style=None, grid_drawing_color=None, grid_drawing_nudge=None,
                         grid_name=None, grid_x=None, grid_y=None, grid_width=grid_width, grid_height=grid_height,
                         grid_scale_width=None, grid_scale_height=None, grid_anchor=None,
                         members=members, mapping_position=mapping_position, mapping_bound=None, mapping_nudge=mapping_nudge,
                         filling_color=filling_color,
                         border_thickness=0, border_radius=border_radius, border_color=pg.Color("black"),
                         drawing=drawing)

        self.reserved_tiles_indices = []

    @property
    def tiles(self):
        return self.members

    @property
    def score(self):
        return sum([2 ** tile.id for tile in self.tiles if tile.id > 0])

    def __getitem__(self, key):

        if type(key) is int:
            return self.members[key]

        if type(key) in [list, tuple, np.ndarray]:
            i, j = key
            return self.members[self.dimension * i + j]

    def __setitem__(self, key, value):

        if type(key) is int:
            value.name = self.members[key].name
            value.position = self.members[key].position
            self.members[key] = value

        if type(key) in [list, tuple, np.ndarray]:
            i, j = key
            value.name = self.members[self.dimension * i + j].name
            value.position = self.members[self.dimension * i + j].position
            self.members[self.dimension * i + j] = value

    @property
    def full_tiles_indices(self):
        return [i for i, tile in enumerate(self.members) if tile.id != 0]

    @property
    def full_tiles(self):
        return [tile for tile in self.members if tile.id != 0]

    @property
    def empty_tiles_indices(self):
        return [i for i, tile in enumerate(self.members) if tile.id == 0]

    @property
    def empty_tiles(self):
        return [tile for tile in self.members if tile.id == 0]

    def spawn_tile(self, include=None, exclude=None):

        if include is None: include = self.empty_tiles_indices
        if exclude is None: exclude = []
        if type(exclude) is int: exclude = [exclude]
        if type(include) is int: include = [include]

        index = random.choice([i for i in include if i not in exclude + self.reserved_tiles_indices])
        id = 1 if random.random() < 0.9 else 2
        return Tile(self.surface, x=self[index].x, y=self[index].y, scale_width=0, scale_height=0, id=id, skin=self.skin), index

    def spawn_tiles(self, amount=1, include=None, exclude=None):

        if include is None: include = self.empty_tiles_indices
        if exclude is None: exclude = []
        if type(exclude) is int: exclude = [exclude]
        if type(include) is int: include = [include]

        tiles = []
        tiles_indices = []

        for _ in range(amount):
            tile, index = self.spawn_tile(include=include, exclude=exclude)
            exclude.append(index)
            tiles.append(tile)
            tiles_indices.append(index)

        return tiles, tiles_indices

    def tiles_moving_info(self, direction):

        tiles_moving_info = []
        id_matrix    = [[self[i, j].id for j in range(self.dimension)] for i in range(self.dimension)]
        merge_matrix = [[False         for j in range(self.dimension)] for i in range(self.dimension)]

        if direction == "up":

            for i in range(1, self.dimension):
                for j in range(self.dimension):
                    if id_matrix[i][j] != 0:

                        i_new = i; j_new = j
                        while i_new-1 >= 0 and id_matrix[i_new-1][j] == 0:
                            id_matrix[i_new-1][j] = id_matrix[i_new][j]
                            id_matrix[i_new][j] = 0
                            i_new -= 1

                        merge = False
                        if i_new-1 >= 0 and id_matrix[i_new-1][j] == id_matrix[i_new][j] and not merge_matrix[i_new-1][j]:
                            id_matrix[i_new][j] = 0
                            merge_matrix[i_new-1][j] = True
                            i_new -= 1
                            merge = True

                        if i_new != i:
                            tiles_moving_info.append(((i, j), (i_new, j_new), merge))

        if direction == "down":

            for i in range(self.dimension-1, -1, -1):
                for j in range(self.dimension):
                    if id_matrix[i][j] != 0:

                        i_new = i; j_new = j
                        while i_new+1 < self.dimension and id_matrix[i_new+1][j] == 0:
                            id_matrix[i_new+1][j] = id_matrix[i_new][j]
                            id_matrix[i_new][j] = 0
                            i_new += 1

                        merge = False
                        if i_new+1 < self.dimension and id_matrix[i_new+1][j] == id_matrix[i_new][j] and not merge_matrix[i_new+1][j]:
                            id_matrix[i_new][j] = 0
                            merge_matrix[i_new+1][j_new] = True
                            i_new += 1
                            merge = True

                        if i_new != i:
                            tiles_moving_info.append(((i, j), (i_new, j_new), merge))

        if direction == "left":

            for i in range(self.dimension):
                for j in range(1, self.dimension):
                    if id_matrix[i][j] != 0:

                        i_new = i; j_new = j
                        while j_new-1 >= 0 and id_matrix[i][j_new-1] == 0:
                            id_matrix[i][j_new-1] = id_matrix[i][j_new]
                            id_matrix[i][j_new] = 0
                            j_new -= 1

                        merge = False
                        if j_new-1 >= 0 and id_matrix[i][j_new-1] == id_matrix[i][j_new] and not merge_matrix[i][j_new-1]:
                            id_matrix[i][j_new] = 0
                            merge_matrix[i][j_new-1] = True
                            j_new -= 1
                            merge = True

                        if j_new != j:
                            tiles_moving_info.append(((i, j), (i_new, j_new), merge))

        if direction == "right":

            for i in range(self.dimension):
                for j in range(self.dimension-1, -1, -1):
                    if id_matrix[i][j] != 0:

                        i_new = i; j_new = j
                        while j_new+1 < self.dimension and id_matrix[i][j_new+1] == 0:
                            id_matrix[i][j_new+1] = id_matrix[i][j_new]
                            id_matrix[i][j_new] = 0
                            j_new += 1

                        merge = False
                        if j_new+1 < self.dimension and id_matrix[i][j_new+1] == id_matrix[i][j_new] and not merge_matrix[i][j_new+1]:
                            id_matrix[i][j_new] = 0
                            merge_matrix[i][j_new+1] = True
                            j_new += 1
                            merge = True

                        if j_new != j:
                            tiles_moving_info.append(((i, j), (i_new, j_new), merge))

        return tiles_moving_info

    def update(self, event=None):

        for i, tile in enumerate(self.tiles):
            self.tiles[i] = Tile(tile.surface, tile.name, id=tile.id, skin=self.skin)

        if event is not None: super().update(event)

class Player(object):

    def __init__(self, name):
        self.name = name

    def high_score(self, dimension):

        high_score = 0

        with open("high_scores.csv", "r") as csv_file:

            csv_reader = csv.reader(csv_file)
            next(csv_reader)

            for csv_name, csv_dimension, csv_score in csv_reader:
                if csv_name == self.name and int(csv_dimension) == dimension:
                    high_score = int(csv_score)
                    break

        return high_score

class Game(object):

    def __init__(self, screen, board, player):
        self.screen = screen
        self.board = board
        self.player = player

    @property
    def dimension(self):
        return self.board.dimension

    @property
    def score(self):
        return self.board.score

    def set_up(self):

        self.animations_dict = {}
        if len(self.board.full_tiles) == 0:
            self.spawning_tiles, self.spawning_tiles_indices = self.board.spawn_tiles(2)
            self.animations_dict["spawning tiles"] = Animations(3, 0, self.spawning_tiles, scale_width_array=[1, 1], scale_height_array=[1, 1])
        else:
            self.spawning_tiles = []

        self.moving_tiles = []

    def draw(self):

        self.board.draw()

        for moving_tile in self.moving_tiles:
            moving_tile.draw()

        for spawning_tile in self.spawning_tiles:
            spawning_tile.draw()

    def move_tiles(self, direction):

        if False not in [animations.done for animations in self.animations_dict.values()]:

            self.moving_tiles = []
            self.tile_indices_new = []
            self.position_array = []
            self.merges = []

            if len(self.board.tiles_moving_info(direction)) > 0:

                for tile_index_old, tile_index_new, merge in self.board.tiles_moving_info(direction):

                    moving_tile = self.board[tile_index_old]
                    self.merges.append(merge)

                    self.moving_tiles.append(moving_tile)
                    self.tile_indices_new.append(tile_index_new)
                    self.board.reserved_tiles_indices.append(tile_index_new)
                    self.position_array.append(self.board[tile_index_new].position)
                    self.board[tile_index_old] = Tile(self.board.surface, x=moving_tile.x, y=moving_tile.y)

                self.animations_dict["moving tiles"] = Animations(3, 0, self.moving_tiles, position_array=self.position_array)
                self.animations_dict["moving tiles"].step()

    def update_animations(self):

        delete_keys = []
        animations_dict_new = {}
        sound_index = -1
        for animations_type, animations in self.animations_dict.items():

            animations.step()

            if animations.done:

                if animations_type == "moving tiles":

                    for tile_index_new, moving_tile in zip(self.tile_indices_new, self.moving_tiles):
                        self.board[tile_index_new] = moving_tile

                    if True in self.merges:

                        box_array = []
                        for tile_index_new, merge in zip(self.tile_indices_new, self.merges):
                            if merge:
                                self.board[tile_index_new] = Tile(self.screen, scale_width=1.25, scale_height=1.25, id=self.board[tile_index_new].id+1, skin=self.board.skin)
                                box_array.append(self.board[tile_index_new])

                        scale_width_array = [1] * len(box_array)
                        scale_height_array = [1] * len(box_array)

                        animations_dict_new["shrinking tiles"] = Animations(3, 0, box_array, scale_width_array=scale_width_array, scale_height_array=scale_height_array)
                        animations_dict_new["shrinking tiles"].step()

                    else:

                        sound_index = max(sound_index, 0)
                        delete_keys.append("moving tiles")

                        spawning_tile, i = self.board.spawn_tile()
                        self.spawning_tiles = [spawning_tile]
                        self.spawning_tiles_indices = [i]

                        animations_dict_new["spawning tiles"] = Animations(3, 0, self.spawning_tiles, scale_width_array=[1]*len(self.spawning_tiles), scale_height_array=[1]*len(self.spawning_tiles))
                        animations_dict_new["spawning tiles"].step()

                    self.moving_tiles = []
                    self.tile_indices_new = []
                    self.position_array = []
                    self.merges = []
                    self.board.reserved_tiles_indices = []

                elif animations_type == "spawning tiles":

                    for spawning_tile_index, spawning_tile in zip(self.spawning_tiles_indices, self.spawning_tiles):
                        self.board[spawning_tile_index] = spawning_tile

                    self.spawning_tiles = []
                    delete_keys.append("spawning tiles")

                elif animations_type == "shrinking tiles":

                    sound_index = max(sound_index, 1)
                    delete_keys.append("shrinking tiles")

        for delete_key in delete_keys:
            del self.animations_dict[delete_key]

        self.animations_dict.update(animations_dict_new)

        if sound_index > -1: sounds[sound_index].play()

    def update_high_score(self):

        high_scores_list = ["player,dimension,score"]
        high_score_new = self.board.score

        with open("high_scores.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for csv_player, csv_dimension, csv_score in csv_reader:
                csv_dimension = int(csv_dimension)
                csv_score = int(csv_score)
                if csv_player == self.player.name and csv_dimension == self.dimension:
                    if csv_score > self.board.score:
                        high_score_new = csv_score
                else:
                    high_scores_list.append(f"{csv_player},{csv_dimension},{csv_score}")

        high_scores_list.append(f"{self.player.name},{self.dimension},{high_score_new}")

        with open("high_scores.csv", "w") as csv_file:
                csv_file.write("\n".join(high_scores_list))

    def save(self):

        board_number = 0
        with open("boards.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            next(csv_reader)
            for csv_player, csv_name, csv_skin, csv_contents in csv_reader:
                board_member_ids = [int(n) for n in csv_contents[1:-1].split(", ")]
                board_dimension = int(np.sqrt(len(board_member_ids)))
                if csv_player == self.player.name and board_dimension == self.board.dimension:
                    board_number += 1

        self.board.name = f"{self.player.name} {self.board.dimension}D {board_number}"

        save_to_boards_file(self.board, self.player)

        self.update_high_score()

# ---------------------------------------------------------------- #
