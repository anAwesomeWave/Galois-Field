import copy
import math
import random
from bitarray import bitarray as ba
from bitarray.util import ba2int, int2ba


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


def is_prime_fermat(n, it=20):
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


def gen_random_prime_number_above(lower_bound):
    # генерирую рандомное просто число (не меньше чем lower_bound)
    lb = random.randint(lower_bound, lower_bound + 1000)
    for i in range(lb, lb + 10000):
        if is_prime_fermat(i):
            return i


def euler(p, q):
    return (p - 1) * (q - 1)


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


def is_coprime(a, b):
    return extended_gcd(a, b)[0] == 1


def gen_l(fn):
    for i in range(2, 1000):
        if is_coprime(i, fn):
            return i


class RSA:
    def __init__(self, keys=None):  # format: (l, n, d) -> l, n = open, n, d = closed
        if keys is None:
            keys = self.generate_keys()
        self.open_keys = (keys[0], keys[1])
        self.closed_keys = (keys[1], keys[2])

    def generate_keys(self):
        p = gen_random_prime_number_above(100)
        q = gen_random_prime_number_above(100)
        fn = euler(p, q)
        l = gen_l(fn)
        d = mod_inverse(l, fn)
        print("p, q, fn, l, d:", p, q, fn, l, d)
        return l, p * q, d

    def get_bin_string(self, message):
        b = ba()
        b.frombytes(message.encode('utf-8'))
        return b

    def _encrypt_block(self, l, n, block, encr_block_size, operation):
        int_val = ba2int(block)
        print(operation, "block:", int_val, block, end="\t")
        encr_val = exp_by_modulo(int_val, l, n)
        # print(encr_val)
        encr_block = int2ba(encr_val)
        # print("added len = ", encr_block_size, len(encr_block), encr_block)
        encr_block = ba('0' * (encr_block_size - len(encr_block))) + encr_block
        # print(encr_block, len(encr_block))
        print(f"encr_block={encr_block}, val={ba2int(encr_block)}")
        return encr_block

    def encrypt(self, message):
        l, n = self.open_keys
        block_size = math.floor(math.log2(n))
        # строку в битовую
        bin_mes = self.get_bin_string(message)
        print(f"Encryption: block_size={block_size}, message={message}")
        # добить строку до кратности нулями слева
        extra_block_size = len(bin_mes) % block_size
        added_len = block_size - extra_block_size
        if added_len != block_size:  # бессмысленно добавлять целый блок из нулей
            bin_mes = ba('0' * added_len) + bin_mes
        # print(len(bin_mes), bin_mes, len(bin_mes) % block_size)

        # так как дополнили слева. идем слева направо последовательно
        encrypted_blocks = [
            self._encrypt_block(l, n, bin_mes[i:i + block_size], block_size + 1, "encrypt") for i in
            range(0, len(bin_mes), block_size)
        ]
        # print(encrypted_blocks)
        encrypted = ba()
        for i in encrypted_blocks:
            encrypted.extend(i)
        return encrypted

    def decrypt(self, bin_mes):
        n, d = self.closed_keys
        block_size = math.floor(math.log2(n)) + 1
        print(f"Decryption: block_size={block_size}, message={bin_mes}")
        # print("decr", len(bin_mes), block_size, bin_mes)
        decrypted_blocks = [
            self._encrypt_block(d, n, bin_mes[i:i + block_size], block_size - 1, "decrypt") for i in
            range(0, len(bin_mes), block_size)
        ]
        print(decrypted_blocks)
        decrypted = ba()
        for i in decrypted_blocks:
            decrypted.extend(i)
        return decrypted

    def bitarray_to_text(self, arr):
        arr = copy.deepcopy(arr)
        if len(arr) % 8 != 0:
            arr.fill()

        byte_data = arr.tobytes()

        text = byte_data.decode('utf-8', errors='replace')
        text = text.lstrip('\x00')  # удаляю нулевый байты из текста
        text = text.rstrip('\x00')
        return text


if __name__ == '__main__':
    # ex 1
    # rsa = RSA(keys=(13, 21583, 1637))
    # enc = rsa.encrypt("CRYPTO")
    # print(enc)
    # print(rsa.bitarray_to_text(enc))
    # dec = rsa.decrypt(enc)
    # print(rsa.bitarray_to_text(dec))
    # ex 2
    rsa2 = RSA(keys=(13, 323, 133))
    message = "HASH"
    enc2 = rsa2.encrypt(message)
    print(enc2)
    print(rsa2.bitarray_to_text(enc2))
    dec2 = rsa2.decrypt(enc2)
    print(dec2)
    print(rsa2.bitarray_to_text(dec2))
