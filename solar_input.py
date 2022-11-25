# coding: utf-8
# license: GPLv3
import numpy as np
import matplotlib.pyplot as plt
from solar_objects import Star, Planet, DrawableObject

def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename, 'r') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем

            object_type = line.split()[0].lower()
            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object")

    return [DrawableObject(obj) for obj in objects]


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.
    Входная строка должна иметь слеюущий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.
    Пример строки:
    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание звезды.
    **star** — объект звезды.
    """
    line = line.lower().split()
    star.R = float(line[1])
    star.color = line[2]
    star.m = float(line[3])
    star.x = float(line[4])
    star.y = float(line[5])
    star.Vx = float(line[6])
    star.Vy = float(line[7])

def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Предполагается такая строка:
    Входная строка должна иметь слеюущий формат:
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
    Пример строки:
    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.
    **planet** — объект планеты.
    """

    line = line.lower().split()
    planet.R = float(line[1])
    planet.color = line[2]
    planet.m = float(line[3])
    planet.x = float(line[4])
    planet.y = float(line[5])
    planet.Vx = float(line[6])
    planet.Vy = float(line[7])

def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            if obj.obj.type == "star":
                out_file.write(" ".join(("Star", str(obj.obj.R), obj.obj.color, str(obj.obj.m), str(obj.obj.x), str(obj.obj.y), str(obj.obj.Vx), str(obj.obj.Vy))) + '\n')
            elif obj.obj.type == "planet":
                out_file.write(" ".join(("Planet", str(obj.obj.R), obj.obj.color, str(obj.obj.m), str(obj.obj.x), str(obj.obj.y), str(obj.obj.Vx), str(obj.obj.Vy))) + '\n')

def build_graphics(object_list):
    """Строит график <величина>/время, на вход список пар время-<величина>."""
    out_filename = "graphics.jpg"
    
    if len(object_list.list) == 0:
        print("No measurements")
        return
    
    plt.figure(figsize=(20, 10))
    
    time = [el[0] for el in object_list.list]
    distance = [el[1] for el in object_list.list]
    speed = [el[2] for el in object_list.list]
    a = [el[3] for el in object_list.list]
    
    plt.subplot(221)
    plt.xlabel("Время")
    plt.ylabel("Скорость")
    plt.xlim(0, 1.2*max(time))
    plt.ylim(0, 1.2*max(speed))
    plt.plot(time, speed)
    plt.subplot(222)
    plt.xlabel("Время")
    plt.ylabel("Расстояние")
    plt.xlim(0, 1.2*max(time))
    plt.ylim(0, 1.2*max(distance))
    plt.plot(time, distance)
    plt.subplot(223)
    plt.xlabel("Расстояние")
    plt.ylabel("Скорость")
    plt.xlim(0, 1.2*max(distance))
    plt.ylim(0, 1.2*max(speed))
    plt.plot(distance, speed)
    plt.subplot(224)
    plt.xlabel("Время")
    plt.ylabel("Большая полуось")
    plt.xlim(0, 1.2*max(time))
    plt.ylim(1.2*min(0, min(a)), 1.2*max(a))
    plt.plot(time, a)
    plt.savefig('graphics.jpg')

if __name__ == "__main__":
    print("This module is not for direct call!")
