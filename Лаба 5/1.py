import random
import string

def password_generator(length=8):
    chars = random.choices(string.ascii_letters + string.digits, k=length)
    password = ''.join(chars)
    inverted_password = ''.join(map(lambda c: c.swapcase(), password))
    return inverted_password

for x in range(5):
    print(password_generator())
