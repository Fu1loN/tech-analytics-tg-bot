from PIL import Image, ImageDraw


from graphic import Graphic
from random import randint
from math import ceil


class PIL_drawer:
    def __init__(self, *args):
        self.graphs = []
        for i in args:
            self.add(i)
        self.mn_y = 10 ** 9
        self.mx_y = -10 ** 9
        self.colors = []
        self.offset_level = 0

    def update_min(self):
        new_max_y = -100000
        new_min_y = 100000
        for i in self.graphs:
            if isinstance(i, Graphic):
                if i.min_positive:
                    new_min_y = min(new_min_y, min(i))
                    new_max_y = max(new_max_y, max(i))
        self.mn_y = self.mn_y - (new_max_y - new_min_y)
        self.offset_level = new_min_y

    def add(self, item, color=None):
        self.graphs.append(item)
        if color is None:
            self.colors.append((randint(1, 255), randint(1, 255), randint(1, 255)))
        else:
            self.colors.append(color)
        if isinstance(item, Graphic):
            if not item.min_positive:
                self.mx_y = max(self.mx_y, max(item))
                self.mn_y = min(self.mn_y, min(item))
        else:
            for i in item:
                self.mx_y = max(self.mx_y, max(i))
                self.mn_y = min(self.mn_y, min(i))

    def draw(self, filename):
        screen_width, screen_height = 1920, 1080
        top_offset =  100
        bottom_offset = 0
        image = Image.new("RGB", (screen_width, screen_height), "black")
        self.update_min()
        max_y, min_y = self.mx_y, self.mn_y
        scale = (screen_height - top_offset - bottom_offset) / (self.mx_y - self.mn_y)
        draw = ImageDraw.Draw(image)
        for graphic, color in zip(self.graphs, self.colors):
            if isinstance(graphic, Graphic):
                for i in range(1, len(graphic)):
                    width = screen_width // len(graphic)
                    sides_offset = screen_width % len(graphic) // 2
                    if graphic.min_positive:
                        start = (i * width + sides_offset + width // 2,
                                 screen_height -(graphic[i] - self.offset_level) * scale - bottom_offset)
                        end = ((i - 1) * width + sides_offset + width // 2,
                               screen_height - (graphic[i - 1] - self.offset_level) * scale - bottom_offset)
                        # pygame.draw.line(screen, color, start, end)
                        draw.line((*start, *end), fill=color, width=1)
                    else:
                        # pygame.draw.line(screen, color,
                        #                  (i * width + sides_offset + width // 2,
                        #                   screen_height - (graphic[i] - min_y) * scale - top_offset),
                        #                  ((i - 1) * width + sides_offset + width // 2,
                        #                   screen_height - (graphic[i - 1] - min_y) * scale - top_offset))
                        draw.line((i * width + sides_offset + width // 2,
                                   screen_height - (graphic[i] - min_y) * scale - bottom_offset,
                                   (i - 1) * width + sides_offset + width // 2,
                                   screen_height - (graphic[i - 1] - min_y) * scale - bottom_offset), fill=color, width=1)
            else:
                closes, highs, lows, opens = graphic
                width = screen_width // len(opens)
                # print(width)
                sides_offset = screen_width % len(opens) // 2
                color_line = (200, 200, 200)
                color_up = (0, 200, 0)
                color_down = (200, 0, 0)
                for i in range(len(opens)):
                    candle_width = width - 2
                    candle_height = abs(closes[i] - opens[i]) * scale
                    candle_x = i * width + sides_offset
                    if opens[i] < closes[i]:
                        candle_y = screen_height - (min(opens[i], closes[i]) - min_y) * scale - bottom_offset
                        draw.rectangle((candle_x + 1, candle_y, candle_width + candle_x, candle_y - candle_height),
                                       fill=color_up)
                        draw.line((candle_x + ceil(width / 2), candle_y - candle_height,
                                   candle_x + ceil(width / 2),
                                   screen_height - (highs[i] - min_y) * scale - bottom_offset), fill=color_line)
                        draw.line((candle_x + ceil(width / 2), candle_y,
                                   candle_x + ceil(width / 2),
                                   screen_height - (lows[i] - min_y) * scale - bottom_offset), fill=color_line)
                    else:
                        candle_y = screen_height - (max(opens[i], closes[i]) - min_y) * scale - bottom_offset
                        draw.rectangle((candle_x + 1, candle_y, candle_width + candle_x, candle_y + candle_height),
                                       fill=color_down)
                        draw.line((candle_x + ceil(width / 2), candle_y,
                                   candle_x + ceil(width / 2),
                                   screen_height - (highs[i] - min_y) * scale - bottom_offset), fill=color_line)
                        draw.line((candle_x + ceil(width / 2), candle_y + candle_height,
                                   candle_x + ceil(width / 2),
                                   screen_height - (lows[i] - min_y) * scale - bottom_offset), fill=color_line)
        # image.show()
        image.save(filename)
if __name__ == "__main__":
    # Создаём новое изображение (RGB, размер 500x500, белый фон)
    width, height = 500, 500
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Рисуем линию (от (50, 50) до (450, 50), цвет красный, толщина 5)
    draw.line((50, 50, 450, 50), fill="red", width=5)

    # Рисуем прямоугольник (границы от (100, 100) до (400, 300), цвет синий, толщина 3)
    draw.rectangle((100, 100, 400, 300), outline="blue", width=3)

    # Рисуем закрашенный прямоугольник (границы от (150, 150) до (350, 250), цвет зелёный)
    draw.rectangle((150, 150, 350, 250), fill="green")

    # Сохраняем изображение
    image.save("drawing_example.png")

    # Показываем изображение (опционально)
    image.show()