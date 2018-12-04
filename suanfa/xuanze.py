def selection_sort(alist):
    n = len(alist)
    for i in range(n-1):
        min_index = i
        # 从i+1位置到末尾选择出最小数据
        for j in range(i+1,n):
            if alist[j] < alist[min_index]:
                min_index = j

        # 如果选择出的数据不在正确位置, 进行交换
        if min_index != i:
            alist[i],alist[min_index] = alist[min_index],alist[i]

alist = [54,226,93,17,77,31,44,55,20]
selection_sort(alist)
print(alist)