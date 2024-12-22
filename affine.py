from galois_field import GF

class Affine:
    def __init__(self, a, b, gf):
        if a == 0:
            raise ValueError(
                "Неправильный ключ a. Он должен принадлежать"
                "мультипликативнйо группе"
            )
        self.a = gf.int_to_poly(a)
        self.b = gf.int_to_poly(b)

        # либо расширенный евклид либо просто перебор всех возможных ключей
        # если какой-то другой элемент из поля даст 1 то он обратный
        self.inv_a = gf.find_inv_perebor(self.a)

    def __str__(self):
        return f'a={self.a}, b={self.b}, inv_a={self.inv_a}'


a = Affine(3, 1, GF(2, 3))



print(a)
# gf = GF(3, 3)
# print(gf.poly_mult([1, 1, 0, 2], [2]))
