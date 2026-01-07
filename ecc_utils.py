import random
from ecc_curve import double_add, P

def generate_private_key(min_value=1, max_value=1000):
   return random.randint(min_value, max_value)

def generate_public_key(private_key):
   return double_add(private_key, P)