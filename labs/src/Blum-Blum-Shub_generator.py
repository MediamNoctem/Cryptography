# import random
# import math

def BBS_generator(p, q):
    n = p*q
    # s = n
    # while math.gcd(s, n) != 1:
    #     s = random.randint(1, n - 1)
    s = 100
    x = s ** 2 % n
    i = 0
    # print(str(i) + ": x = " + str(x))
    while i < 12:
        i += 1
        x = x ** 2 % n
        b = x % 2
        # print(str(i) + ": x = " + str(x))
        print(str(i) + ": b = " + str(b))


p = 7
q = 19
BBS_generator(p, q)
