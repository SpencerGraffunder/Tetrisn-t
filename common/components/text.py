import pygame
import os
import sys
from client.globals import *


# Example
# text.draw(screen, score_str1, 'SMALL', ((g.window_width) - (4 * TILE_SIZE), (BOARD_HEIGHT - 3) * TILE_SIZE), (0, 128, 0))


class Text:
    def __init__(self):
        self.fonts = None

    def load_fonts(self):
        if getattr(sys, 'frozen', False):
            wd = sys._MEIPASS
        else:
            wd = ''

        large_font_size = g.window_height // 5
        medium_font_size = g.window_height // 10
        small_font_size = g.window_height // 20

        self.fonts = {
            'LARGE': pygame.font.Font(os.path.join(wd, 'resources', 'munro-small.ttf'), large_font_size),
            'MEDIUM': pygame.font.Font(os.path.join(wd, 'resources', 'munro-small.ttf'), medium_font_size),
            'SMALL': pygame.font.Font(os.path.join(wd, 'resources', 'munro-small.ttf'), small_font_size)
        }

    def draw(self, screen, text_str, size, pos, color):
        the_text = self.fonts[size].render(text_str, True, color)
        text_rect = the_text.get_rect()
        text_rect.center = pos
        screen.blit(the_text, text_rect)


text = Text()
