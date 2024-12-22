from galois_field import GF


def test_div():
    assert GF(3, 3).poly_div([1, 1, 0, 2], [2]) == ([2, 2, 0, 1], [0])

    assert GF(2, 3).poly_div([1, 1, 0], [1, 1, 0]) == ([1], [0])

    assert GF(5, 3).poly_div([1, 1, 0, 0, 1, 1], [1, 1]) == ([1, 0, 0, 0, 1], [0])

    assert GF(2, 3).poly_div([1, 0, 0, 0], [1, 0, 1, 1]) == ([1], [1, 1])

    assert GF(3, 3).poly_div([2, 2, 0, 1], [1, 0, 2, 1]) == ([2], [2, 2, 2])

    assert GF(3, 3).poly_div([2, 0, 2, 1], [1, 0, 2, 1]) == ([2], [1, 2])


def test_mult():
    assert GF(2, 3).poly_mult([0], [1, 1, 1, 1, 1, 0, 0]) == [0]
    assert GF(2, 3).poly_mult([1, 0], [1, 0, 0]) == [1, 1]
    assert GF(2, 3).poly_mult([1, 1, 0], [1, 1, 0]) == [1, 0]


def test_sum():
    assert GF(2, 3).poly_sum([0], [1, 1, 1, 1, 1, 0, 0]) == [1, 1, 1, 1, 1, 0, 0]
    assert GF(2, 3).poly_sum([1, 1, 1, 1, 1, 0, 0], [0]) == [1, 1, 1, 1, 1, 0, 0]
    assert GF(2, 3).poly_sum([1, 0], [1, 0, 0]) == [1, 1, 0]
    assert GF(2, 3).poly_sum([1, 0, 0], [1, 0, 0]) == [0]
    assert GF(3, 3).poly_sum([1, 1, 1], [1, 2, 1]) == [2, 0, 2]
