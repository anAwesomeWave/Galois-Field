from galois_field import GF
import numpy as np

print(GF(3, 3).poly_div([1, 1, 0, 2], [2]))  # [2, 2, 0, 1], [0]
print(np.polydiv([1, 1, 0, 2], [2]))

print("---------")
print(GF(2, 3).poly_div([1, 1, 0], [1, 1, 0]))  # [1], [0]
print(np.polydiv([1, 1, 0], [1, 1, 0]))

print("---------")
print(GF(5, 3).poly_div([1, 1, 0, 0, 1, 1], [1, 1]))  # [1, 0, 0, 0, 1]
print(np.polydiv([1, 1, 0, 0, 1, 1], [1, 1]))
print("---------")

print(GF(2, 3).poly_div([1, 0, 0, 0], [1, 0, 1, 1]))
print(np.polydiv([1, 0, 0, 0], [1, 0, 1, 1]))
print("---------")
