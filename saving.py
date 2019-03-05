def save(brain):
    data = []
    data += [open('data.txt').read().split('\n')[0]]
    data += [str(brain['x']) + ' ' + str(brain['y'])]
    data += [brain['way']]
    data += [str(brain['food'][0]['x']) + ' ' + str(brain['food'][0]['y'])]
    t = []
    for i in brain['tail']:
        t += [str(i['x']) + ' ' + str(i['y']) + ' ' + i['way']]
    data += ['|'.join(t)]
    open('data.txt', 'w').write('\n'.join(data))


def update():
    data = open('data.txt').read().split('\n')
    x = int(data[1].split(' ')[0])
    y = int(data[1].split(' ')[1])
    l = len(data[4].split('|'))
    way = data[2]
    tail = []
    for t in data[4].split('|'):
        e = t.split(' ')
        tail += [dict(tail=None, x=int(e[0]), y=int(e[1]), way=e[2])]
    food = [dict(x=int(data[3].split(' ')[0]), y=int(data[3].split(' ')[1])), None]
    brain = dict(x=x, y=y, l=l, snake=None, tail=tail, food=food, way=way, status='pause', task=None)
    return brain


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
