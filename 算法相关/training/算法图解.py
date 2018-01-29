# -*- coding: utf-8 -*-
"""算法图解书上的练习"""


# 递归计算阶乘
# def fact(x):
#     return x if x == 1 else x * fact(x-1)
#
# print(fact(5))


# 斐波那契 尾递归
# def fib(x):
#     def fibonacci(num, res, temp):
#         if num == 0:
#             return res
#         else:
#             print(res)
#             return fibonacci(num-1, temp, res+temp)
#     return fibonacci(x, 0, 1)
#
# print(fib(5))

# fib = lambda n: 1 if n <= 2 else fib(n-1)+fib(n-2)

# 递归计算列表和
# def my_sum(l):
#     if l == []:
#         return 0
#     else:
#         return l[0] + my_sum(l[1:])
#
# l = [1, 2, 3]
# print(my_sum(l))

# def count(list):
#     if list == []:
#         return 0
#     else:
#         return 1 + count(list[1:])
#
# L = [i for i in range(1, 21)]
# print(count(L))


# 二分查找
# def two_search(list, target):
#     list.sort()
#     min = 0
#     max = len(list)
#     mid = len(list) // 2
#     if list[mid] == target:
#         return list[mid]
#     else:
#         return two_search(list[mid:], target) if target > list[mid] \
#             else two_search(list[:mid], target)
#
# print(two_search(L, 17))

L = [2,6,8,13,15,17,17,18,19,20]

# # 快速排序
# def quicksort(list):
#     if len(list) < 2:
#         return list
#     else:
#         pivot = list[0]
#         less = [i for i in list[1:] if i <= pivot]
#         greater = [i for i in list[1:] if i > pivot]
#         return quicksort(less) + [pivot] + quicksort(greater)

# print(quicksort(L))


# def sortIntegers(A):
#     # write your code here
#     def find_min_index(list):
#         min = list[0]
#         index = 0
#         for i in range(1, len(list)):
#             if list[i] < min:
#                 min = list[i]
#                 index = i
#         print(list[index])
#         return index
#
#     new_arr = []
#     for i in range(len(A)):
#         min = find_min_index(A)
#         new_arr.append(A.pop(min))
#     return new_arr
#
# print(sortIntegers(L))

# def naive_match(s, p):
#     m = len(s)
#     n = len(p)
#     for i in range(m-n+1):#起始指针i
#         if s[i:i+n] == p:
#             return i
#     return -1
#
# naive_match('abcsds', 'cs')

def binarySearch(nums, target):
    # write your code here
    min = 0
    max = len(nums) - 1
    if nums is None or target is None:
        return -1

    def search(min, max):
        while max >= min:
            mid = (max + min) // 2
            if nums[mid] == target:
                if mid - min > 0:
                    se = search(min, mid)
                    return mid if se is None else se
                else:
                    return mid
            if target > nums[mid]:
                min = mid + 1
            else:
                max = mid - 1
        return 0

    return search(min, max)


L = [2,2,3,4,5,6,8,13,17,18]


print(binarySearch(L, 17))




