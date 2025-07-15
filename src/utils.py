import random
import string

def generate_random_string(length=8):
    """Generate a random alphanumeric string of given length."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def string_to_int_seed(s):
    """Convert a string to an integer seed deterministically."""
    return abs(hash(s)) % (2**32)  # Limit to 32-bit positive integer