def save(snake, tail):
    data = []
    data += open('data.txt').read().split('\n')[0]
    data += [str(snake['x'])]
    data += [str(snake['y'])]
    data += [str(snake['l'])]
    data += [str(snake['way'])]
    data += [str(snake['status'])]
    data += [str(snake['game'])]
    data += [str(snake['task'])]
    t = ''
    for i in tail:
        t += str(i['x']) + ' ' + str(i['y']) + '|'
    data += [t]
    open('data.txt', 'w').write('\n'.join(data))


def update():
    data = open('data.txt').read().split('\n')
    snake = dict(x=None, y=None, l=None, way=None, status=None, game=None, task=None)
    tail = []
    snake['x'] = int(data[1])
    snake['y'] = int(data[2])
    snake['l'] = int(data[3])
    snake['way'] = data[4]
    snake['status'] = data[5]
    snake['game'] = data[6]
    snake['task'] = data[7]
    if len(tail) > 0:
        for t in data[8].split('|'):
            t = t.split(' ')
            tail += [dict(x=int(t[0]), y=int(t[1]))]
    return snake, tail




def nullify():
    pass


def save_score(score):
    data = open('data.txt').read().split('\n')
    if int(data[0]) < score:
        data[0] = str(score)
        open('data.txt', 'w').write('\n'.join(data))
    return data[0]


def nullify_score():
    data = open('data.txt').readlines()
    data[0] = '0'
    open('data.txt', 'w').write('\n'.join(data))
