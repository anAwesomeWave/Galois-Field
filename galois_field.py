from tabulate import tabulate


class GF:
    def __init__(self, p=2, n=3, f=None):
        self.p = p
        self.n = n
        self.all_elems = self.poly_generator()  # сразу сгенерируем все элементы поля
        if f is None:
            f = self.generate_irreducible()
        self.f = f  # неприводимый
        if not self.is_irreducible(self.f):
            raise ValueError(f"Polynomial {self.f} not irreducible in GF(p={self.p}, n={self.n})")
        # print("GF: f(x) =", self.f)
        self.primitive = self.find_primitive()

    def poly_mod(self, poly):
        return [c % self.p for c in poly]

    def poly_generator(self):
        numbers_in_base = []

        for num in range(self.p ** self.n):
            digits = []
            n = num
            while n > 0:
                digits.insert(0, n % self.p)
                n //= self.p

            if num == 0:
                digits = [0]

            numbers_in_base.append(digits)
        return numbers_in_base

    def poly_div(self, dividend, divisor):
        """
        Делит один многочлен на другой в поле Галуа (GF(p)).
            dividend - делимое
        """
        quotient = []
        remainder = dividend[:]

        while len(remainder) >= len(divisor):
            lead_coeff_rem = remainder[0]
            lead_coeff_div = divisor[0]

            term_coeff = (lead_coeff_rem * pow(lead_coeff_div, -1, self.p)) % self.p

            quotient.append(term_coeff)

            term = [term_coeff * coeff % self.p for coeff in divisor] + [0] * (len(remainder) - len(divisor))
            remainder = [(rem - term[i]) % self.p for i, rem in enumerate(remainder)]

            # убрать 1 зануленный коеф.
            if remainder and remainder[0] == 0:
                remainder.pop(0)

        # Если остаток пуст, заменяем его на [0]
        if not remainder:
            remainder = [0]
        while len(remainder) > 1 and remainder[0] == 0:
            remainder.pop(0)

        # Дополняем частное нулями до корректной длины
        quotient = quotient + [0] * (len(dividend) - len(quotient) - len(divisor) + 1)

        return quotient, remainder

    def poly_mult(self, a, b):
        """Умножение двух многочленов в поле F_p."""
        result = [0] * (len(a) + len(b) - 1)
        for i, c1 in enumerate(a):
            for j, c2 in enumerate(b):
                result[i + j] += c1 * c2
                result[i + j] %= self.p  # Операция по модулю p
        return self.poly_div(result, self.f)[1]  # берем остаток (то есть приводим по модулю с помощью неприводимого)

    def poly_sum(self, a, b):
        """Пусть len(a) - всегда <= len(b)"""
        if len(a) > len(b):
            a, b = b, a
        pos_a = len(a) - 1
        pos_b = len(b) - 1
        result = [0] * len(b)
        while pos_a > -1:
            result[pos_b] += (a[pos_a] + b[pos_b]) % self.p
            pos_a -= 1
            pos_b -= 1
        while pos_b > -1:
            result[pos_b] += b[pos_b] % self.p
            pos_b -= 1
        while len(result) > 1 and result[0] == 0:
            result.pop(0)
        return result

    def poly_sub(self, a, b):
        inv_b = [-x for x in b]
        return self.poly_sum(a, inv_b)

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
            rem = self.poly_div(poly, elem)[1]
            if len(rem) == 1 and rem[0] == 0:
                return False
        return True

    def int_to_poly(self, i):
        return self.all_elems[i % self.p ** self.n]

    def poly_to_int(self, poly):
        ans = 0
        cur_p = 1
        for i in range(len(poly) - 1, -1, -1):
            ans += poly[i] * cur_p
            cur_p *= self.p
        return ans

    def find_inv_perebor(self, poly):
        for elem in self.all_elems:
            if self.poly_mult(poly, elem) == [1]:
                return elem
        raise ValueError(f"CANNOT FIND inv. Probably bad elem (0?) {poly}")

    def find_primitive(self):
        for elem in self.all_elems[1::]:
            if self.is_primitive(elem):
                return elem

    def is_primitive(self, elem):
        power = self.p ** self.n - 1  # столько элементов в мультипликативнйо группе
        cur_elem = elem
        # print(cur_elem)
        for i in range(power - 1):  # сдвиг, так как начинаем с нуля, а внутри цикла уже 2 степень
            if cur_elem == [1]:  # в меньший степенях не должен давать 1
                return False
            cur_elem = self.poly_mult(cur_elem, elem)
            # print(cur_elem)
        return cur_elem == [1]

    def generate_primitive_powers(self):
        # на выходе словарь, элемент - степень
        powers_dict = dict()
        power = self.p ** self.n - 1  # столько элементов в мультипликативнйо группе
        cur_elem = self.primitive
        for i in range(power - 1):  # сдвиг, так как начинаем с нуля, а внутри цикла уже 2 степень
            if cur_elem == [1]:  # в меньший степенях не должен давать 1
                return False
            powers_dict[tuple(cur_elem)] = i + 1
            cur_elem = self.poly_mult(cur_elem, self.primitive)
        powers_dict[tuple(cur_elem)] = power
        return powers_dict

    def __str__(self):
        def visualize_poly(poly):
            if len(poly) == 1 and poly[0] == 0:
                return "0"
            return "".join(
                [
                    f" + {x}*x^{len(poly) - ind - 1}" if x != 0 and x != 1 else "" if x == 0 else f" + x^{len(poly) - ind - 1}"
                    for ind, x in enumerate(poly)]
            ).strip(" + ")
        powers_dict = self.generate_primitive_powers()
        powers = [f"a^{powers_dict[tuple(i)]}" if tuple(i) in powers_dict else " - " for i in self.all_elems]

        elements = tabulate(zip(powers, [visualize_poly(i) for i in self.all_elems]), headers=['Element', 'Polynomial'],
                            tablefmt='orgtbl')
        return elements + f"\n f(x) = {self.f}"


if __name__ == "__main__":
    # gf = GF(3, 2, [2, 1, 1])
    # print(gf.poly_div([1, 0, 0], [2, 1, 1]))

    print('-----')
    # gf = GF(2, 3, [1, 1, 0, 1])
    # print(gf.poly_mult([1, 1, 0], [1, 1]))
    # print(gf)
    # print(gf.all_elems)
    # print(GF(5, 2))
    gf = GF(5, 2)
    print(gf)
