# The problem
# How many zeroes are at the end of the factorial of 10? 10! = 3628800, i.e. there are 2 zeroes.
# 16! (or 0x10!) in hexadecimal would be 0x130777758000, which has 3 zeroes.
#
# Scalability
# Unfortunately, machine integer numbers has not enough precision for larger values.
# Floating point numbers drop the tail we need.
# We can fall back to arbitrary-precision ones - built-ins or from a library,
# but calculating the full product isn't an efficient way to find just the tail of a factorial.
# Calculating 100'000! in compiled language takes around 10 seconds.
# 1'000'000! would be around 10 minutes, even using efficient Karatsuba algorithm
#
# Your task
# is to write a function,
# which will find the number of zeroes at the end of (number) factorial in arbitrary radix = base for larger numbers.
#
# base is an integer from 2 to 256
# number is an integer from 1 to 1'000'000
# Note Second argument: number is always declared,
# passed and displayed as a regular decimal number.
# If you see a test described as 42! in base 20 it's 4210 not 4220 = 8210.

from collections import Counter


def prime(num):
    # 求质数
    prime_list = []
    for i in range(2, num + 1):
        is_prime = True
        for j in prime_list:
            if i / 2 < j:
                break
            if i % j == 0:
                is_prime = False
        if is_prime:
            prime_list.append(i)
            yield i


def factorization(num):
    # 因式分解
    result = []
    prime_num = [i for i in prime(num)]
    if num < 2 or num in prime_num:
        return [num]
    while True:
        for i in prime_num:
            if num % i == 0:
                num = num / i
                result.append(i)
        if num == 1:
            break
    return result


def zeroes(base, number):
    # 1.对base进行因式分解
    # 2.循环number,判断每个number的因子是否在base的因子列表中
    # 3.对所有的number因子进行计数并分组，一组base因子即为1个0
    base_cal = {}
    for i in prime(base):
        while True:
            if base % i == 0:
                base_cal[i] = base_cal.get(i, 0) + 1
                base = base / i
            else:
                break
        if base == 1:
            break
    number_cal = {}
    for i in range(1, number + 1):
        for j in base_cal:
            while True:
                if i % j == 0:
                    number_cal[j] = number_cal.get(j, 0) + 1
                    i = i / j
                else:
                    break
    return min(number_cal.get(i, 0) // base_cal[i] for i in base_cal)


if __name__ == '__main__':
    import time

    a = time.time()
    # print([i for i in prime(256)])
    print(zeroes(2, 42))
    # print(1 % 2)
    print(time.time() - a)
