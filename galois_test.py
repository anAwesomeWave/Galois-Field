from galois_field import GF

def test_div():
    assert GF(3, 3).poly_div([1, 1, 0, 2], [2]) == ([2, 2, 0, 1], [0])

    assert GF(2, 3).poly_div([1, 1, 0], [1, 1, 0]) == ([1], [0])

    assert GF(5, 3).poly_div([1, 1, 0, 0, 1, 1], [1, 1]) == ([1, 0, 0, 0, 1], [0])

    assert GF(2, 3).poly_div([1, 0, 0, 0], [1, 0, 1, 1]) == ([1], [1, 1])
