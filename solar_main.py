# coding: utf-8
# license: GPLv3

import pygame
from solar_vis import *
from solar_model import *
from solar_input import *
from solar_objects import *
import thorpy
import time
import numpy as np

timer = None
back_flag = None
in_filename = "one_satellite.txt"

alive = True

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

model_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

time_scale = 10000.0
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""

object_list = ObjectList()

FPS = 120

def execution(delta):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global model_time
    global displayed_time
    for i in range(1000):
        recalculate_space_objects_positions([dr.obj for dr in space_objects], delta / 1000)
        model_time += delta / 1000


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True

def pause_execution():
    global perform_execution
    perform_execution = False

def open_file():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global perform_execution
    global space_objects
    global browser
    global model_time
    global in_filename
    global object_list

    model_time = 0.0
    perform_execution = False
    space_objects = read_space_objects_data_from_file(in_filename)
    if in_filename == "one_satellite.txt":
        object_list = ObjectList(space_objects[1].obj.type)
    max_distance = max([max(abs(obj.obj.x), abs(obj.obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)

def write_file():
    global space_objects
    global browser
    global model_time
    
    pause_execution()
    out_filename = "stats.txt"
    write_space_objects_data_to_file(out_filename, space_objects)

def handle_events(events, menu):
    global alive
    for event in events:
        menu.react(event)
        if event.type == pygame.QUIT:
            alive = False

def slider_to_real(val):
    return 10e5 * val

def slider_reaction(event):
    global time_scale
    time_scale = slider_to_real(event.el.get_value())

def start_building_graphics():
	pause_execution()
	build_graphics(object_list)

def init_ui(screen):
    global browser
    slider = thorpy.SliderX(150, (0, 10), "Speed")
    slider.user_func = slider_reaction
    button_play = thorpy.make_button("Play", func=start_execution)
    button_pause = thorpy.make_button("Pause", func=pause_execution)
    timer = thorpy.make_text("nnnnnnn seconds passed")
    empty_space = thorpy.make_text("\n\n")
    button_load = thorpy.make_button(text="Load a file", func=open_file)
    button_write = thorpy.make_button(text="Write a file", func=write_file)
    button_graphics = thorpy.make_button(text="Build graphics", func=start_building_graphics)

    box_slider = thorpy.Box(elements=[
        slider,
        empty_space,
        button_graphics,
        timer])
    reaction_slider = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=slider_reaction,
                                event_args={"id":thorpy.constants.EVENT_SLIDE},
                                params={},
                                reac_name="slider reaction")
    box_slider.add_reaction(reaction_slider)
    box_control = thorpy.Box(elements=[
        button_play,
        button_pause])
    box_file = thorpy.Box(elements=[
        button_load,
        button_write])
    box = thorpy.Box(elements=[
        box_slider,
        box_control,
        box_file])
    box_slider.set_topleft((0, 0))
    box_control.set_topleft((40, 30))
    box_file.set_topleft((120, 30))
    
    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen
    return menu, box_slider, box_control, box_file, timer

def main():
    global perform_execution
    global timer
    global back_flag
    global in_filename
    global model_time
    global object_list

    print('Modelling started!')
    physical_time = 0

    pygame.init()
    
    screen = pygame.display.set_mode((window_width, window_height))
    drawer = Drawer(screen)
    menu, box_slider, box_control, box_file, timer = init_ui(screen)
    perform_execution = False
    clock = pygame.time.Clock()
    cur_time = time.perf_counter()
    
    while alive:
        clock.tick(FPS)
        handle_events(pygame.event.get(), menu)
        last_time = cur_time
        cur_time = time.perf_counter()
        timer_text = "%d seconds passed" % (int(model_time))
        timer.set_text(timer_text)
        if perform_execution:
            execution((cur_time - last_time) * time_scale)
            if in_filename == "one_satellite.txt" and len(space_objects) > 0:
                distance = np.sqrt((space_objects[0].obj.x-space_objects[1].obj.x)**2 + (space_objects[0].obj.y-space_objects[1].obj.y)**2)
                speed = np.sqrt((space_objects[1].obj.Vx)**2 + (space_objects[1].obj.Vy)**2)
                a = 1 / (2/distance - speed**2/(gravitational_constant*space_objects[0].obj.m))
                object_list.update_list(model_time, distance, speed, a)
        drawer.update(space_objects, box_slider, box_control, box_file)

    print('Modelling finished!')

if __name__ == "__main__":
    main()
