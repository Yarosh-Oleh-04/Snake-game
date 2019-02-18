# coding=utf-8
import threading
import tkinter
import random
import time
from typing import Any


def run_game(tail=[]):
    time.sleep(0.5 - snake['l'] / 500)
    while snake['way'] == '' or stop['text'] == '⬤':
        pass
    tail = go_to(1, tail)
    xyz = snake_side()
    tail = edit_tail(tail)
    snake['y'] = (snake['y'] + xyz[1]) % 15
    snake['x'] = (snake['x'] + xyz[0]) % 15

    go_to(0, tail)
    score_button['text'] = 'Score: ' + str(snake['l'])
    run_game(tail)


def go_to(value, tail=None):
    if value == 1:
        if snake['l'] > len(tail):
            xyz = snake_side()
            tail += [dict(x=snake['x'] - xyz[0], y=snake['y'] - xyz[1])]
        map[snake['y'] * 15 + snake['x']]['bg'] = 'green'
        for coordinate in tail:
            map[(coordinate['y'] * 15 + coordinate['x'])]['bg'] = 'green'

    if value == 0:
        if map[snake['y'] * 15 + snake['x']]['bg'] == 'red':
            snake['l'] += 1
            snake['food'] = False
        map[snake['y'] * 15 + snake['x']]['bg'] = 'black'
        for coordinate in tail:
            map[(coordinate['y'] * 15 + coordinate['x'])]['bg'] = 'black'
        throw_food()

    if value != 1 and value != 0:
        snake['way'] = value

    return tail


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
    if not snake['food']:
        coords = []
        for i in range(len(map)):
            if map[i]['bg'] == 'green':
                coords += [str(i // 15) + ' ' + str(i % 15)]
        x, y = coords[random.randint(0, len(coords) - 1)].split(' ')
        x, y = int(x), int(y)
        map[y * 15 + x]['bg'] = 'red'
        snake['food'] = True


def edit_tail(tail):
    if len(tail) > 0:
        for index in range(len(tail) - 1):
            tail[len(tail) - index - 1] = tail[len(tail) - index - 2]
        tail[0] = dict(x=snake['x'], y=snake['y'])
    return tail


def game_start():
    snake['way'] = 'left'
    throw_food()


global snake
snake = dict(x=7, y=7, l=0, food=False, way='')
map = []

game = tkinter.Tk()
game.title('Snake')
game.geometry('450x610')
game.resizable(0, 0)

for i in range(225):
    map += [tkinter.Label(game, bg='green', height=2, width=4, borderwidth=0, relief='groove')]
    map[i].grid(row=i // 15, column=i % 15)


tkinter.Label(game, height=2, borderwidth=0).grid(row=15, column=0, columnspan=15)

start_button = tkinter.Button(game, bg='gray', text='New game!', command=game_start)
start_button.grid(row=16, column=0, columnspan=3, rowspan=3)
score_button = tkinter.Button(game, bg='gray', text='Score:')
score_button.grid(row=16, column=11, columnspan=3, rowspan=3)

go_left = tkinter.Button(game, bg='gray', width=3, text='⮜', borderwidth=1, command=lambda: go_to('left'))
go_left.grid(row=17, column=6)
go_right = tkinter.Button(game, bg='gray', width=3, text='⮞', borderwidth=1, command=lambda: go_to('right'))
go_right.grid(row=17, column=8)
go_up = tkinter.Button(game, bg='gray', width=3, text='⮝', borderwidth=1, command=lambda: go_to('up'))
go_up.grid(row=16, column=7)
go_down = tkinter.Button(game, bg='gray', width=3, text='⮟', borderwidth=1, command=lambda: go_to('down'))
go_down.grid(row=18, column=7)

stop = tkinter.Button(game, bg='gray', width=3, text='◯', borderwidth=1, command=pause)
stop.grid(row=17, column=7)

map[snake['y'] * 15 + snake['x']]['bg'] = 'black'
threading.Thread(target=run_game).start()

game.mainloop()
