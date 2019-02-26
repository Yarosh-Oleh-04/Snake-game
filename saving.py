def save(snake, tail):
    data = []
    data += [open('data.txt').read().split('\n')[0]]
    data += [str(snake['x'])]
    data += [str(snake['y'])]
    data += [str(snake['l'])]
    data += [str(snake['way'])]
    data += [str(snake['status'])]
    data += [str(snake['game'])]
    data += [str(snake['task'])]
    t = []
    for i in tail:
        t += [str(i['x']) + ' ' + str(i['y'])]
    data += ['|'.join(t)]
    open('data.txt', 'w').write('\n'.join(data))


def update():
    data = open('data.txt').read().split('\n')
    snake = data
    return snake, data[8]




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
