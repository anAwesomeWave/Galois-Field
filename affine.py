from galois_field import GF

# gf = GF(3, 3)
#
# print(gf.all_elems)
# print(gf.int_to_poly(-1))


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
        self.inv_a = gf.int_to_poly()



gf = GF(3, 3)
print(gf.poly_mult([1, 1, 0, 2], [1, 0, 0]))