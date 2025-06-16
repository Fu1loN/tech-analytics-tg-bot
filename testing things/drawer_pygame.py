import pygame
import sys
from random import randint
from graphic import Graphic, MACD, oper_MACD, read_all_data, find_optimal_EMA, EMA, Zero
from math import ceil
from graphic import Graphic
pygame.init()
top_offset = 100
bottom_offset = 100
offset_level = 0
screen_width, screen_height = size = 1920, 1080

class Graph_drawer:

    def __init__(self, screen=None):
        self.graphs = []
        self.mn_y = 10**8
        self.mx_y = -10**8
        self.colors = []
        self.offset_level = 0
        self.screen = screen
    def add(self, item, color=None):
        self.graphs.append(item)
        if color is None:
            self.colors.append((randint(1, 255),randint(1, 255),randint(1, 255)))
        else:
            self.colors.append(color)
        if isinstance(item,Graphic):
            if not item.min_positive:
                self.mx_y = max(self.mx_y, max(item))
                self.mn_y = min(self.mn_y, min(item))
        else:
            for i in item:
                self.mx_y = max(self.mx_y, max(i))
                self.mn_y = min(self.mn_y, min(i))
    def update_min(self):
        new_max_y = -100000
        new_min_y = 100000
        for i in self.graphs:
            if isinstance(i, Graphic):
                if i.min_positive:
                    new_min_y= min(new_min_y, min(i))
                    new_max_y = max(new_max_y, max(i))
        self.mn_y = self.mn_y - (new_max_y - new_min_y)
        self.offset_level =  (new_max_y - new_min_y)
    def run(self, text):
        if self.screen is None:
            screen = pygame.display.set_mode((screen_width, screen_height))
        else:
            screen = self.screen
        clock = pygame.time.Clock()
        running = True
        self.update_min()
        global max_y, min_y, offset_level
        min_y = self.mn_y
        max_y = self.mx_y
        offset_level = self.offset_level
        font = pygame.font.Font(None, 36)
        screen.fill((0, 0, 0))
        for i in range(len(text)):
            sur = font.render(text[i][0], True, (200, 0, 0) if not text[i][1] else (0,200, 0))
            screen.blit(sur, (0, i * 20))
        for i, color in zip(self.graphs, self.colors):
            if isinstance(i, Graphic):
                draw_graphic(screen, i, color)
            else:
                assert len(i) == 4
                draw_candles(screen, *i)
        # draw_graphic(screen, highs, min_y, max_y)
        pygame.display.flip()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    # print(event.pos)

                    screen.fill((0, 0, 0))
                    for i in range(len(text)):
                        sur = font.render(text[i][0], True, (200, 0, 0) if not text[i][1] else (0,200, 0))
                        screen.blit(sur, (0, i * 20))
                    draw_lines_to_cursor(screen, event.pos)
                    for i, color in zip(self.graphs, self.colors):
                        if isinstance(i, Graphic):
                            draw_graphic(screen, i, color)
                        else:
                            assert len(i) == 4
                            draw_candles(screen, *i)
                    pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

            clock.tick(30)
            break
        return screen
def draw_lines_to_cursor(screen, pos, color=(200, 200, 200)):
    start = (pos[0], 0)
    pygame.draw.line(screen, color, start, pos)
def draw_graphic(screen, graphic : Graphic, color=(255, 255, 255)):
    scale = (screen_height - top_offset - bottom_offset) / (max_y - min_y)
    width = screen_width // len(graphic)
    sides_offset = screen_width % len(graphic) // 2
    for i in range(1, len(graphic)):

        if graphic.min_positive:
            start = (i * width + sides_offset + width // 2,
                          (max_y - min_y -  graphic[i]) * scale + top_offset)
            end = ((i - 1) * width + sides_offset + width // 2,
                          (max_y - min_y -  graphic[i - 1]) * scale + top_offset)
            pygame.draw.line(screen, color, start, end)


        else:
            pygame.draw.line(screen, color,
                         (i * width + sides_offset + width // 2,
                          screen_height - (graphic[i] - min_y) * scale - top_offset),
                         ((i - 1) * width + sides_offset + width // 2,
                          screen_height - (graphic[i - 1] - min_y) * scale - top_offset))


def draw_candles(screen, closes, highs, lows, opens, color_up=(0, 255, 0), color_down=(255, 0, 0),
                 color_line=(200, 200, 200)):
    # print(min_y, max_y)
    width = screen_width // len(opens)
    # print(width)
    sides_offset = screen_width % len(opens) // 2
    scale = (screen_height - top_offset - bottom_offset) / (max_y - min_y)
    for i in range(len(opens)):
        candle_width = width - 2
        candle_height = abs(closes[i] - opens[i]) * scale
        candle_x = i * width + sides_offset
        candle_y = screen_height - (max(opens[i], closes[i]) - min_y) * scale - top_offset

        pygame.draw.line(screen, color_line, (
            candle_x + ceil(width / 2), candle_y), (
                             candle_x + ceil(width / 2),
                             screen_height - (highs[i] - min_y) * scale - top_offset))
        pygame.draw.line(screen, color_line, (
            candle_x + ceil(width / 2), candle_y + candle_height), (
                             candle_x + ceil(width / 2),
                             screen_height - (lows[i] - min_y) * scale - top_offset))

        if opens[i] < closes[i]:
            pygame.draw.rect(screen, color_up, (candle_x + 1, candle_y, candle_width, candle_height))
        else:
            pygame.draw.rect(screen, color_down, (candle_x + 1, candle_y, candle_width, candle_height))




max_y = min_y = 0


def main():
    closes_main, highs, lows, opens = read_all_data("../data/apple/AAPL_historical_data.csv")
    screen = None
    for i in range(10, len(closes_main)):
        closes = closes_main[:i]
        drawer = Graph_drawer(screen)
        drawer.add([closes, highs[:i], lows[:i], opens[:i]])
        zero = Zero(len(closes))
        ft, sc = find_optimal_EMA(closes)
        macd = MACD(sc, ft)
        MACD_oper = oper_MACD(macd, EMA, 48)
        text = []
        for i in ft, sc, MACD_oper:
            text.append((f"{i} stonks {i.stonks} with chance {i.reliability}", i.stonks))
        if macd.line[-1] > 0:
            text.append((f"{macd} stonks", True))
        else:
            text.append((f"{macd} not stonks", False))
        for i in ft, sc, MACD_oper, macd:
            if i.signal:
                text.append((f"{i} signal!!!!!", True))

        # print()

        drawer.add(zero, (100, 100, 200))
        drawer.add(ft)
        drawer.add(sc)

        drawer.add(macd, (159, 129, 112))
        drawer.add(MACD_oper, (150, 10, 150))

        screen = drawer.run(text)


if __name__ == "__main__":
    main()
