# Example keygen for generating keys for the Flask app

# Security:
# secrets.token_hex and os.urandom are designed specifically for cryptographic use, making them more suitable for generating secure secret keys.
# uuid.uuid4() is not designed for cryptographic use. While it produces random values, it may not be as suitable for cryptographic purposes as the other methods.

# Usage:
# secrets.token_hex and os.urandom are more commonly used for generating secret keys due to their cryptographic nature.
# uuid.uuid4() is more commonly used for generating unique identifiers rather than secret keys.


# Using secrets to generate a key
import secrets # python 3.6+
def generate_key(length: int = 32) -> str:
    return secrets.token_hex(length)

# Using os.urandom to generate a key
import os
def generate_key(length: int = 32) -> str:
    return os.urandom(length).hex()

# Using uuid.uuid4 to generate a key
import uuid
def generate_key() -> str:
    return uuid.uuid4().hex
