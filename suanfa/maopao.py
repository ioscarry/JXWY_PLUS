def bubble_sort(alist):
    n = len(alist)
    for j in range(n-1):
        count = 0
        for i in range(n-1-j):
            if alist[i] > alist[i+1]:
                alist[i],alist[i+1] = alist[i+1],alist[i]
                count += 1
        if count == 0:
            break
        print(count)

if __name__ == '__main__':
    alist = [33,22,44,11,99,55]
    bubble_sort(alist)
    print(alist)