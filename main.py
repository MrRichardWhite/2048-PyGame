# ---------------------------------------------------------------- #

import time
import csv
import pygame as pg

from widgets.single import *
from widgets.utils  import *
from widgets.multi  import *

from classes import *
from constants import *

# ---------------------------------------------------------------- #

pg.init()

pg.display.set_caption("2048")

screen = pg.display.set_mode(SCREEN_MIN_DIMENSIONS, pg.RESIZABLE)
screen.fill(COLOR_BG)

icon = pg.image.load("icon.png")
pg.display.set_icon(icon)

# ---------------------------------------------------------------- #

def boards(screen):

    saving = False

    boards_members = []
    players = []
    with open("boards.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        next(csv_reader)
        for csv_player, csv_name, csv_skin, csv_contents in csv_reader:

            board_member_ids = [int(n) for n in csv_contents[1:-1].split(", ")]
            board_dimension = int(np.sqrt(len(board_member_ids)))
            board_members = [
                Tile(screen, f"field ({n % board_dimension}, {n // board_dimension})", id=id, skin=csv_skin)
                for n, id in zip(range(board_dimension ** 2), board_member_ids)
            ]

            board = Board(screen, csv_name, members=board_members, dimension=board_dimension, skin=csv_skin)
            boards_members.append(board)
            players.append(Player(csv_player))

    boards = Album(screen, "boards", members=boards_members)

    button_menu = Button(screen, "menu", width=256, height=64,
                         filling_color=colors["grey"],
                         border_radius=4,
                         text_string="Menu", text_color=colors["white"],
                         font_type=clear_sans["bold"], font_size=36,
                         response="hold",
                         filling_color_unclicked=colors["grey"], filling_color_semiclicked=colors[32])

    button_back = Button(screen, "back", width=256, height=64,
                         filling_color=colors[128],
                         border_radius=4,
                         text_string="Back", text_color=colors["white"],
                         font_type=clear_sans["bold"], font_size=40,
                         response="hold",
                         filling_color_semiclicked=colors["green"],
                         unclickable_outside=False)

    button_play = Button(screen, "play", width=256, height=64,
                         filling_color=colors[128],
                         border_radius=4,
                         text_string="Play", text_color=colors["white"],
                         font_type=clear_sans["bold"], font_size=40,
                         response="hold",
                         filling_color_semiclicked=colors["green"],
                         unclickable_outside=False)

    text_box_board_name = TextBox(screen, "board name", width=256, height=64,
                                  filling_color=COLOR_BG,
                                  border_radius=4, border_thickness=6,
                                  font_type=clear_sans["bold"], font_size=36,
                                  border_color_unclicked=colors[32], border_color_semiclicked=colors[128], border_color_clicked=colors["green"],
                                  text_color_unclicked=colors[32], text_color_semiclicked=colors[128], text_color_clicked=colors["green"])

    if not boards.empty:
        text_box_board_name.text_string_clicked = boards.page_current.name

    button_delete_board = Button(screen, "delete board", width=64, height=64,
                                 filling_color=colors[64],
                                 border_radius=4,
                                 image_path="trash_can.png", image_scale_width=0.4, image_scale_height=0.4,
                                 text_color=colors["white"],
                                 font_type=clear_sans["bold"], font_size=40,
                                 response="hold",
                                 filling_color_semiclicked=colors["green"],
                                 unclickable_outside=False)

    button_next = Button(screen, "next", width=256, height=64,
                         filling_color=colors[128],
                         border_radius=4,
                         text_string="Next", text_color=colors["white"],
                         font_type=clear_sans["bold"], font_size=40,
                         response="hold",
                         filling_color_semiclicked=colors["green"],
                         unclickable_outside=False)

    rhs = Boxes(screen, "rhs",
                grid_amount_rows=6, grid_amount_columns=2,
                members=[button_menu, button_back, button_play, text_box_board_name, button_delete_board, button_next],
                mapping_position={0: (0, 0), 1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3), 5: (0, 4)},
                mapping_nudge="inner")

    boxes_boards = Boxes(screen, "boxes play",
                         grid_amount_rows=9+1, grid_amount_columns=16+1,
                         members=[boards, rhs],
                         mapping_position={0: (4, 4), 1: (12-2, 0)},
                         mapping_bound={1: (12+2, 8)},
                         mapping_nudge="inner")

    boxes_boards.width = screen.get_width()
    boxes_boards.height = screen.get_height()
    rhs.width = screen.get_width() / 4
    rhs.height = screen.get_height()

    boxes_boards.update_members_position()
    boxes_boards.update_members_bound()
    if not boards.empty:
        boards.page_current.update_members_position()
        boards.page_current.update_members_bound()
    rhs.update_members_position()
    rhs.update_members_bound()

    run = True
    while run:

        pg.time.delay(DELAY)

        pg.display.update()
        screen.fill(COLOR_BG)

        boards.draw()
        if boards.empty:
            button_menu.draw()
        else:
            if not boards.on_first_page: button_back.draw()
            else: button_menu.draw()
            if not boards.on_last_page: button_next.draw()
            button_play.draw()
            text_box_board_name.draw()
            button_delete_board.draw()

        for event in pg.event.get():

            if event.type == pg.QUIT: run = False

            if event.type == pg.VIDEORESIZE:

                    width, height = event.size

                    if width < SCREEN_MIN_WIDTH: width = SCREEN_MIN_WIDTH
                    if height < SCREEN_MIN_HEIGHT: height = SCREEN_MIN_HEIGHT

                    screen = pg.display.set_mode((width, height), pg.RESIZABLE)

                    boxes_boards.width = screen.get_width()
                    boxes_boards.height = screen.get_height()
                    rhs.width = screen.get_width() / 4
                    rhs.height = screen.get_height()

                    boxes_boards.update_members_position()
                    boxes_boards.update_members_bound()
                    if not boards.empty:
                        boards.page_current.update_members_position()
                        boards.page_current.update_members_bound()
                    rhs.update_members_position()
                    rhs.update_members_bound()

            if boards.empty:
                button_menu.update(event)
            else:
                if not boards.on_first_page: button_back.update(event)
                else: button_menu.update(event)
                if not boards.on_last_page: button_next.update(event)
                button_play.update(event)
                text_box_board_name.update(event)
                button_delete_board.update(event)

            if ((boards.on_first_page or boards.empty) and button_menu.clicked(event)) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if saving: save_to_boards_file(boards.members, players, overwrite=True)
                return run, screen

            if not boards.empty:

                if button_play.clicked(event):
                    if saving: save_to_boards_file(boards.members, players, overwrite=True)
                    return setup(screen, players[boards.page_index], boards.page_current)

                if text_box_board_name.entered(event):
                    if boards.page_current.name != text_box_board_name.text_string:
                        boards.page_current.name = text_box_board_name.text_string
                        saving = True

                if button_delete_board.clicked(event):
                    del boards.members[boards._page_index]
                    del players[boards._page_index]
                    if not boards.empty:
                        if boards._page_index > boards.pages_amount-1:
                            boards._page_index -= 1
                        text_box_board_name.text_string_clicked = boards.page_current.name
                    saving = True
                    break

                if not boards.on_first_page:
                    if button_back.clicked(event) or (event.type == pg.KEYDOWN and event.key in [pg.K_LEFT, pg.K_UP]):
                        boards.move("back")
                        text_box_board_name.text_string_clicked = boards.page_current.name
                if not boards.on_last_page:
                    if button_next.clicked(event) or (event.type == pg.KEYDOWN and event.key in [pg.K_RIGHT, pg.K_DOWN]):
                        boards.move("next")
                        text_box_board_name.text_string_clicked = boards.page_current.name

    return run, screen

def high_scores(screen):

    with open("high_scores.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        high_scores_list = [(csv_player, int(csv_dimension), int(csv_score))
                            for csv_player, csv_dimension, csv_score in csv_reader]
        high_scores_list = sorted(high_scores_list, key=lambda x: (x[1], -x[2]))

    WIDTH = 3
    HEIGHT = 5

    pages = []
    lines = []
    for i, (player, dimension, score) in enumerate(high_scores_list):
        if i % HEIGHT == 0: lines = [["Player", "Dimension", "Score"]]
        lines.append([player, str(dimension), str(score)])
        if (i + 1) % HEIGHT == 0: pages.append(lines)

    if lines != []: pages.append(lines)

    tables_members = []
    for i, page in enumerate(pages):

        text_strings = []
        for line in page: text_strings += line

        members = [
            Label(screen, text_string.lower(), width=0, height=0,
                  text_string=text_string, text_color=colors["white"],
                  font_type=clear_sans["bold"], font_size=32)
            for text_string in text_strings
        ]
        mapping_position = {n: (n % WIDTH, n // WIDTH) for n in range(len(text_strings))}

        member = Labels(screen, f"table {i}", width=512+256, height=512-128,
                        anchor="center",
                        grid_amount_rows=7, grid_amount_columns=4,
                        grid_drawing_style="lines inner mixed", grid_drawing_color=COLOR_BG,
                        members=members, mapping_position=mapping_position,
                        mapping_nudge="inner", filling_color=colors["dark grey"],
                        border_radius=4,
                        drawing=True)

        tables_members.append(member)

    button_menu = Button(screen, "menu", width=256, height=64,
                         filling_color=colors["grey"],
                         border_radius=4,
                         text_string="Menu", text_color=colors["white"],
                         font_type=clear_sans["bold"], font_size=36,
                         response="hold",
                         filling_color_unclicked=colors["grey"], filling_color_semiclicked=colors[32])

    button_next = Button(screen, "button next", width=256, height=64,
                         filling_color=colors[128],
                         border_radius=4,
                         text_string=f"Next", text_color=colors["white"],
                         font_type=clear_sans["bold"], font_size=36,
                         response="hold",
                         filling_color_semiclicked=colors["green"],
                         unclickable_outside=False)

    button_back = Button(screen, "button back", width=256, height=64,
                         filling_color=colors[128],
                         border_radius=4,
                         text_string=f"Back", text_color=colors["white"],
                         font_type=clear_sans["bold"], font_size=36,
                         response="hold",
                         filling_color_semiclicked=colors["green"],
                         unclickable_outside=False)

    tables = Album(screen, "tables", members=tables_members)

    boxes_high_scores = Boxes(screen, name="boxes high scores",
                              grid_amount_rows=12, grid_amount_columns=4,
                              members=[button_menu, tables, button_back, button_next],
                              mapping_position={"tables": (1, 4), "button back": (0, 9), "menu": (0, 9), "button next": (2, 9)},
                              mapping_nudge="inner")

    boxes_high_scores.width = screen.get_width()
    boxes_high_scores.height = screen.get_height()

    boxes_high_scores.update_members_position()
    boxes_high_scores.update_members_bound()
    for page in tables:
        page.update_members_position()
        page.update_members_bound()

    run = True
    while run:

        pg.time.delay(DELAY)

        pg.display.update()
        screen.fill(COLOR_BG)

        tables.draw()
        if tables.empty:
            button_menu.draw()
        else:
            if not tables.on_first_page: button_back.draw()
            else: button_menu.draw()
            if not tables.on_last_page: button_next.draw()

        for event in pg.event.get():

            if event.type == pg.QUIT: run = False

            if event.type == pg.VIDEORESIZE:

                    width, height = event.size

                    if width < SCREEN_MIN_WIDTH: width = SCREEN_MIN_WIDTH
                    if height < SCREEN_MIN_HEIGHT: height = SCREEN_MIN_HEIGHT

                    screen = pg.display.set_mode((width, height), pg.RESIZABLE)

                    boxes_high_scores.width = screen.get_width()
                    boxes_high_scores.height = screen.get_height()

                    boxes_high_scores.update_members_position()
                    boxes_high_scores.update_members_bound()
                    for page in tables:
                        page.update_members_position()
                        page.update_members_bound()

            if tables.empty:
                button_menu.update(event)
            else:
                if not tables.on_first_page: button_back.update(event)
                else: button_menu.update(event)
                if not tables.on_last_page: button_next.update(event)

            if ((tables.on_first_page or tables.empty) and button_menu.clicked(event)) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return run, screen

            if not tables.empty:
                if not tables.on_first_page:
                    if button_back.clicked(event) or (event.type == pg.KEYDOWN and event.key in [pg.K_LEFT, pg.K_UP]):
                        tables.move("back")
                if not tables.on_last_page:
                    if button_next.clicked(event) or (event.type == pg.KEYDOWN and event.key in [pg.K_RIGHT, pg.K_DOWN]):
                        tables.move("next")


    return run, screen

def play(screen, player, dimension=4, skin="standard", board=None):

    if board is None: board = Board(screen, "board", dimension=dimension, skin=skin)

    game = Game(screen, board, player)

    save_game = Button(screen, "save game", width=256, height=64,
                       border_radius=4,
                       text_string="Save Game", text_color=colors["white"],
                       filling_color=colors[128], filling_color_semiclicked=colors["green"],
                       font_type=clear_sans["bold"], font_size=36,
                       response="hold")

    quit_game = Button(screen, "quit game", width=256, height=64,
                       border_radius=4,
                       text_string="Quit Game", text_color=colors["white"],
                       font_type=clear_sans["bold"], font_size=36,
                       response="hold",
                       filling_color_unclicked=colors["grey"], filling_color_semiclicked=colors[32])

    menu_buttons = Buttons(screen, "menu buttons", width=0, height=64+16,
                           grid_amount_rows=2, grid_amount_columns=1,
                           anchor="center",
                           members=[save_game, quit_game],
                           mapping_position={0: (0, 0), 1: (0, 1)})

    score_board = Labels(screen, "score board", width=256+64, height=128+32,
                         anchor="center",
                         grid_amount_rows=1+1, grid_amount_columns=2+1,
                         grid_width=256+64-8,
                         members=[
                            Labels(screen, name, width=128, height=128,
                                   anchor="center",
                                   grid_amount_rows=2+1, grid_amount_columns=1+1,
                                   grid_drawing_style="lines inner dashed", grid_drawing_color=COLOR_BG,
                                   members=[
                                    Label(screen, "upper",  width=0, height=0,
                                          text_string=name.upper(), text_color=colors["white"], font_type=clear_sans["bold"], font_size=32),
                                    Label(screen, "lower",  width=0, height=0,
                                          text_string=str(player.high_score(dimension)), text_color=colors["white"], font_type=clear_sans["bold"], font_size=32),
                                   ],
                                   mapping_position={0: (0, 0), 1: (0, 1)}, mapping_nudge="inner",
                                   filling_color=colors["light grey"],
                                   border_radius=4,
                                   drawing=True)
                            for name in ["score", "best"]
                         ],
                         mapping_position={0: (0, 0), 1: (1, 0)}, mapping_nudge="inner",
                         filling_color=colors["grey"],
                         border_radius=4,
                         drawing=True)

    arrows = Buttons(screen, "arrows", width=2*64+2*8, height=64+8,
                     anchor="center",
                     grid_amount_rows=2, grid_amount_columns=3,
                     members=[
                          Button(screen, name, width=64, height=64,
                                 filling_color=colors["light grey"],
                                 border_thickness=8, border_radius=4, border_color=colors["grey"],
                                 text_string=text_string, text_color=colors["white"], font_size=32,
                                 response="hold",
                                 filling_color_semiclicked=colors[128], filling_color_clicked=colors[32],
                                 border_color_semiclicked=colors[512], border_color_clicked=colors[64])
                          for name, text_string in zip(["up", "down", "left", "right"], ["↑", "↓", "←", "→"])
                     ],
                     mapping_position={0: (1, 0), 1: (1, 1), 2: (0, 1), 3: (2, 1)})

    rhs = Boxes(screen, "rhs",
                grid_amount_rows=101, grid_amount_columns=2,
                members=[score_board, menu_buttons, arrows], mapping_position={0: (0, 17), 1: (0, 55), 2: (0, 91)}, mapping_nudge="inner")

    boxes_play = Boxes(screen, "boxes play",
                       grid_amount_rows=9+1, grid_amount_columns=16+1,
                       members=[board, rhs], mapping_position={0: (4, 4), 1: (12-2, 0)}, mapping_bound={1: (12+2, 8)},
                       mapping_nudge="inner")

    boxes_play.width = screen.get_width()
    boxes_play.height = screen.get_height()
    rhs.width = screen.get_width() / 4
    rhs.height = screen.get_height()

    boxes_play.update_members_position()
    boxes_play.update_members_bound()
    rhs.update_members_position()
    rhs.update_members_bound()
    arrows.update_members_position()
    arrows.update_members_bound()
    board.update_members_position()
    board.update_members_bound()

    game.set_up()

    run = True
    while run:

        pg.time.delay(DELAY)

        pg.display.update()
        screen.fill(COLOR_BG)

        game.update_animations()

        score_board["score"]["lower"].text_string = str(board.score)
        score_board["best"]["lower"].text_string = str(max(
            int(score_board["best"]["lower"].text_string),
            int(score_board["score"]["lower"].text_string)
        ))

        draw(boxes_play)
        game.draw()

        for event in pg.event.get():

            if event.type == pg.QUIT:
                game.update_high_score()
                run = False

            if event.type == pg.VIDEORESIZE:

                width, height = event.size

                if width < SCREEN_MIN_WIDTH: width = SCREEN_MIN_WIDTH
                if height < SCREEN_MIN_HEIGHT: height = SCREEN_MIN_HEIGHT

                screen = pg.display.set_mode((width, height), pg.RESIZABLE)

                boxes_play.width = screen.get_width()
                boxes_play.height = screen.get_height()
                rhs.width = screen.get_width() / 4
                rhs.height = screen.get_height()

                boxes_play.update_members_position()
                boxes_play.update_members_bound()
                rhs.update_members_position()
                rhs.update_members_bound()
                arrows.update_members_position()
                arrows.update_members_bound()
                board.update_members_position()
                board.update_members_bound()

            menu_buttons.update(event)
            arrows.update(event)

            if save_game.clicked(event):
                game.save()

            if quit_game.clicked(event) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                game.update_high_score()
                return run, screen

            for direction, key in zip(["up", "down", "left", "right"]*2,
                                      [pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT] + [pg.K_w, pg.K_s, pg.K_a, pg.K_d]):
                if (event.type == pg.KEYDOWN and event.key == key) or arrows[direction].clicked(event):
                    game.move_tiles(direction)

    return run, screen

def setup(screen, player=None, board=None):

    if player is None:
        with open("boards.csv", "r") as csv_file:
            *_, (player_name, _, _, _) = csv.reader(csv_file, delimiter=";")
    else:
        player_name = player.name

    description_names = Label(screen, "description names", width=400, height=20,
                              filling_color=COLOR_BG,
                              text_string="Please enter your player name ...", text_color=colors["grey"],
                              font_type=clear_sans["bold"], font_size=40)

    text_box_player = TextBox(screen, "text box player", width=256, height=64,
                              filling_color=COLOR_BG,
                              border_radius=4, border_thickness=6,
                              font_type=clear_sans["bold"], font_size=36,
                              border_color_unclicked=colors[32], border_color_semiclicked=colors[128], border_color_clicked=colors["green"],
                              text_color_unclicked=colors[32], text_color_semiclicked=colors[128], text_color_clicked=colors["green"],
                              text_string_clicked=player_name)

    if player is not None: text_box_player.text_string_clicked = player.name

    description_dimension = Label(screen, "description dimension", width=400, height=20,
                                  filling_color=COLOR_BG,
                                  text_string="Please select the dimension that you want to play with ...", text_color=colors["grey"],
                                  font_type=clear_sans["bold"], font_size=40)

    buttons_dimension = Buttons(screen, "buttons dimension",
                                grid_amount_columns=4,
                                members=[Button(screen, f"button dimension {n}", width=64, height=64,
                                                border_radius=4,
                                                text_string=str(n), text_color=colors["white"],
                                                font_type=clear_sans["bold"], font_size=40,
                                                filling_color_unclicked=colors[32], filling_color_semiclicked=colors[128], filling_color_clicked=colors["green"],
                                                unclickable_outside=False)
                                        for n in [3, 4, 5, 6]],
                                mapping_position={n: (n, 0) for n in range(4)})

    if board is not None:
        buttons_dimension.clickable = False
        for i, button_dimension in enumerate(buttons_dimension):
            if board.dimension-3 != i:
                button_dimension.filling_color = colors["light grey"]

    description_skin = Label(screen, "description skin", width=400, height=20,
                             filling_color=COLOR_BG,
                             text_string="Please select a skin ...", text_color=colors["grey"],
                             font_type=clear_sans["bold"], font_size=40)

    buttons_skin = Buttons(screen, "buttons skin",
                                grid_amount_columns=2,
                                members=[Button(screen, f"button skin {skin}", width=256, height=64,
                                                border_radius=4,
                                                text_string=skin, text_color=colors["white"],
                                                font_type=clear_sans["bold"], font_size=40,
                                                filling_color_unclicked=colors[32], filling_color_semiclicked=colors[128], filling_color_clicked=colors["green"],
                                                unclickable_outside=False)
                                        for skin in ["standard", "periodic table"]],
                                mapping_position={n: (n, 0) for n in range(2)})

    buttons_move = Buttons(screen, "buttons move",
                           grid_amount_columns=2,
                           members=[Button(screen, f"button move {direction}", width=256, height=64,
                                           filling_color=colors[128],
                                           border_radius=4,
                                           text_string=direction.title(), text_color=colors["white"],
                                           font_type=clear_sans["bold"], font_size=40,
                                           response="hold",
                                           filling_color_semiclicked=colors["green"],
                                           unclickable_outside=False)
                                       for direction in ["back", "next"]],
                           mapping_position={0: (0, 0), 1: (1, 0)})

    boxes_setup = Boxes(screen, name="boxes setup",
                        grid_amount_rows=32, grid_amount_columns=7,
                        members=[description_names, text_box_player, description_dimension, buttons_dimension, description_skin, buttons_skin, buttons_move],
                        mapping_position={
                                                          "description names":     (3, 2),
                                                          "text box player":       (3, 6),
                                                          "description dimension": (3, 10),
                            "buttons dimension": (2, 14),
                                                          "description skin":      (3, 18),
                            "buttons skin":      (2, 22),
                            "buttons move":      (2, 28),
                        },
                        mapping_bound={
                            "buttons dimension": (4, 14+2),
                            "buttons skin":      (4, 22+2),
                            "buttons move":      (4, 28+2),
                        })

    boxes_setup.width = screen.get_width()
    boxes_setup.height = screen.get_height()

    boxes_setup.update_members_position()
    boxes_setup.update_members_bound()
    buttons_dimension.update_members_position()
    buttons_dimension.update_members_bound()
    buttons_skin.update_members_position()
    buttons_skin.update_members_bound()
    buttons_move.update_members_position()
    buttons_move.update_members_bound()

    if board is None:
        buttons_dimension.member_clicked_index = 1
        buttons_skin.member_clicked_index = 1
    else:
        buttons_dimension.member_clicked_index = board.dimension - 3
        if board.skin == "standard":
            buttons_skin.member_clicked_index = 0
        if board.skin == "periodic table":
            buttons_skin.member_clicked_index = 1

    run = True
    while run:

        pg.time.delay(DELAY)

        pg.display.update()
        screen.fill(COLOR_BG)

        boxes_setup.draw()

        for event in pg.event.get():

            if event.type == pg.QUIT: run = False

            if event.type == pg.VIDEORESIZE:

                    width, height = event.size

                    if width < SCREEN_MIN_WIDTH: width = SCREEN_MIN_WIDTH
                    if height < SCREEN_MIN_HEIGHT: height = SCREEN_MIN_HEIGHT

                    screen = pg.display.set_mode((width, height), pg.RESIZABLE)

                    boxes_setup.width = screen.get_width()
                    boxes_setup.height = screen.get_height()

                    boxes_setup.update_members_position()
                    boxes_setup.update_members_bound()
                    buttons_dimension.update_members_position()
                    buttons_dimension.update_members_bound()
                    buttons_skin.update_members_position()
                    buttons_skin.update_members_bound()
                    buttons_move.update_members_position()
                    buttons_move.update_members_bound()

            boxes_setup.update(event)

            if buttons_move["button move back"].clicked(event) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return run, screen

            if buttons_move["button move next"].clicked(event) or (event.type == pg.KEYDOWN and event.key == pg.K_RETURN):
                if board is None:
                    return play(screen, Player(text_box_player.text_string),
                                dimension=buttons_dimension.member_clicked_index+3, skin=buttons_skin.member_clicked.text_string)
                else:
                    board.skin = buttons_skin.member_clicked.text_string
                    board.update()
                    return play(screen, Player(text_box_player.text_string),
                                board=board)

    return run, screen

def menu(screen):

    title = Label(screen, "title", width=400, height=40,
                  filling_color=COLOR_BG,
                  text_string="2048", text_color=colors["dark grey"],
                  font_type=clear_sans["bold"], font_size=80)

    sub_title = Label(screen, "sub title", width=400, height=20,
                      filling_color=COLOR_BG,
                      text_string="... in 3, 4, 5 and 6 dimensions", text_color=colors["light grey"],
                      font_type=clear_sans["bold"], font_size=40)

    quit = Button(screen, "quit", width=256, height=64,
                  border_radius=4,
                  text_string="Quit", text_color=colors["white"],
                  font_type=clear_sans["bold"], font_size=36,
                  response="hold",
                  filling_color_unclicked=colors["grey"], filling_color_semiclicked=colors[32])

    menu_buttons = Buttons(screen, "menu buttons", width=1920/2/3, height=1080/2/4,
                           grid_amount_rows=2, grid_amount_columns=2,
                           anchor="center",
                           members=[Button(screen, button_name.lower(), width=256, height=64,
                                           filling_color=colors[128],
                                           border_radius=4,
                                           text_string=button_name.title(), text_color=colors["white"],
                                           filling_color_semiclicked=colors["green"],
                                           font_type=clear_sans["bold"], font_size=36,
                                           response="hold")
                                    for i, button_name in enumerate(["play", "high scores", "boards"])] + [quit],
                           mapping_position={0: (0, 0), 1: (0, 1), 2: (1, 0), 3: (1, 1)})

    boxes_menu = Boxes(screen, name="boxes menu",
                       grid_amount_rows=12, grid_amount_columns=2,
                       members=[title, sub_title, menu_buttons],
                       mapping_position={"title": (0, 2), "sub title": (0, 3), "menu buttons": (0, 7)},
                       mapping_nudge="inner")

    boxes_menu.update_members_position()
    boxes_menu.update_members_bound()
    menu_buttons.update_members_position()
    menu_buttons.update_members_bound()

    run = True
    while run:

        pg.time.delay(DELAY)

        pg.display.update()
        screen.fill(COLOR_BG)

        boxes_menu.draw()

        for event in pg.event.get():

            if event.type == pg.QUIT or quit.clicked(event) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): run = False

            if event.type == pg.VIDEORESIZE:

                    width, height = event.size
                    
                    if width < SCREEN_MIN_WIDTH: width = SCREEN_MIN_WIDTH
                    if height < SCREEN_MIN_HEIGHT: height = SCREEN_MIN_HEIGHT

                    screen = pg.display.set_mode((width, height), pg.RESIZABLE)

                    boxes_menu.width = screen.get_width()
                    boxes_menu.height = screen.get_height()

                    boxes_menu.update_members_position()
                    boxes_menu.update_members_bound()
                    menu_buttons.update_members_position()
                    menu_buttons.update_members_bound()

            boxes_menu.update(event)

            for button_name, function in zip(["play", "high scores", "boards"],
                                             [setup, high_scores, boards]):
                if menu_buttons[button_name].clicked(event):

                    run, screen = function(screen)

                    boxes_menu.width = screen.get_width()
                    boxes_menu.height = screen.get_height()

                    boxes_menu.update_members_position()
                    boxes_menu.update_members_bound()
                    menu_buttons.update_members_position()
                    menu_buttons.update_members_bound()

                    break

    pg.quit()

# ---------------------------------------------------------------- #

if __name__ == "__main__":
    menu(screen)

# ---------------------------------------------------------------- #
