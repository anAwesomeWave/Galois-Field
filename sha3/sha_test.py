import pytest
from bitarray import bitarray as ba
from main import SHA3


@pytest.mark.parametrize("byte_arr, r, ans", [
    (ba(), 3, ba('101')),
    (ba(), 2, ba('11')),
    (ba('1'), 2, ba('1101')),
    (ba("101"), 5, ba('10111')),
    (ba("1010"), 5, ba('1010100001')),
    (ba('100101'), 12, ba('100101100001')),
    ])
def test_padding(byte_arr, r, ans):
    sha = SHA3(0, r, 0)
    assert sha.padding(byte_arr) == ans


@pytest.mark.parametrize("byte_arr, r, ans", [
    (ba("101001"), 3, [ba('101'),ba('001')]),
    (ba("101001"), 6, [ba("101001")]),
    (ba("1010011010"), 2, [ba("10"), ba("10"), ba("01"), ba("10"), ba("10")]),
    ])
def test_split(byte_arr, r, ans):
    sha = SHA3(0, r, 0)
    assert sha.split_message(byte_arr) == ans


@pytest.mark.parametrize("b, r, parts, state, ans", [
    (4, 3, [ba("101"), ba('001')], ba('1101'), [ba('0110'), ba('1110')]),
    (5, 2, [ba("10"), ba('01')], ba('00000'), [ba('10000'), ba('01000')]),
    ])
def test_apply_state(b, r, parts, state, ans):
    sha = SHA3(b, r, 0)
    assert sha.apply_state(parts, state) == ans
