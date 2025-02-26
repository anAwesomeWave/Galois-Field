import math

from bitarray import bitarray as ba

'''

b – размер состояния (обычно 1600 бит). для sha3
r – скорость (rate).
c – емкость (capacity), при этом r + c = b.

sha-3 (r + c = 1600 = b )
sha3-256 (r = 1088, c=512

KECCAK-p[1600, 24] =KECCAK-f[1600]. (nr = 12 + 2l = 24)

'''


class SHA3:
    def __init__(self, b=1600, r=1088):
        self.b = b  # size of state
        self.r = r
        self.w = self.b // 25  # size of state row (if we imagine state as a matrix 5x5xw)
        self.d = 256  # sha3-256 - 256 извлекаем из функции sponge
        self.l = int(math.log(1600/25, 2))  # log2(b/25) = log2(w)
        self.nr = 12 + 2 * self.l  # kecaak number of rounds

    def padding(self, message_len: int) -> ba:
        # шаг 1
        # pad10*1, 1 + 0*r + 1
        # добавим 1 000000 (r) 1 бит
        # len(bytes) % r = k
        # if k = 0 -> k = r
        # k - сколько бит надо добавить
        # 1 << (k-1), т.к. 1 уже занимает 1 позицию,
        # padding = 1 << (k-1)
        # padding.extend(0b1)
        pad_len = (-message_len - 2) % self.r
        # if pad_len == 0:
        #     pad_len = self.r
        padding_bits = ba('1' + '0' * pad_len + '1', endian='little')
        return padding_bits

    def split_message(self, message_bits: ba) -> list[ba]:
        # шаг 2
        # n * r = len(message_bits), n - кол-во частей
        # n * r = len(^) = r * k, так как после дополнения длина кратна r
        # берем по r бит каждый раз.

        parts = []
        for i in range(0, len(message_bits), self.r):
            parts.append(message_bits[i:i + self.r])
        return parts

    # def apply_state(self, part: ba, state: ba) -> ba:
    #     xor_part = (part ^ state[:self.r])
    #     xor_part.extend(ba('0' * (self.b - self.r)))
    #     return xor_part

    def sponge(self, P: ba) -> ba:
        # 1
        P.extend(self.padding(len(P)))
        # 2
        n = len(P) // self.r
        # 3
        c = self.b - self.r
        # 4 (split)
        parts = []
        for i in range(0, len(P), self.r):
            parts.append(P[i:i + self.r])

        # 5
        state = ba('0' * self.b, endian='little')

        # 6
        for i in range(n):
            parts[i].extend('0' * c)
            state = self.kecaak(state ^ parts[i])

        # 7
        z = ba(endian='little')
        # 8
        while True:
            z.extend(state[:self.r])
            # 9
            if self.d <= len(z):
                return z[:self.d]
            # 10
            state = self.kecaak(state)
        # parts = self.split_message(bits)
        # for part in parts:
        #     state = self.apply_state(part, state)
        #
        #

    def kecaak(self, state: ba) -> ba:
        def Rnd(cur_state: ba, cur_ir: int) -> ba:
            return self.iota(self.chi(self.pi(self.rho(self.theta(cur_state)))), cur_ir)

        for ir in range(12 + 2 * self.l - self.nr, 12 + 2 * self.l):
            state = Rnd(state, ir)

        return state

    def theta(self, state: ba) -> ba:
        """
            1. для всех пар C[x, z] {x=0,1,2,3,4, z = 0,1,...,w-1} = state[x,0,z] xor state[x,1,z] xor state[x,2,z] xor state[x,3,z] xor state[x,4,z]
            2. для всех пар D[x, z] {x=0,1,2,3,4, z = 0,1,...,w-1} = C[(x-1)%5, z] xor C[(x+1)%5, (z-1) % w]
            3. для всех x=0,...,4; y=0,...,4; z=0,...,w-1; state[x, y, z] = state[x, y, z] xor D[x,z]
        """
        # 1
        C = [[0 for _ in range(self.w)] for _ in range(5)]
        for i in range(5):  # x
            for j in range(self.w):  # z
                # state[x,y,z] = state[w(5y+x)+z]
                C[i][j] = state[self.w * i + j] ^ state[self.w * (5 + i) + j] ^ state[self.w * (10 + i) + j] ^ state[
                    self.w * (15 + i) + j] ^ state[self.w * (20 + i) + j]
        # 2
        D = [[0 for _ in range(self.w)] for _ in range(5)]
        for i in range(5):  # x
            for j in range(self.w):  # z
                # state[x,y,z] = state[w(5y+x)+z]
                D[i][j] = C[(i - 1) % 5][j] ^ C[(i + 1) % 5][(j - 1) % self.w]
        state2 = ba('0' * self.b, endian='little')
        for i in range(5):  # x
            for j in range(5):  # y
                for k in range(self.w):  # z
                    state2[self.w * (5 * j + i) + k] = state[self.w * (5 * j + i) + k] ^ D[i][k]
        return state2

    def rho(self, state: ba) -> ba:
        """
            1. z=0,1,2,...,w-1: State2[0,0,z] = State[0,0,z]
            2. x = 1, y = 0
            3. for t = 0, 1, ..., 23:
            3.1     z = 0,1,..., w-1: State2[x,y,z] = State[x, y, (z–(t+1)(t+2)//2) mod w]
            3.2     x = y, y = (2x_prev + 3y_prev) % 5
            return State2
        """
        # 1
        state2 = ba('0' * self.b, endian='little')
        for k in range(self.w):
            state2[k] = state[k]

        # 2
        x = 1
        y = 0
        for t in range(24):
            for z in range(self.w):
                z2 = (z - (t + 1) * (t + 2) // 2) % self.w
                state2[self.w * (5 * y + x) + z] = state[self.w * (5 * y + x) + z2]

            x, y = y, (2 * x + 3 * y) % 5
        return state2

    def pi(self, state: ba) -> ba:
        """
            1. all x,y,z state2[x, y, z] = state[(x + 3y) % 5, x, z]
            2. return state2
        """
        state2 = ba('0' * self.b, endian='little')
        for x in range(5):
            for y in range(5):
                for z in range(self.w):
                    x2 = (x + 3 * y) % 5
                    state2[self.w * (5 * y + x) + z] = state[self.w * (5 * x + x2) + z]
        return state2

    def chi(self, state: ba) -> ba:
        """
        1.  for all x, y, z: state2[x, y, z] = state[x, y, z] ^ ((state[(x + 1) % 5, y , z] ^ 1) & state[(x+2) % 5, y, z])
        2. return state2
        """
        state2 = ba('0' * self.b, endian='little')
        for x in range(5):
            for y in range(5):
                for z in range(self.w):
                    x2 = (x + 1) % 5
                    x3 = (x + 2) % 5
                    state2[self.w * (5 * y + x) + z] = state[self.w * (5 * y + x) + z] ^ (
                            (state[self.w * (5 * y + x2) + z] ^ 1) & state[self.w * (5 * y + x3) + z])
        return state2

    def rc_f(self, t: int) -> int:
        if t % 255 == 0:
            return 1
        R = list("10000000")
        for i in range(1, t % 255 + 1):
            R = list("0") + R
            R = list(R)
            R[0] = str(int(R[0]) ^ int(R[8]))
            R[4] = str(int(R[4]) ^ int(R[8]))
            R[5] = str(int(R[5]) ^ int(R[8]))
            R[6] = str(int(R[6]) ^ int(R[8]))
            R = R[0:8]
        return int(R[0])

    def iota(self, state: ba, ir: int) -> ba:
        """
            1. for all x, y, z: state2[x, y, z] = state[x, y, z]
            2. rc = '0' * self.w
        """

        # 1
        state2 = state.copy()

        # 2
        rc = ba('0' * self.w, endian='little')
        for j in range(self.l + 1):
            rc[2 ** j - 1] = self.rc_f(j + 7 * ir)

        for z in range(self.w):
            state2[z] = state[z] ^ rc[z]
        return state2


def calc_hash(filepath):
    with open(filepath, 'r') as f:
        data = ba(endian='little')
        print(data.endian())
        data.frombytes(bytes(f.read(), 'utf-8'))
        data.extend("01")
        sha = SHA3()
        hash = sha.sponge(data)
        # print(hash)
        byte_array = hash.tobytes()
        hex_string = byte_array.hex()
        print(hex_string)
        return hex_string


def write_hash(filepath):
    f2 = open("out.txt", "w")
    f2.write(calc_hash(filepath))


def integrity(filepath):
    print(calc_hash(filepath))
    print(open("out.txt").read())
    return calc_hash(filepath) == open("out.txt").read()


if __name__ == '__main__':
    option = int(input("What you want to do? (1 - calculate hash, 2 - check the integrity)"))
    filepath = input('Enter the file:')
    if option == 1:
        write_hash(filepath)
    else:
        if integrity(filepath):
            print("the file passed integrity check")
        else:
            print("file corrupted")
