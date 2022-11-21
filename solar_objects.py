# coding: utf-8
# license: GPLv3
import pygame
from solar_vis import *

class Star:
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """

    type = "star"
    """Признак объекта звезды"""

    m = 1
    """Масса звезды"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    Vx = 0
    """Скорость по оси **x**"""

    Vy = 0
    """Скорость по оси **y**"""

    Fx = 0
    """Сила по оси **x**"""

    Fy = 0
    """Сила по оси **y**"""

    R = 5
    """Радиус звезды"""

    color = "red"
    """Цвет звезды"""


class Planet:
    """Тип данных, описывающий планету.
    Содержит массу, координаты, скорость планеты,
    а также визуальный радиус планеты в пикселах и её цвет
    """

    type = "planet"
    """Признак объекта планеты"""

    m = 1
    """Масса планеты"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    Vx = 0
    """Скорость по оси **x**"""

    Vy = 0
    """Скорость по оси **y**"""

    Fx = 0
    """Сила по оси **x**"""

    Fy = 0
    """Сила по оси **y**"""

    R = 5
    """Радиус планеты"""

    color = "green"
    """Цвет планеты"""

class Drawer:
    def __init__(self, screen):
        self.screen = screen


    def update(self, figures, box_slider, box_control, box_file):
        self.screen.fill((0, 0, 0))
        for figure in figures:
            figure.draw(self.screen)
        
        box_slider.blit()
        box_control.blit()
        box_file.blit()
        box_slider.update()
        box_control.update()
        box_file.update()
        pygame.display.update()


class DrawableObject:
    def __init__(self, obj):
        self.obj = obj

    def draw(self, surface):
        pygame.draw.circle(surface, self.obj.color, (scale_x(self.obj.x), scale_y(self.obj.y)), self.obj.R)

class ObjectList:
    def __init__(self, name=None):
        self.name = name
        self.list = []
	
    def update_list(self, time, distance, speed, a):
        self.list.append((time, distance, speed, a))

