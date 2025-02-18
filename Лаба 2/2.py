def count_four():
    N = 5**36 + 5**24 - 25
    c = 0
    while N > 0:
        if N % 5 == 4:
            c += 1
        N //= 5
    return(c)
redult = count_four()
print(result)
