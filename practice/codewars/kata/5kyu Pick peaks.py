# In this kata, you will write a function that returns the positions and the values of the "peaks"
# (or local maxima) of a numeric array.
#
# For example, the array arr = [0, 1, 2, 5, 1, 0] has a peak at position 3 with a value of 5 (since arr[3] equals 5).
#
# The output will be returned as an object with two properties:
# pos and peaks. Both of these properties should be arrays.
# If there is no peak in the given array, then the output should be {pos: [], peaks: []}.
#
# Example: pickPeaks([3, 2, 3, 6, 4, 1, 2, 3, 2, 1, 2, 3]) should return
# {pos: [3, 7], peaks: [6, 3]} (or equivalent in other languages)
#
# All input arrays will be valid integer arrays
# (although it could still be empty), so you won't need to validate the input.
#
# The first and last elements of the array will not be considered as peaks
# (in the context of a mathematical function,
# we don't know what is after and before and therefore, we don't know if it is a peak or not).
#
# Also, beware of plateaus !!! [1, 2, 2, 2, 1] has a peak while [1, 2, 2, 2, 3] and [1, 2, 2, 2, 2] do not.
# In case of a plateau-peak, please only return the position and value of the beginning of the plateau.
# For example: pickPeaks([1, 2, 2, 2, 1]) returns {pos: [1], peaks: [2]} (or equivalent in other languages)
#
# Have fun!

"""
flag:
    0:判断是否上升，上升的话可能为顶点，更新顶点索引，flag -> 1;
    1:已上升，判断是否下降，上升更新索引，等于不更新顶点索引，flag不变，下降flag -> 0
"""


#
# def pick_peaks(arr):
#     res = {'pos': [], 'peaks': []}
#     flag = 0
#     peak_index = None
#
#     def inner(n1, n2):
#         nonlocal flag
#         nonlocal res
#         nonlocal peak_index
#         _, n1 = n1
#         index2, n2 = n2
#         if flag == 0:
#             if n1 < n2:
#                 peak_index = index2
#                 flag = 1
#         elif flag == 1:
#             if n1 > n2:
#                 res['pos'].append(peak_index)
#                 res['peaks'].append(n1)
#                 flag = 0
#             elif n1 < n2:
#                 peak_index = index2
#
#     arr = list(enumerate(arr))
#     l = len(arr)
#     for i in range(l - 1):
#         inner(arr[i], arr[i + 1], )
#     return res

# import re
#
#
# def pick_peaks(arr):
#     slope = "".join("u" if b > a else "d" if a > b else "p" for a, b in zip(arr, arr[1:]))
#     print(slope)
#     positions = [m.start() + 1 for m in re.finditer(r"up*d", slope)]
#     peaks = [arr[pos] for pos in positions]
#     return {"pos": positions, "peaks": peaks}


def pick_peaks(arr):
    pos = []
    prob_peak = False
    for i in range(1, len(arr)):
        if arr[i] > arr[i - 1]:
            prob_peak = i
        elif arr[i] < arr[i - 1] and prob_peak:
            pos.append(prob_peak)
            prob_peak = False
    return {'pos': pos, 'peaks': [arr[i] for i in pos]}


if __name__ == '__main__':
    a = pick_peaks([3, 2, 3, 6, 4, 1, 2, 3, 3, 3, 3, 2, 1, 2, 3])
    print(a)
