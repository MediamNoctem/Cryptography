def divmod_polly(x, y):
    q = [0 for _ in range(len(x) - len(y) + 1)]

    while len(x) >= len(y):
        q[len(y) - len(x) - 1] = 1
        y1 = y + [0] * (len(x) - len(y))
        x = [x[i] ^ y1[i] for i in range(len(x))]

        while len(x) > 0 and x[0] == 0:
            x.pop(0)

    r = x if len(x) > 0 else [0]
    return q, r


def add_polynomials(x, y, p=None):
    if len(x) > len(y):
        y = [0] * (len(x) - len(y)) + y
    else:
        x = [0] * (len(y) - len(x)) + x
    z = [x[i] ^ y[i] for i in range(len(x))]
    while True:
        if len(z) > 1 and z[0] == 0:
            z = z[1:]
        else:
            break
    if p is None:
        return z
    return divmod_polly(z, p)[1]


def multiply_polynomial(x, y, p=None):
    z = [0]
    for i in range(len(y)):
        if y[i] == 1:
            z = add_polynomials(x + [0] * (len(y) - i - 1), z, p)
    return z


def find_item_by_number(n, item_number, p):
    if item_number == 0:
        return [0]
    else:
        return divmod_polly([1] + [0] * ((item_number - 1) % ((2 ** n) - 1)), p)[1]


def substitute_x(x, a, b, p):
    s = multiply_polynomial(x, x, p)  # x^2
    s1 = multiply_polynomial(s, x, p)  # x^3
    s2 = multiply_polynomial(a, s, p)  # a * x^2
    res = add_polynomials(add_polynomials(s1, s2), b, p)
    return res


def find_point(n, item_number, a, b, p):
    x = find_item_by_number(n, item_number, p)
    s = substitute_x(x, a, b, p)
    for i in range(2 ** n):
        y = find_item_by_number(n, i, p)
        s1 = multiply_polynomial(y, y, p)  # y^2
        s2 = multiply_polynomial(x, y, p)  # x * y
        res = add_polynomials(add_polynomials(s1, s2, p), s, p)
        if len(res) == 1 and res[0] == 0:
            return [x, y]
    return None


def find_inverse_point(point, p):
    x = point[0]
    y = add_polynomials(point[0], point[1], p)
    return [x, y]


def find_all_points(n, a, b, p):
    points = []
    for i in range(2 ** n):
        point = find_point(n, i, a, b, p)
        if point is not None:
            points.append([make_polynomial(point[0]), make_polynomial(point[1])])
            inv_point = find_inverse_point(point, p)
            points.append([make_polynomial(inv_point[0]), make_polynomial(inv_point[1])])
    return points


def make_polynomial(t):
    if len(t) == 1:
        return str(t[0])
    poly = "g^" + str(len(t) - 1)
    for i in range(1, len(t) - 1):
        if t[i] == 1:
            poly += " + g^" + str(len(t) - i - 1)
    if t[-1] == 1:
        poly += " + 1"
    return poly


# GF(2^n)
# p - образующий полином.
n = 4
a = [1, 0, 0, 0, 0] # g^4
b = [1]             # 1
p = [1, 0, 0, 1, 1] # p(x) = x^4 + x + 1
points = find_all_points(n, a, b, p)
print(points)


# x1 = [1,0,0,0,0,0]
# x2 = [1,0,0,0,0,0,0,0,0,0,0]
# y1 = [1,0,0,0]
# y2 = [1,0,0,0,0,0,0,0,0]
# # l = add_polynomials(x1, multiply_polynomial(y1, [1,0,0,0,0,0,0]))
#
# l = multiply_polynomial(add_polynomials(y2,y1,p), [1],p)
#
# # x = add_polynomials(add_polynomials(multiply_polynomial(l,l,p), l, p), a, p)
# # y = add_polynomials(add_polynomials(multiply_polynomial(x1,x1,p), multiply_polynomial(l,x), p), x,p)
#
# x = add_polynomials(add_polynomials(multiply_polynomial(l,l,p),l,p),add_polynomials(add_polynomials(x1,x2),a,p),p)
# y = add_polynomials(multiply_polynomial(l, add_polynomials(x1,x,p),p),add_polynomials(x,y1,p),p)
#
# print(x)
# print(y)
