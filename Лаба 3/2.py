import math

def calculate_sqrt_no(n):
    result = 0
    for _ in range(n):
        result = math.sqrt(3 + result)
    return result



def calculate_sqrt_yes(n):
    if n == 0:
        return 0
    return math.sqrt(3 + calculate_sqrt_yes(n - 1))

n = int(input("Введите количество корней: "))
print(calculate_sqrt_yes(n))
print( calculate_sqrt_no(n))
