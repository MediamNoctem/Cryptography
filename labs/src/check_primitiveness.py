# Реализовать проверку многочлена на неприводимость и примитивность

min_neprivodim_mch = [[1, 0],
                      [1, 1],
                      [1, 1, 1],
                      [1, 0, 1, 1],
                      [1, 1, 0, 1],
                      [1, 0, 0, 1, 1],
                      [1, 1, 1, 1, 1],
                      [1, 1, 0, 0, 1],
                      [1, 0, 0, 1, 0, 1],
                      [1, 0, 1, 0, 0, 1],
                      [1, 0, 1, 1, 1, 1],
                      [1, 1, 0, 1, 1, 1],
                      [1, 1, 1, 0, 1, 1],
                      [1, 1, 1, 1, 0, 1],
                      [1, 0, 0, 0, 0, 1, 1],
                      [1, 0, 0, 1, 0, 0, 1],
                      [1, 0, 1, 0, 1, 1, 1],
                      [1, 0, 1, 1, 0, 1, 1],
                      [1, 1, 0, 0, 0, 0, 1]]


def divmod_polly(x, y):
    q = [0 for i in range(len(x) - len(y) + 1)]

    while len(x) >= len(y):
        q[len(y) - len(x) - 1] = 1
        y1 = y + [0] * (len(x) - len(y))
        x = [x[i] ^ y1[i] for i in range(len(x))]

        while (len(x) > 0 and x[0] == 0):
            x.pop(0)

    r = x if len(x) > 0 else [0]
    return q, r


def is_primitiv(x):
    m_min = len(x)
    m_max = 2 ** (len(x) - 1) - 2

    for i in range(m_min, m_max):
        x_m = [1] + [0] * (i - 1) + [1]
        q, r = divmod_polly(x_m, x)

        if r == [0]:
            return False
    return True


def is_neprivodim(x):
    i = 0

    while len(min_neprivodim_mch[i]) <= len(x) / 2:
        q, r = divmod_polly(x, min_neprivodim_mch[i])

        if r == [0] and min_neprivodim_mch[i] != x:
            return False
        i += 1

    return True


if __name__ == '__main__':
    test1 = [1, 0, 1, 0]  # x^3 + x
    test2 = [1, 1, 0, 1, 1]  # x^4 + x^3 + x + 1
    test3 = [1, 1, 1]  # x^2 + x + 1
    test4 = [1, 0, 1, 1, 0, 1, 1]

    if not is_neprivodim(test4):
        print('Приводимый, непримитивный')
    else:
        print('Неприводимый, ', end='')
        print('примитивный') if is_primitiv(test4) else print('непримитивный')
