# ---------------------------------------------------------------- #

import pygame as pg

# ---------------------------------------------------------------- #

SCREEN_MIN_WIDTH = 1920 // 2
SCREEN_MIN_HEIGHT = 1080 // 2
SCREEN_MIN_DIMENSIONS = (SCREEN_MIN_WIDTH, SCREEN_MIN_HEIGHT)

shades_of_grey = {
    "black":            (0, 0, 0),
    "light light grey": (245, 248, 239),
    "light grey":       (202, 192, 181),
    "grey":             (184, 173, 161),
    "dark grey":        (118, 111, 103),
    "white":            (255, 255, 255),
}

filling_colors = {
    2 ** 1:  (236, 228, 219),
    2 ** 2:  (234, 224, 202),
    2 ** 3:  (232, 179, 129),
    2 ** 4:  (223, 145, 95),
    2 ** 5:  (230, 130, 102),
    2 ** 6:  (217, 98,  67),
    2 ** 7:  (238, 217, 123),
    2 ** 8:  (235, 209, 99),
    2 ** 9:  (222, 193, 76),
    2 ** 10: (235, 194, 76),
    2 ** 11: (229, 197, 66),
    2 ** 12: (183, 132, 171),
    2 ** 13: (174, 108, 168),
    2 ** 14: (170, 96,  166),
}

colors = {"green": (144, 204, 103)}
colors.update(shades_of_grey)
colors.update(filling_colors)

COLOR_BG = colors["light light grey"]

clear_sans = {
    type: f"fonts//ClearSans-{type.capitalize().replace(' i', 'I')}.ttf"
    for type in ["bold", "bold italic", "italic", "light", "medium", "medium italic", "regular", "thin"]
}

DELAY = 10

periodic_table = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si"]

skins = {
    "standard": {2**n: str(2**n) for n in range(1, 14+1)},
    "periodic table": {2**n: periodic_table[n-1] for n in range(1, 14+1)}
}

text_colors = {
    2 ** 1:  colors["dark grey"],
    2 ** 2:  colors["dark grey"],
    2 ** 3:  colors["white"],
    2 ** 4:  colors["white"],
    2 ** 5:  colors["white"],
    2 ** 6:  colors["white"],
    2 ** 7:  colors["white"],
    2 ** 8:  colors["white"],
    2 ** 9:  colors["white"],
    2 ** 10: colors["white"],
    2 ** 11: colors["white"],
    2 ** 12: colors["white"],
    2 ** 13: colors["white"],
    2 ** 14: colors["white"],
}

font_sizes = {
    "standard": {
        2 ** 1: 32 + 16,
        2 ** 2: 32 + 16,
        2 ** 3: 32 + 16,
        2 ** 4: 32 + 16,
        2 ** 5: 32 + 16,
        2 ** 6: 32 + 16,
        2 ** 7: 32 + 8,
        2 ** 8: 32 + 8,
        2 ** 9: 32 + 8,
        2 ** 10: 32,
        2 ** 11: 32,
        2 ** 12: 32,
        2 ** 13: 32,
        2 ** 14: 16 + 8,
    },
    "periodic table": {2**n: 32 + 16 for n in range(1, 14+1)},
}

pg.mixer.init()
sounds = [pg.mixer.Sound(f"sounds//{i}.mp3") for i in [0, 1]]

# ---------------------------------------------------------------- #
