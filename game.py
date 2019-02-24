# coding=utf-8
import saving
import threading
import tkinter
import random
import time
from typing import Any, Dict, Union


def run_game(tail=[]):
    time.sleep(0.1 - snake['l'] / 2250)
    last_data(snake, tail)
    while snake['status'] == 'sleeping' or stop['text'] == '⬤':
        pass
    if snake['game'] == 'false':
        snake['game'] = 'true'
        run_game([])
    tail = go_to(1, tail)
    xyz = snake_side()
    tail = edit_tail(tail)
    snake['y'] = (snake['y'] + xyz[1]) % 15
    snake['x'] = (snake['x'] + xyz[0]) % 15
    end_game()
    if snake['status'] == 'dead':
        snake['status'] = 'sleeping'
        while snake['status'] == 'sleeping':
            pass
        run_game([])
    go_to(0, tail)
    run_game(tail)


def go_to(value, tail=None):
    if value == 1:
        if snake['l'] > len(tail):
            xyz = snake_side()
            tail += [dict(x=snake['x'] - xyz[0], y=snake['y'] - xyz[1])]
        if not tail:
            map[snake['y'] * 15 + snake['x']]['bg'] = 'green'
        else:
            map[tail[len(tail) - 1]['y'] * 15 + tail[len(tail) - 1]['x']]['bg'] = 'green'

    if value == 0:
        food = False
        if map[snake['y'] * 15 + snake['x']]['bg'] == 'red':
            food = True
            snake['l'] += 1
            snake['food'] = False
            tail = go_to(1, tail)
        map[snake['y'] * 15 + snake['x']]['bg'] = 'black'
        for coordinate in tail:
            map[coordinate['y'] * 15 + coordinate['x']]['bg'] = 'black'
        if food:
            throw_food()

    if value != 1 and value != 0:
        snake['way'] = value

    return tail


def end_game():
    if map[snake['y'] * 15 + snake['x']]['bg'] == 'black':
        snake['status'] = 'dead'


def snake_side():
    if snake['way'] == 'left':
        return [-1, 0]
    elif snake['way'] == 'right':
        return [1, 0]
    elif snake['way'] == 'up':
        return [0, -1]
    elif snake['way'] == 'down':
        return [0, 1]


def pause():
    if stop['text'] == '◯':
        stop['text'] = '⬤'
    else:
        stop['text'] = '◯'


def throw_food():
    coords = []
    for i in range(225):
        if map[i]['bg'] == 'green':
            coords += [str(i % 15) + ' ' + str(i // 15)]
    x, y = coords[random.randint(0, len(coords) - 1)].split(' ')
    x, y = int(x), int(y)
    map[y * 15 + x]['bg'] = 'red'
    snake['food'] = True
    score_button['text'] = 'Score: ' + saving.save_score(snake['l'])
    point_button['text'] = 'Points: ' + str(snake['l'])


def edit_tail(tail):
    if len(tail) > 0:
        for index in range(len(tail) - 1):
            tail[len(tail) - index - 1] = tail[len(tail) - index - 2]
        tail[0] = dict(x=snake['x'], y=snake['y'])
    return tail


def game_start():
    update_map()
    throw_food()


def update_map():
    for label in map:
        label['bg'] = 'green'
    global snake
    snake = dict(x=7, y=7, l=0, way='left', status='live', game='false', task='none')
    map[snake['y'] * 15 + snake['x']]['bg'] = 'black'


def last_data(csr, tail):
    if csr['task'] == 0:
        snake['task'] = None
        saving.save(snake, tail)
    if csr['task'] == 1:
        snake['task'] = None
        csr, tail = saving.update()
        for label in map:
            label['bg'] = 'green'
        map[csr['y'] * 15 + csr['x']] = 'black'
        for i in tail:
            map[i['y'] * 15 + i['x']] = 'black'
    if csr['task'] == 2:
        snake['task'] = None
        saving.nullify_score()

    snake['x'] = csr['x']
    snake['y'] = csr['y']
    snake['l'] = csr['l']
    snake['way'] = csr['way']
    snake['status'] = csr['status']
    snake['game'] = csr['game']


def expection(value):
    snake['task'] = value


global snake
snake = dict(x=7, y=7, l=0, food=False, way='left', status='sleeping', game=False, task=None)
map = []

game = tkinter.Tk()
game.title('Snake')
game.geometry('450x610')
game.resizable(0, 0)

for i in range(225):
    map += [tkinter.Label(game, bg='green', height=2, width=4, borderwidth=0, relief='groove')]
    map[i].grid(row=i // 15, column=i % 15)

tkinter.Label(game, height=2, borderwidth=0).grid(row=15, column=0, columnspan=15)

start_button = tkinter.Button(game, bg='gray', width=10, text='New game!', command=game_start)
start_button.grid(row=16, column=0, columnspan=3)
continue_button = tkinter.Button(game, bg='gray', width=10, text='Continue', command=lambda: expection(1))
continue_button.grid(row=17, column=0, columnspan=3)
save_button = tkinter.Button(game, bg='gray', width=10, text='Save game', command=lambda: expection(0))
save_button.grid(row=18, column=0, columnspan=3)

score_button = tkinter.Button(game, bg='gray', width=10, text='Score:')
score_button.grid(row=16, column=12, columnspan=3)
point_button = tkinter.Button(game, bg='gray', width=10, text='Points:')
point_button.grid(row=17, column=12, columnspan=3)
nullify_button = tkinter.Button(game, bg='gray', width=10, text='Nullify score', command=lambda: expection(2))
nullify_button.grid(row=18, column=12, columnspan=3)

go_left = tkinter.Button(game, bg='gray', width=3, text='⮜', borderwidth=1, command=lambda: go_to('left'))
go_left.grid(row=17, column=6)
go_right = tkinter.Button(game, bg='gray', width=3, text='⮞', borderwidth=1, command=lambda: go_to('right'))
go_right.grid(row=17, column=8)
go_up = tkinter.Button(game, bg='gray', width=3, text='⮝', borderwidth=1, command=lambda: go_to('up'))
go_up.grid(row=16, column=7)
go_down = tkinter.Button(game, bg='gray', width=3, text='⮟', borderwidth=1, command=lambda: go_to('down'))
go_down.grid(row=18, column=7)

game.bind('<Key-Left>', lambda e: go_to('left'))
game.bind('<Key-Right>', lambda e: go_to('right'))
game.bind('<Key-Up>', lambda e: go_to('up'))
game.bind('<Key-Down>', lambda e: go_to('down'))


stop = tkinter.Button(game, bg='gray', width=3, text='◯', borderwidth=1, command=pause)
stop.grid(row=17, column=7)

map[snake['y'] * 15 + snake['x']]['bg'] = 'black'
threading.Thread(target=run_game).start()

game.mainloop()
