import random
from math import isqrt, sqrt


class EllipticCurve:
    def __init__(self, a, b, p):
        if (4 * a ** 3 + 27 * b ** 2) % p == 0:
            raise ValueError("Кривая вырождена! Коэффициенты a и b не удовлетворяют условию 4a^3 + 27b^2 != 0 (mod p).")
        self.a = a
        self.b = b
        self.p = p

        self.sq_roots = self.get_sq_roots()  # возвращает словарь x -> [y1, y2], где x принадлежит GFp,
        # yi*yi = x, i = 1, 2, 3...

        self.all_points = self.generate_points_trivial()
        assert self.generate_points_sq() == self.generate_points_trivial()
        self.N = len(self.all_points)  # порядок группы

    def get_sq_roots(self):
        d = {}
        for i in range(self.p):
            p = (i * i) % self.p
            if p not in d:
                d[p] = []
            d[p].append(i)
        return d

    def inverse_point(self, point):
        return point[0], self.p - point[1]

    def is_point_on_curve(self, x, y):
        # print(x, y, (y * y) % p, (x ** 3 + self.a * x + self.b) % self.p)
        return (y * y) % p == (x ** 3 + self.a * x + self.b) % self.p

    def point_addition(self, P, Q):
        if P == "O":
            return Q
        if Q == "O":
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and y1 != y2:
            return "O"

        if P == Q:
            # Случай удвоения точки
            s = (3 * x1 ** 2 + self.a) * pow(2 * y1, -1, self.p) % self.p
        else:
            # Случай сложения различных точек
            s = (y2 - y1) * pow(x2 - x1, -1, self.p) % self.p

        x3 = (s * s - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p

        return x3, y3

    def scalar_multiply(self, k, p):
        """Compute k * P using the double-and-add method."""
        result = p
        if k == 0:
            return "O"
        if k == 1:
            return p
        if k & 1:  # odd. minus 1
            result = self.point_addition(result, self.scalar_multiply(k - 1, p))
            return result

        while k > 1:
            result = self.point_addition(result, result)
            k >>= 1  # divide by 2

        return result

    def generate_points_trivial(self):
        """
        Генерирует все точки на эллиптической кривой.
        :return: Список точек (включая точку на бесконечности)
        """
        points = ["O"]  # Добавляем точку на бесконечности
        for x in range(self.p):
            for y in range(self.p):
                if self.is_point_on_curve(x, y):
                    points.append((x, y))
        return points

    def generate_points_sq(self):
        """
        Генерирует все точки на эллиптической кривой. пользуясь словарем квадрат элемента поля -> корни в поле
        """
        points = ["O"]  # Добавляем точку на бесконечности
        for x in range(self.p):
            y_p = (x ** 3 + self.a * x + self.b) % self.p  # возможный кварат ответа
            if y_p in self.sq_roots:
                for y in self.sq_roots[y_p]:
                    points.append((x, y))
        return points


def exp_by_modulo(a, k, p):
    b = 1
    if k > 0:
        A = a
        if k & 1:
            b = a
        while k > 0:
            A = (A * A) % p
            k //= 2
            if k % 2 == 1:
                b = (b * A) % p
    return b


def is_prime_fermat(n, it=10):
    if n == 2:
        return True
    if n <= 4 or n % 2 == 0:
        return False

    for i in range(it):
        a = random.randint(2, n - 1)
        r = exp_by_modulo(a, n - 1, n)
        if r != 1:
            return False
    return True


if __name__ == "__main__":
    a = 2
    b = 1
    p = 5

    curve = EllipticCurve(a, b, p)
    print("Генерация точек на кривой:")
    # points = curve.generate_points()
    print(f"Найдено {len(curve.all_points)} точек: {curve.all_points}")
    print((2 ** 3 + curve.a * 2 + curve.b) % curve.p)
    # P = points[1]  # Берем первую точку на кривой
    # Q = points[2]  # Берем вторую точку на кривой
    # print(f"Сложение точек {P} и {Q}: {curve.point_addition(P, Q)}")
    print(curve.generate_points_sq())
    print(curve.scalar_multiply(5, (0, 4)))
    print(curve.point_addition((0, 4), (3, 3)))
    # print(curve.bsgs((1, 2)))
    print(curve.inverse_point((1, 2)))
    print(curve.point_addition((1, 2), (1, 3)))

    print("--------------")
    print(exp_by_modulo(3, 12, 10))
    for i in range(5, 15):
        for j in range(3, 6):
            print(f"n = {i}, mod = {j}, is_prime = {is_prime_fermat(i, j)}")
