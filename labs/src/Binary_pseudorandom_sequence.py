alpha = [1, 1, 0, 1, 0]
x = [1, 0, 1, 0, 1]
n = len(alpha)
print("a: " + str(alpha))
for i in range(30):
    print(str(i) + ": " + str(x))
    z = alpha[0] * x[-n]
    for j in range(1, n):
        z ^= alpha[j] * x[-n + j]
    x.append(z)
