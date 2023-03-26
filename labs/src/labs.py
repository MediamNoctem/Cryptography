# ------------ lab1 ------------
# Поиск всех делителей
def find_divisors(n):
    d = []
    for i in range(2, n):
        if n % i == 0:
            d.append(i)
    return d


# Определение простоты числа
def is_prime(n):
    if n <= 2:
        return True
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


# Функция Эйлера
def Euler_function(n):
    if is_prime(n):
        return n - 1
    else:
        res = n
        d = find_divisors(n)
        for i in d:
            res *= (1 - 1 / i)
        return round(res)


# Вычисление НОД двух чисел
def calc_gcd(a, b):
    if a < b:
        tmp = a
        a = b
        b = tmp
    while b:
        r = a % b
        a = b
        b = r
    return a


# Нахождение взаимно простых чисел, меньше заданного
def calc_coprime_numbers(n):
    c = []
    for i in range(2, n):
        if calc_gcd(i, n) == 1:
            c.append(i)
    return c


# Вычисление минимального первообразного корня
def calc_min_primitive_root(n):
    if not is_prime(n):
        print("Ошибка: значение модуля не является простым числом.")
    else:
        fi = Euler_function(n)
        print("Значение функции Эйлера от " + str(n) + ": " + str(fi) + ".")
        d = find_divisors(fi)
        print("Значение функции Эйлера кратно таким числам, как: " + str(d) + ".")
        print("Ищем первообразный корень.")
        for i in range(2, n):
            print("a = " + str(i))
            flag = True
            for j in d:
                print(str(i) + "^" + str(j) + " (mod " + str(n) + ") = " + str((i ** j) % n) + " (mod " + str(n) + ")")
                if (i ** j) % n == 1:
                    print("Единица получилась раньше времени, следовательно, число " + str(i) + " не является "
                                                                                                "первообразным "
                                                                                                "корнем.")
                    flag = False
                    break
            if flag:
                print("Единица не была получена раньше времени, следовательно, число " + str(i) + " является "
                                                                                                  "первообразным "
                                                                                                  "корнем.")
                return i


# Вычисление всех первообразных корней через минимальный
def calc_all_primitive_roots(n):
    if not is_prime(n):
        print("Ошибка: значение модуля не является простым числом.")
    else:
        min_root = calc_min_primitive_root(n)
        print("Минимальный первообразный корень: " + str(min_root))
        roots = [min_root]
        c = calc_coprime_numbers(n - 1)
        print("Ищем степени, значения которых будут взаимно простыми с числом " + str(Euler_function(n)) + ".")
        print("Степени: " + str(c))
        print("Вычисление остальных первообразных корней:")
        for i in c:
            print(str(min_root) + "^" + str(i) + " (mod " + str(n) + ") = " + str((min_root ** i) % n) + " (mod " + str(
                n) + ")")
            roots.append((min_root ** i) % n)
        return roots


# ------------ lab2 ------------
# Разложить модуль на простые множители
def find_simple_divisors(n):
    d = []
    for i in range(2, n + 1):
        while n % i == 0:
            d.append(i)
            n /= i
    return d


# Вычислить символ Лежандра
def calc_Legendre_symbol(a, p):
    if is_prime(p):
        L = round((a ** ((p - 1) / 2)) % p)
        if L > 1:
            return L - p
        else:
            return L
    else:
        print("Ошибка: значение модуля не является простым числом!")
        return None


# Представить простой модуль в виде 4k + i
def present_in_form_4k_plus_i(p, i):
    m = p - i
    if m % 4 == 0:
        return round(m / 4)
    else:
        return None


# Решение квадратичного сравнения по простому модулю
def solve_quadratic_comparison_by_simple_modulus(a, p):
    print("--------------------------------------------------------")
    print("Дано квадратичное сравнение по простому модулю: x^2 = " + str(a) + " mod " + str(p) + ".")
    print("Проверим нулевое решение.")
    if a % p == 0:
        print(str(a) + " mod " + str(p) + " = 0 mod " + str(p) + ".")
        print("x = 0 mod " + str(p) + ".")
        return [0]
    print("x = 0 не является решением сравнения.")
    if p == 2:
        print("p < 3, поэтому отдельно проверим ещё один возможный корень: 1.")
        if a == 1:
            print("a = 1 mod " + str(p) + "  =>  1 является корнем сравнения.")
            s = [1]
            print("x = 1 mod " + str(p) + ".")
            return s
        print("Решения нет.")
        return None
    else:
        print("Попробуем представить значение модуля в виде 4k + 3.")
        k = present_in_form_4k_plus_i(p, 3)
        if k is not None:
            print("p = 4 * " + str(k) + " + 3  =>  k = " + str(k))
            s = [(a ** (k + 1)) % p, -((a ** (k + 1)) % p)]
            print("Найдем решение сравнения.")
            print("x = " + str(s[0]) + " mod " + str(p) + ";")
            print("x = " + str(s[1]) + " mod " + str(p) + ".")
            return s
        else:
            print("Значение модуля не представляется в виде 4k + 3.")
            print("Попробуем представить значение модуля в виде 4k + 1.")
            k = present_in_form_4k_plus_i(p, 1)
            if k is not None:
                print("p = 4 * " + str(k) + " + 1  =>  k = " + str(k))
                print("Решение квадратичного сравнения затруднительно.")
                return None
            else:
                print("Значение модуля нельзя представить в виде 4k + 1.")
                return None


# Найти обратный элемент по модулю
def calc_multiplicative_inversion_of_element_modulo(a, n):
    return (a ** (Euler_function(n) - 1)) % n


# Китайская теорема об остатках
def crt(b, m):
    n = len(m)

    Module = 1
    for i in range(n):
        Module *= m[i]

    M = []
    for i in range(n):
        M.append(round(Module / m[i]))

    M_ = []
    for i in range(n):
        M_.append(calc_multiplicative_inversion_of_element_modulo(M[i], m[i]))

    x = 0
    for i in range(n):
        x += (b[i] * M[i] * M_[i]) % Module
    x = x % Module
    return x


def enumeration(list, a):
    res = [0 for _ in range(len(list))]
    for i in range(len(list)):
        res[i] = list[i][a[i]]
    return res


def change_a(list, a):
    n = len(a) - 1
    while True:
        n_max = len(list[n]) - 1
        if a[n] < n_max:
            a[n] += 1
            return a
        else:
            if n != 0:
                a[n] = 0
                n -= 1
            else:
                return a


# Общий алгоритм решения квадратичного сравнения
def solve_quadratic_comparison(a, n):
    print("--------------------------------------------------------")
    print("1. Дано квадратичное сравнение: x^2 = " + str(a) + " mod " + str(n) + ".")
    print("2. Разложим значение модуля на произведение простых чисел.")
    d = find_simple_divisors(n)
    if len(d) == 1:
        print("Значение модуля - простое число.")
    else:
        print("Значение модуля представимо в виде произведения чисел: " + str(d) + ".")
    print("3. Вычислим значение символа Лежандра, чтобы определить, имеет ли сравнение решение.")
    for i in d:
        L = calc_Legendre_symbol(a % i, i)
        print("L(" + str(a % i) + ", " + str(i) + ") = " + str(L))
        if L is None:
            return None
        if L == -1:
            print("Сравнение не имеет решений.")
            return None
    print("Сравнение имеет решение.")
    print("4. Приступим к решению сравнения.")
    if len(d) == 1:
        return solve_quadratic_comparison_by_simple_modulus(a % n, n)
    else:
        print("Решим систему квадратичных сравнений по простому модулю.")
        decisions = []
        list = []
        for i in d:
            list_ = solve_quadratic_comparison_by_simple_modulus(a % i, i)
            if list_ is None:
                return None
            else:
                list.append(list_)
        print("--------------------------------------------------------")
        print("Составим системы сравнений по вычисленным значениям.")
        len_a = len(list)
        a_ = [0 for _ in range(len_a)]
        size = 1
        for i in list:
            size *= len(i)
        for i in range(size):
            b = enumeration(list, a_)
            print("--------------------------------------------------------")
            print("Система " + str(i + 1) + ".")
            for j in range(len(b)):
                print("x = " + str(b[j]) + " mod " + str(d[j]))
            decisions.append(crt(b, d))
            print("По КТО получаем решение: x = " + str(decisions[-1]))
            a_ = change_a(list, a_)
        print("--------------------------------------------------------")
        return decisions


# ------------ lab5 ------------
def Pollard_p_1_factorization(n, B):
    print("--------------------------------------------------------")
    print("p - 1 метод Полларда.")
    print("--------------------------------------------------------")
    a = 2
    e = 2
    print("Инициализация: a = " + str(a) + "; e = " + str(e) + ".")
    while e <= B:
        print("e <= " + str(B) + "  =>")
        a = (a ** e) % n
        e += 1
        print("   a = " + str(a) + " mod " + str(n) + ";")
        print("   e = " + str(e) + ".")
    p = calc_gcd(a - 1, n)
    print("e > " + str(B) + "  =>  было пройдено заданное количество итераций.")
    print("p = gcd(" + str(a - 1) + ", " + str(n) + ") = " + str(p) + ".")
    if (p > 1) and (p < n):
        print(str(n) + " = " + str(p) + " * " + str(n // p) + ".")
        print("--------------------------------------------------------")
        return p
    print("Делитель не может быть найден при заданном значении числа B.")
    print("--------------------------------------------------------")
    return None


def f(x):
    return x ** 2 + 1


def Pollard_rho_factorization(n):
    print("--------------------------------------------------------")
    print("РО(Rho) - метод Полларда.")
    print("--------------------------------------------------------")
    print("В качестве функции используется f(x) = x^2 + 1.")
    x = 2
    y = 2
    p = 1
    print("Инициализация: x = " + str(x) + "; y = " + str(y) + "; p = " + str(p) + ".")
    while p == 1:
        print("p == 1  =>")
        x = f(x) % n
        y = f(f(y) % n) % n
        p = calc_gcd(abs(x - y), n)
        print("   x = " + str(x) + " mod " + str(n) + ";")
        print("   y = " + str(y) + " mod " + str(n) + ";")
        print("   p = gcd(" + str(abs(x - y)) + ", " + str(n) + ") = " + str(p) + ".")
    print("p != 1  => найден делитель числа " + str(n) + ".")
    print(str(n) + " = " + str(p) + " * " + str(n // p) + ".")
    print("--------------------------------------------------------")
    return p


# ------------ lab8 ------------
def BPS(f, x, file_name):
    file = open(file_name, "a")
    alpha = []
    n = len(f)
    for i in range(n - 1):
        alpha.append(f[-(i + 1)])
    file.write("a: " + str(alpha) + "\n")
    n = len(alpha)
    for i in range(2 ** (len(f) - 1)):
        file.write(str(i) + ": " + str(x) + "\n")
        z = alpha[0] * x[-n]
        for j in range(1, n):
            z ^= alpha[j] * x[-n + j]
        x.append(z)
    file.close()


# calc_all_primitive_roots(33)
# 4 21
# 4 14
# 4 7
# 5 10
# solve_quadratic_comparison(7, 13)
# Pollard_p_1_factorization(687, 3)
# Pollard_rho_factorization(687)
f10 = [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
x10 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
# BPS(f10, x10, "BPS_primitive_10.txt")
f6 = [1, 0, 0, 0, 0, 1, 1]
x6 = [1, 0, 0, 0, 0, 1]
# BPS(f6, x6, "BPS_primitive_6.txt")
f14 = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1]
x14 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
BPS(f14, x14, "BPS_primitive_14.txt")
