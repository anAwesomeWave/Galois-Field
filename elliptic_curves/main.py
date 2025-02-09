import random


class EllipticCurve:
    def __init__(self, a, b, p):
        if (4 * a ** 3 + 27 * b ** 2) % p == 0:
            raise ValueError("Кривая вырождена! Коэффициенты a и b не удовлетворяют условию 4a^3 + 27b^2 != 0 (mod p).")
        self.a = a
        self.b = b
        self.p = p

        self.sq_roots = self.get_sq_roots()  # возвращает словарь x -> [y1, y2], где x принадлежит GFp,
        # yi*yi = x, i = 1, 2, 3...

        self.all_points = self.generate_points_sq()
        # assert self.generate_points_sq() == self.generate_points_trivial()
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
            if y1 == 0: # обратный(a*b mod p = 1) не сможем найти по модулю, так как 0
                return "O"
            s = (3 * x1 ** 2 + self.a) * pow(2 * y1, -1, self.p) % self.p
        else:
            # Случай сложения различных точек
            if x2 - x1 == 0:
                return "O"
            s = (y2 - y1) * pow(x2 - x1, -1, self.p) % self.p

        x3 = (s * s - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p

        return x3, y3

    def scalar_multiply(self, k, p):
        """Compute k * P using the double-and-add method."""
        if k == 0 or p == "O":
            return "O"
        if k == 1:
            return p

        result = "O"

        cur_p_2pow = p
        # это число будет каждый  раз равнять 2 ^ i * p. его мы будем прибавлять
        # Ex: 13 = 1101, значит надо сложить p + 4p + 8p
        while k:
            if k % 2 != 0:
                result = self.point_addition(result, cur_p_2pow)
            cur_p_2pow = self.point_addition(cur_p_2pow, cur_p_2pow)
            k >>= 1

        return result

    def generate_points_trivial(self):
        points = ["O"]
        for x in range(self.p):
            for y in range(self.p):
                if self.is_point_on_curve(x, y):
                    points.append((x, y))
        return points

    def generate_points_sq(self):
        """
        Генерирует все точки на эллиптической кривой. пользуясь словарем квадрат элемента поля -> корни в поле
        """
        points = ["O"]
        for x in range(self.p):
            y_p = (x ** 3 + self.a * x + self.b) % self.p  # возможный кварат ответа
            if y_p in self.sq_roots:
                for y in self.sq_roots[y_p]:
                    points.append((x, y))
        return points

    def find_subgroups_prime_deg(self, deg):
        """
            Поиск подгрупп заданной кратности. Задача упрощается, так как deg - простое число,
            то не надо перебирать его делители, нужно только, чтобы o(P) = deg.
            т.е. deg * P = "O". то есть нейтральному элементу
        """
        if not is_prime_fermat(deg):
            raise ValueError(f"Степень должна быть простой! deg = {deg}")

        all_subgroups = []
        for point in self.all_points:
            if point == "O":
                continue
            if self.scalar_multiply(deg, point) == "O":
                # точка явл. образующем подгруппы
                group = [point]
                cur_point = point
                for i in range(deg - 1):
                    cur_point = self.point_addition(cur_point, point)
                    group.append(cur_point)
                all_subgroups.append(group)
        return all_subgroups


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
    if n == 2 or n == 3:
        return True
    if n <= 4:
        return False

    for i in range(it):
        a = random.randint(2, n - 1)
        r = exp_by_modulo(a, n - 1, n)
        if r != 1:
            return False
    return True


"""
    a = 2
    b = 1
    p = 5
"""

"""
    a = 1
    b = 0
    p = 11
    
    для поиска подгрупп
"""
if __name__ == "__main__":
    a = 2
    b = 1
    p = 5
    # ex. 4.1
    curve = EllipticCurve(a, b, p)
    print(f"Генерация точек на кривой: a={curve.a}, b={curve.b}, p={curve.p}")
    # points = curve.generate_points()
    print(f"Найдено {len(curve.all_points)} точек: {curve.all_points}")

    # 4.2
    point = (1, 3)
    cur_point = "O"
    for i in range(1, 10):
        cur_point = curve.point_addition(cur_point, point)
        print(f"k = {i}, С помощью сложения: {cur_point}, Метод скаляра: {curve.scalar_multiply(i, point)}")


    # 4.3
    a = 1
    b = 0
    p = 11
    # ex. 4.1
    curve = EllipticCurve(a, b, p)
    print(f"Генерация точек на кривой: a={curve.a}, b={curve.b}, p={curve.p}")
    print(f"Найдено {len(curve.all_points)} точек: {curve.all_points}")
    # 4.3
    for i in range(1, curve.N):
        # print(i, is_prime_fermat(i))
        try:
            ans = curve.find_subgroups_prime_deg(i)
            if ans != []:
                print(i, ans)
        except ValueError as e:
            if "Степень должна быть простой!" not in e.__str__():
                print(e)
