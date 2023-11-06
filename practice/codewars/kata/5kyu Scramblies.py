# Complete the function scramble(str1, str2) that returns true
# if a portion of str1 characters can be rearranged to match str2,
# otherwise returns false.
#
# Notes:
#
# Only lower case letters will be used (a-z). No punctuation or digits will be included.
# Performance needs to be considered.
# Examples
# scramble('rkqodlw', 'world') ==> True
# scramble('cedewaraaossoqqyt', 'codewars') ==> True
# scramble('katas', 'steak') ==> False


# def scramble(s1, s2):
#     for i in set(s2):
#         if s2.count(i) > s1.count(i):
#             return False
#     return True


# def scramble(s1, s2):
#     # all 判断是否所有元素都为真值
#     return all(s1.count(x) >= s2.count(x) for x in set(s2))


from collections import Counter


def scramble(s1, s2):
    return len(Counter(s2) - Counter(s1)) == 0


if __name__ == '__main__':
    a = scramble('tflqkgyyuvi', 'ykvv')
    print(a)
