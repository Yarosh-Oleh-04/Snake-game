import saving
import threading
import tkinter
import random
import time


def run_game():
    while True:
        while brain['status'] == 'pause':
            pass
        if brain['status'] == 'dead':
            return 0
        new_tail()
        go_to()
        while brain['status'] == 'pause':
            pass
        if brain['status'] == 'dead':
            return 0
        end_moving()
        new_tail()
        edit_tail()
        if end_game() == 'dead':
            end_game_options()
        if brain['tail']:
            brain['tail'][0]['tail'].destroy()
            brain['tail'] = brain['tail'][1:]
        while brain['status'] == 'pause':
            pass
        if brain['status'] == 'dead':
            return 0


def go_to():
    xyz = snake_side(brain['way'])
    for i in range(30):
        x = brain['x'] * 30
        y = brain['y'] * 30
        time.sleep(0.005 - brain['l'] / 65000)
        brain['snake'].place(x=x+xyz[0]*i, y=y+xyz[1]*i)
        last_tail()
    if brain['task'] == 0:
        brain['tail'][0]['tail'].destroy()
        brain['tail'] = brain['tail'][1:]
        brain['task'] = None
    brain['x'] += xyz[0]
    brain['y'] += xyz[1]


def end_moving():
    xyz = snake_side(brain['way'])
    if brain['x'] + xyz[0] < 0 or brain['x'] + xyz[0] > 14 or brain['y'] + xyz[1] < 0 or brain['y'] + xyz[1] > 14:
        edit_tail()
        brain['task'] = 0
    if brain['x'] + xyz[0] < 0:
        brain['x'] = 15
    elif brain['x'] + xyz[0] > 14:
        brain['x'] = -1
    elif brain['y'] + xyz[1] < 0:
        brain['y'] = 15
    elif brain['y'] + xyz[1] > 14:
        brain['y'] = -1


def snake_side(value):
    if value == 'left':
        return [-1, 0]
    elif value == 'right':
        return [1, 0]
    elif value == 'up':
        return [0, -1]
    elif value == 'down':
        return [0, 1]


def pause():
    if stop['text'] == '⬜':
        stop['text'] = '⬛'
        brain['status'] = 'pause'
    else:
        stop['text'] = '⬜'
        brain['status'] = 'live'


def throw_food():
    cords = []
    for i in range(225):
        n = 0
        x = i // 15 * 30
        y = i % 15 * 30
        if brain['tail']:
            for tail in brain['tail']:
                if tail['x'] == x and tail['y'] == y:
                    n += 1
        if brain['x'] == x and brain['y'] == y:
            n += 1
        if n == 0:
            cords += [[x, y]]
    k = cords[random.randint(0, len(cords) - 1)]
    food = tkinter.Frame(game_cell, bg='red', width=30, height=30)
    food.place(x=k[0], y=k[1])
    brain['food'] = [dict(x=k[0], y=k[1]), food]


def new_tail():
    xyz = snake_side(brain['way'])
    if brain['x'] + xyz[0] == brain['food'][0]['x'] / 30 and brain['y'] + xyz[1] == brain['food'][0]['y'] / 30:
        score['text'] = 'Score: ' + '000'[len(str(brain['l'])):] + str(brain['l'])
        brain['l'] += 1
        brain['food'][1].destroy()
        edit_tail()
        throw_food()
        for i in range(30):
            x = brain['x'] * 30
            y = brain['y'] * 30
            time.sleep(0.005 - brain['l'] / 65000)
            brain['snake'].place(x=x + xyz[0] * i, y=y + xyz[1] * i)
        brain['x'] += xyz[0]
        brain['y'] += xyz[1]


def last_tail():
    if brain['tail']:
        xyz = snake_side(brain['tail'][0]['way'])
        x = brain['tail'][0]['x']
        y = brain['tail'][0]['y']
        brain['tail'][0]['tail'].place(x=x+xyz[0], y=y+xyz[1])
        brain['tail'][0]['x'] += xyz[0]
        brain['tail'][0]['y'] += xyz[1]


def edit_tail():
    tail = tkinter.Frame(game_cell, bg='black', width=30, height=30)
    tail.place(x=brain['x']*30, y=brain['y']*30)
    brain['tail'] += [dict(tail=tail, x=brain['x'] * 30, y=brain['y'] * 30, way=brain['way'])]


def end_game():
    xyz = snake_side(brain['way'])
    for tail in brain['tail']:
        if tail['x'] / 30 == brain['x'] + xyz[0] and tail['y'] / 30 == brain['y'] + xyz[1]:
            return 'dead'


def game_start():
    global brain
    brain = dict(x=7, y=7, l=1, snake=None, tail=[], food=None, way='left', status='sleeping', task=None)
    brain['snake'] = tkinter.Frame(game_cell, bg='black', width=30, height=30)
    brain['snake'].place(x=brain['x'] * 30, y=brain['y'] * 30)
    stop['text'] = '⬜'
    score['text'] = 'Score: 000'
    throw_food()
    edit_tail()
    threading.Thread(target=run_game).start()


def game_continuation():
    global brain
    brain = saving.update()
    brain['snake'] = tkinter.Frame(game_cell, bg='black', width=30, height=30)
    brain['snake'].place(x=brain['x'] * 30, y=brain['y'] * 30)
    for tail in brain['tail']:
        tail['tail'] = tkinter.Frame(game_cell, bg='black', width=30, height=30)
        tail['tail'].place(x=tail['x'], y=tail['y'])
    stop['text'] = '⬛'
    score['text'] = 'Score: 000'
    end_moving()
    food = tkinter.Frame(game_cell, bg='red', width=30, height=30)
    food.place(x=brain['food'][0]['x'], y=brain['food'][0]['y'])
    brain['food'][1] = food
    edit_tail()
    threading.Thread(target=run_game).start()


def new_way(way):
    if brain['tail'][len(brain['tail']) - 1]['way'] == 'up' and way == 'down':
        pass
    elif brain['tail'][len(brain['tail']) - 1]['way'] == 'down' and way == 'up':
        pass
    elif brain['tail'][len(brain['tail']) - 1]['way'] == 'left' and way == 'right':
        pass
    elif brain['tail'][len(brain['tail']) - 1]['way'] == 'right' and way == 'left':
        pass
    else:
        brain['way'] = way


def last_data():
    pass


def update_game():
    brain['status'] = 'dead'
    time.sleep(1)
    for tail in brain['tail']:
        tail['tail'].destroy()
    brain['snake'].destroy()
    brain['food'][1].destroy()


def expection(value, options):
    if value == 1:
        update_game()
        game_continuation()
    if value == 2:
        update_game()
        game_start()
    if value == 3:
        saving.save(brain)
    if value == 4:
        pass
    if value == 5:
        pass
    option_destroy(options)


def end_game_options():

    def f():
        expection(2, end_options)
        end_options.destroy()

    def g():
        game_options()
        end_options.destroy()

    end_options = tkinter.Frame(game, height=500, width=450, bg='darkgreen')
    end_options.place(x=0, y=0)

    text = tkinter.Label(end_options, text='Game over!', bg='darkgreen')
    text.config(font=('', 30))
    text.place(x=130, y=125)

    new_game = tkinter.Button(end_options, text='New Game', bg='gray', activebackground='#005900')
    new_game['command'] = lambda: f()
    new_game.config(font=('', 30))
    new_game.place(x=120, y=200)

    menu = tkinter.Button(end_options, text='Menu', bg='gray', activebackground='#005900')
    menu['command'] = lambda: g()
    menu.config(font=('', 30))
    menu.place(x=170, y=300)


def game_options():
    time.sleep(0.1)
    options = tkinter.Frame(game, height=500, width=450, bg='darkgreen')
    options.place(x=0, y=0)

    close = tkinter.Button(options, text='⛌', bg='darkgreen', borderwidth=0, activebackground='#005900')
    close['command'] = lambda: option_destroy(options)
    close.config(font=('', 20))
    close.place(x=0, y=0)

    continue_the_game = tkinter.Button(options, text='Continue', bg='gray', activebackground='#005900')
    continue_the_game['command'] = lambda: expection(1, options)
    continue_the_game.config(font=('', 30))
    continue_the_game.place(x=145, y=35)

    new_game = tkinter.Button(options, text='New Game', bg='gray', activebackground='#005900')
    new_game['command'] = lambda: expection(2, options)
    new_game.config(font=('', 30))
    new_game.place(x=120, y=125)

    save_game = tkinter.Button(options, text='Save game', bg='gray', activebackground='#005900', pady=0)
    save_game['command'] = lambda: expection(3, options)
    save_game.config(font=('', 30))
    save_game.place(x=120, y=215)

    game_stats = tkinter.Button(options, text='Game stats', bg='gray', activebackground='#005900', pady=0)
    game_stats['command'] = lambda: expection(4, options)
    game_stats.config(font=('', 30))
    game_stats.place(x=120, y=305)

    about_us = tkinter.Button(options, text='About us', bg='gray', activebackground='#005900', pady=0)
    about_us['command'] = lambda: expection(5, options)
    about_us.config(font=('', 30))
    about_us.place(x=145, y=395)

    game.bind('<Escape>', lambda e: option_destroy(options))


def option_destroy(options):
    options.place(y=500)
    game.bind('<Escape>', lambda e: game_options())


game = tkinter.Tk()
game.title('Snake')
game.geometry('450x500')
game.resizable(0, 0)

gamepad = tkinter.Frame(game, bg='darkgreen', height=50, width=450)
gamepad.pack_propagate(0)
gamepad.pack()

menu = tkinter.Button(gamepad, text='☰', bg='darkgreen', borderwidth=0, activebackground='#005900',
                      command=lambda: game_options())
menu.config(font=('', 25))
menu.place(x=-5, y=-5)

stop = tkinter.Label(gamepad, text='⬜', bg='darkgreen')
stop.bind('<Button-1>', lambda e: pause())
stop.config(font=('', 25))
stop.place(x=50, y=3)

score = tkinter.Label(gamepad, text='Score: 000', bg='darkgreen')
score.config(font=('', 30))
score.place(x=250, y=0)

game_cell = tkinter.Frame(game, bg='green', height=450, width=450)
game_cell.pack_propagate(0)
game_cell.pack()

game.bind('<Key-Left>', lambda e: new_way('left'))
game.bind('<Key-Right>', lambda e: new_way('right'))
game.bind('<Key-Up>', lambda e: new_way('up'))
game.bind('<Key-Down>', lambda e: new_way('down'))
game.bind('<space>', lambda e: pause())
game.bind('<Escape>', lambda e: game_options())

game_start()

game.mainloop()
