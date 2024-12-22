import pytest

from affine import Affine
from galois_field import GF


@pytest.mark.parametrize("p, n", [
    (p, n) for p in [2, 3] for n in range(8, 11)
] + [
    (p, n) for p in [5, 7] for n in range(4, 7)
])
def test_encryption(p, n):
    text = """In cryptography, ciphertext or cyphertext is the result of encryption 
    performed on plaintext using an algorithm, called a cipher.
     Ciphertext is also known as encrypted or encoded information because it contains a form of the 
     original plaintext that is unreadable by a human or computer without the proper cipher to decrypt it. 
     This process prevents the loss of sensitive information via hacking. 
     Decryption, the inverse of encryption, is the process of turning ciphertext into readable plaintext. 
    Ciphertext is not to be confused with codetext because the latter is a result of a code, not a cipher.
    """
    aff = Affine(p, n, GF(p, n))
    assert aff.decrypt(aff.encrypt(text)) == text
