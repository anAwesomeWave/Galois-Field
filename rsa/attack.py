import math


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Обратного числа для {a} по модулю {m} не существует")
    return x % m

def is_perfect_square(n):
    """ Проверяет, является ли n идеальным квадратом """
    root = int(math.isqrt(n))
    return root * root == n


def fermat_factorization(n):
    """
    Факторизация методом Ферма.
    Работает лучше всего, если p и q близки друг к другу.
    """
    x = math.isqrt(n)  # Начинаем с sqrt(n)
    if x * x == n:  # Если n уже квадрат, возвращаем его корень
        return x, x

    while True:
        x += 1
        y2 = x * x - n  # Вычисляем y^2
        if is_perfect_square(y2):  # Если y^2 — идеальный квадрат
            y = int(math.sqrt(y2))
            return x - y, x + y  # p, q = (x - y), (x + y)


def find_private_key(n, e):
    """ Факторизует n, вычисляет phi(n) и находит закрытый ключ d """
    p, q = fermat_factorization(n)  # Используем метод Ферма
    if p is None:
        raise ValueError("Не удалось факторизовать n")

    phi = (p - 1) * (q - 1)
    d = mod_inverse(e, phi)  # Обратное к e по модулю phi
    return d, p, q

# Пример использования:
open_n = 21583  # Должно разложиться как 101 * 113
open_e = 13
# p, q = fermat_factorization(n)
# print(f"Факторизация n={n}: p = {p}, q = {q}")

print(find_private_key(open_n, open_e))