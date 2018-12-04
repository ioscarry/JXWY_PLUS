def primes(n):
    P = []
    f = [] # [0,0,0,0.....]
    for i in range(n+1):
        if i > 2 and i%2 == 0:
            f.append(1) #遍历处理从3开始,标记为1意为非质数
        else:
            f.append(0) # 标记为0意为待挖掘质数
    print(f)
    print(len(f))

    i = 3
    # 如果现在这个序列中最大数小于最后一个标出的素数的平方，那么剩下的序列中所有的数都是素数
    while i*i <= n:  # 当不满足序列中都是素数时
        if f[i] == 0:    # i=3对应f列表中的第4个数, 由于第一个是0,因此其实对应的还是3在f中的值(0或1)
            j = i*i
            while j <= n:
                f[j] = 1  # 由于j是平方取值, 因此判为非质数.标记为1
                j += i+i
        i += 2

    P.append(2)
    for x in range(3,n+1,2):
        if f[x] == 0:
            P.append(x)

    return P

n = 100
P = primes(n)
print(P)
