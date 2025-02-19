import bitarray

'''

b – размер состояния (обычно 1600 бит).
r – скорость (rate).
c – емкость (capacity), при этом r + c = b.

# 1. дополнение дл длины r

sha-3 (r + c = 1600 = b )
sha3-256 (r = 1088, c=512

'''


class SHA3:
    def __init__(self, b, r, c):
        self.b = b
        self.r = r
        self.c = c

    # def to_bits(self, message: str) -> bits.Bits:
    #     bits_arr = bits.string_to_bits(message)
    #     return

    def padding(self, message_bits: bitarray.bitarray) -> bitarray.bitarray:
        # шаг 1
        # pad10*1, 1 + 0*r + 1
        # добавим 1 000000 (r) 1 бит
        # len(bytes) % r = k
        # if k = 0 -> k = r
        # k - сколько бит надо добавить
        # 1 << (k-1), т.к. 1 уже занимает 1 позицию,
        # padding = 1 << (k-1)
        # padding.extend(0b1)
        pad_len = (-len(message_bits) - 2) % self.r + 2
        # if pad_len == 0:
        #     pad_len = self.r
        padding_bits = bitarray.bitarray('1' + '0' * (pad_len - 2) + '1')
        return message_bits + padding_bits

    def split_message(self, message_bits: bitarray.bitarray) -> list[bitarray.bitarray]:
        # шаг 2
        # n * r = len(message_bits), n - кол-во частей
        # n * r = len(^) = r * k, так как после дополнения длина кратна r
        # берем по r бит каждый раз.

        parts = []
        for i in range(0, len(message_bits), self.r):
            parts.append(message_bits[i:i + self.r])
        return parts


if __name__ == '__main__':
    s = SHA3(1, 4, 1)
    print(s.padding(bitarray.bitarray([1, 0, 1])))
