import numpy as np
from tabulate import tabulate
from sympy import div

# print(np.polydiv([1, 0], [1]))
# print(np.polydiv(np.polymul([1, 0], [1, 0, 0]), [1, 0, 1, 1]))


# пример поля галуа
# GF(2^3) f(x) = x^3 + x + 1
# умножаем x * x^2 = x^3 == -x - 1 = x + 1

class GF:
    def __init__(self, p=2, n=3, poly=None):
        self.p = p
        self.n = n
        self.all_elems = self.poly_generator2()  # сразу сгенерируем все элементы поля
        if poly is None:
            poly = self.generate_irreducible()
        self.f = poly  # неприводимый
        if not self.is_irreducible(self.f):
            raise ValueError(f"Polynom {self.f} not irreducible in GF(p={self.p}, n={self.n})")

    def poly_mod(self, poly):
        return [c % self.p for c in poly]

    def poly_generator(self):
        """ Генерирует все многочлены поля галуа"""

        ans = []

        def rec_gen(cur_pos, cur_poly):
            if cur_pos == self.n:
                ans.append(cur_poly)
                return
            for i in range(self.p):
                rec_gen(cur_pos + 1, cur_poly + [i])

        rec_gen(0, [])
        return ans

    def poly_generator2(self):
        """ Генерирует все многочлены поля галуа. Без нулевого префикса"""

        ans = []

        def rec_gen(cur_pos, cur_poly):
            if cur_pos == self.n:
                return
            if len(cur_poly) > 0 and cur_poly[0] == 0:
                return
            for i in range(int(cur_poly == 0), self.p):
                ans.append(cur_poly + [i])
            for i in range(self.p):
                rec_gen(cur_pos + 1, cur_poly + [i])

        rec_gen(0, [])
        return ans

    def poly_div(self, dividend, divisor):
        """
        Делит один многочлен на другой в поле Галуа (GF(p)).
            dividend - делимое
        """
        quotient = []
        remainder = dividend[:]

        while len(remainder) >= len(divisor):
            # print("REM AND DIV", remainder, divisor, quotient)
            lead_coeff_rem = remainder[0]
            lead_coeff_div = divisor[0]

            term_coeff = (lead_coeff_rem * pow(lead_coeff_div, -1, self.p)) % self.p

            # print("COEFFF", term_coeff)
            quotient.append(term_coeff)

            term = [term_coeff * coeff % self.p for coeff in divisor] + [0] * (len(remainder) - len(divisor))
            remainder = [(rem - term[i]) % self.p for i, rem in enumerate(remainder)]

            # print("REM AND DIV2", remainder, divisor, quotient)
            # если занулились больше 1 коеф. то мы должны добавить нули в ответ
            # например [1, 1, 0, 2], [2], GF(3)
            # без добавления будет [2, 2, 1, 0] - неверно
            if remainder and remainder[0] == 0:
                remainder.pop(0)
                # while remainder and remainder[0] == 0:
                #     quotient.append(0)
                #     remainder.pop(0)

            # print("REM AND DIV3", remainder, divisor, quotient)

        # Если остаток пуст, заменяем его на [0]
        if not remainder:
            remainder = [0]
        while len(remainder) > 1 and remainder[0] == 0:
            remainder.pop(0)

        # Дополняем частное нулями до корректной длины
        quotient = quotient + [0] * (len(dividend) - len(quotient) - len(divisor) + 1)

        # print("REM AND DIV4", remainder, divisor, quotient)
        return quotient, remainder

    def poly_mult(self, a, b):
        """Умножение двух многочленов в поле F_p."""
        result = [0] * (len(a) + len(b) - 1)
        for i, c1 in enumerate(a):
            for j, c2 in enumerate(b):
                result[i + j] += c1 * c2
                result[i + j] %= self.p  # Операция по модулю p
        # TODO: проверить
        # print(result)
        # while len(result) > 1 and result[0] == 0:
        #     result.pop(0)
        print("START")
        print(result, self.f)
        return self.poly_div(result, self.f)[1]  # берем остаток (то есть приводим по модулю с помощью неприводимого)

    def generate_possible_irreducible(self):
        """ Генерирует все возможные полиномы степени self.n"""

        ans = []

        def rec_gen(cur_pos, cur_poly):
            if cur_pos == self.n:
                ans.append(cur_poly)
                return
            for i in range(self.p):
                rec_gen(cur_pos + 1, cur_poly + [i])

        for i in range(1, self.p):
            rec_gen(0, [i])
        # print(ans)
        return ans

    def generate_irreducible(self):
        """генерируем f(x) для GF(p, n)"""
        for i in self.generate_possible_irreducible():
            if self.is_irreducible(i):
                return i

    def is_irreducible(self, poly):
        """ Проверяем, является ли self.f неприводимым в поле галуа GF(self.p^self.n)"""
        # 1. Сгенерировать все многочлены
        # 2. Для каждого проверить остаток от деления f / cur != 0

        # на скалярные не делим!
        for elem in self.all_elems[self.p:]:
            # print(poly, elem)
            # print(self.poly_div(poly, elem))
            if all(int(x) == 0 for x in self.poly_div(poly, elem)[1]):
                return False
        return True

    def int_to_poly(self, i):
        return self.all_elems[i % self.p ** self.n]

    def find_inv_perebor(self, poly):
        for elem in self.all_elems:
            print(poly, elem)
            print(po)

    def __str__(self):
        def visualize_poly(poly):
            if len(poly) == 1 and poly[0] == 0:
                return "0"
            return " ".join(
                [
                    f"+ {x}*x^{len(poly) - ind - 1}" if x != 0 and x != 1 else "" if x == 0 else f"+ x^{len(poly) - ind - 1}"
                    for ind, x in enumerate(poly)]
            ).strip(" + ")

        powers = [f"a^{i}" for i in range(self.n ** self.p)]

        elements = tabulate(zip(powers, [visualize_poly(i) for i in self.all_elems]), headers=['Element', 'Polynom'],
                            tablefmt='orgtbl')

        return elements + f"\n f(x) = {self.f}"


gf = GF(2, 3)

# print(gf.is_irreducible())
# print(gf.generate_irreducible())
# print(gf.f)
# print(gf)