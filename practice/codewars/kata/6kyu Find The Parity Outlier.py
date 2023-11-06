# You are given an array (which will have a length of at least 3, but could be very large)
# containing integers. The array is either entirely comprised of odd integers or entirely comprised
# of even integers except for a single integer N. Write a method that takes the array as an argument
# and returns this "outlier" N.
#
# Examples
# [2, 4, 0, 100, 4, 11, 2602, 36] -->  11 (the only odd number)
#
# [160, 3, 1719, 19, 11, 13, -21] --> 160 (the only even number)


def find_outlier(integers):
    odd = None
    even = None
    final = None
    for i in integers:
        temp = i % 2
        if odd is not None and even is not None:
            return even if temp else odd
        if temp == 0:
            even = i
        else:
            odd = i
        final = i
    return final


if __name__ == '__main__':
    a = find_outlier([3, 1719, 19, 11, 13, -21, 160, ])
    print(a)
