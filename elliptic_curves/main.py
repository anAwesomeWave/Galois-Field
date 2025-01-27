class EllipticCurve:
    def __init__(self, a, b, p):
        """
        Создает эллиптическую кривую вида y^2 = x^3 + ax + b над полем Fp.
        :param a: Коэффициент a
        :param b: Коэффициент b
        :param p: Простое число, определяющее поле Fp
        """
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

    def is_point_on_curve(self, x, y):
        """
        Проверяет, принадлежит ли точка (x, y) кривой.
        :param x: Координата x
        :param y: Координата y
        :return: True, если точка принадлежит кривой, иначе False
        """
        # print(x, y, (y * y) % p, (x ** 3 + self.a * x + self.b) % self.p)
        return (y * y) % p == (x ** 3 + self.a * x + self.b) % self.p

    def point_addition(self, P, Q):
        """
        Складывает две точки на эллиптической кривой.
        :param P: Точка P (x1, y1) или O (бесконечность)
        :param Q: Точка Q (x2, y2) или O (бесконечность)
        :return: Результат сложения P + Q
        """
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

    def bsgs(self):
        """ baby-step-giant-step """
        pass


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
