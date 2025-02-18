def find_eight():
    n = 500000
    cnt = 0
    while cnt < 5:
        for factor in range(18, n//2+1):
            if n%factor == 0 and str(factor)[-1] == '8':
                print(n, factor)
                cnt += 1
                break
        n += 2
find_eight()

