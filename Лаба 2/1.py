from itertools import *
def count_comb():
    c = 0
    for w in product('ГЕПАРД', repeat=5):
        if w.count('Г')==1 and w[0]!='А' and w[-1]!='Е':
            c += 1
    return c
result = count_comb()
print(result)





