import random
import string

def password_generator(length=8):
    for x in range(5):
        chars = random.choices(string.ascii_letters + string.digits, k=length)
        password = ''.join(chars)
        yield password

passwords = map(lambda p: ''.join(c.swapcase() for c in p), password_generator())

for password in passwords:
    print(password)
