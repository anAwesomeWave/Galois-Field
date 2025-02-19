import pytest
import bitarray
from main import SHA3


@pytest.mark.parametrize("byte_arr, r, ans", [
    (bitarray.bitarray(), 3, bitarray.bitarray('101')),
    (bitarray.bitarray(), 2, bitarray.bitarray('11')),
    (bitarray.bitarray('1'), 2, bitarray.bitarray('1101')),
    (bitarray.bitarray("101"), 5, bitarray.bitarray('10111')),
    (bitarray.bitarray("1010"), 5, bitarray.bitarray('1010100001')),
    (bitarray.bitarray('100101'), 12, bitarray.bitarray('100101100001')),
    ])
def test_padding(byte_arr, r, ans):
    sha = SHA3(0, r, 0)
    assert sha.padding(byte_arr) == ans


@pytest.mark.parametrize("byte_arr, r, ans", [
    (bitarray.bitarray("101001"), 3, [bitarray.bitarray('101'),bitarray.bitarray('001')]),
    (bitarray.bitarray("101001"), 6, [bitarray.bitarray("101001")]),
    (bitarray.bitarray("1010011010"), 2, [bitarray.bitarray("10"), bitarray.bitarray("10"), bitarray.bitarray("01"), bitarray.bitarray("10"), bitarray.bitarray("10")]),
    ])
def test_split(byte_arr, r, ans):
    sha = SHA3(0, r, 0)
    assert sha.split_message(byte_arr) == ans