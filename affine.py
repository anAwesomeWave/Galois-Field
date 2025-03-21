from galois_field import GF


class Affine:
    def __init__(self, a, b, gf):
        if a == 0:
            raise ValueError(
                "Неправильный ключ a. Он должен принадлежать"
                "мультипликативнйо группе"
            )
        total_elems = gf.p ** gf.n
        if total_elems < 128:
            print(f"WARNING: Количество элементов поля ({total_elems}) меньше "
                  f"кол-ва симоволов в таблице ascii. возможны коллизии."
                  f"Попробуйте GF(2, 8)")
        self.gf = gf
        self.a = gf.int_to_poly(a)
        self.b = gf.int_to_poly(b)

        # либо расширенный евклид либо просто перебор всех возможных ключей
        # если какой-то другой элемент из поля даст 1 то он обратный
        self.inv_a = gf.find_inv_perebor(self.a)

    def __str__(self):
        return f'a={self.a}, b={self.b}, inv_a={self.inv_a}'

    def ascii_to_galois(self, text):
        "берем порядковый номер по модулю"
        ans = []
        for char in text:
            ans.append(self.gf.int_to_poly(ord(char)))
        return ans

    def galois_to_ascii(self, galois_text):
        "идем по полиному справа налево суммируя и домножая на p"
        ans = []
        for poly in galois_text:
            ans.append(chr(self.gf.poly_to_int(poly)))
        return "".join(ans)

    def encrypt(self, plaintext):
        plain_poly = self.ascii_to_galois(plaintext)
        ans = []
        for poly in plain_poly:
            ans.append(self.gf.poly_sum(self.gf.poly_mult(self.a, poly), self.b))
        return self.galois_to_ascii(ans)

    def decrypt(self, ciphertext):
        cipher_poly = self.ascii_to_galois(ciphertext)
        ans = []
        for poly in cipher_poly:
            ans.append(self.gf.poly_mult(self.gf.poly_sub(poly, self.b), self.inv_a))
        return self.galois_to_ascii(ans)


# a = Affine(3, 1, GF(2, 3))
#
# print(a)

# gf = GF(3, 3)
# print(gf.poly_mult([1, 1, 0, 2], [2]))

if __name__ == '__main__':
    aff = Affine(3, 2, GF(3, 5))
    print(aff.a, aff.b)
    print(aff.galois_to_ascii(aff.ascii_to_galois("hello world")))
    print(aff.decrypt(aff.encrypt("hello world")))

    cipher = aff.encrypt("my new secret message.123213.!")
    print(cipher)
    print(aff.decrypt(cipher))
    # print(aff.gf)
