from hashlib import pbkdf2_hmac
from hmac import compare_digest
from secrets import token_bytes


def _digest(password, salt):
    return pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 600_000).hex()


def hash_password(password):
    salt = token_bytes(16)
    return f"{salt.hex()}${_digest(password, salt)}"


def verify_password(password, stored_hash):
    if not isinstance(stored_hash, str):
        return False
    salt_hex, separator, expected = stored_hash.partition("$")
    if not separator or len(salt_hex) != 32 or len(expected) != 64:
        return False
    try:
        salt = bytes.fromhex(salt_hex)
    except ValueError:
        return False
    return expected.isascii() and compare_digest(_digest(password, salt), expected)
