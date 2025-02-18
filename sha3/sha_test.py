import pytest
import bitarray
from main import SHA3


@pytest.mark.parametrize("byte_arr, r, ans", [
    (bitarray.bitarray(), 3, bitarray.bitarray('101')),
    (bitarray.bitarray(), 2, bitarray.bitarray('11')),
    (bitarray.bitarray('1'), 2, bitarray.bitarray('1101')),
    (bitarray.bitarray('100101'), 12, bitarray.bitarray('100101100000000000000001')),
    ])
def test_padding(byte_arr, r, ans):
    sha = SHA3(0, r, 0)
    assert sha.padding(byte_arr) == ans
