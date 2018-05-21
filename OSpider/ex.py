# -*- coding: utf-8 -*-


def is_palindrome(str):
    return str == str[::-1]


def is_response(num1, num2):
    num1 = str(num1)
    num2 = str(num2)
    if len(num1) != len(num2):
        return False
    i = 0
    j = len(num2) - 1
    # print(i, j)
    while j >= i:
        if num1[i] != num2[j]:
            return False
        i += 1
        j -= 1
    return True

def return_palindrome(num):
    return int(str(num)[::-1])

if __name__ == "__main__":
    # for i in range(100000, 1000000):
    #     if is_palindrome(str(i)[-4:]) and is_palindrome(str(i+1)[-5:]) \
    #             and is_palindrome(str(i+2)[-4:-1]) and is_palindrome(str(i+3)):
    #         print(i)
    dic = {}
    for i in range(1, 99):
        key = return_palindrome(i) - i
        if not dic.get(key):
            dic[key] = []
        dic[key].append([i, return_palindrome(i)])
    for key, value in dic.items():
        if len(value) == 8:
            print(value)
        else:
            print('这些不是：{}'.format(value))
