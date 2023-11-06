# Write an algorithm that takes an array and moves all of the zeros to the end,
# preserving the order of the other elements.
#
# move_zeros([1, 0, 1, 2, 0, 1, 3]) # returns [1, 1, 2, 1, 3, 0, 0]


# def move_zeros(lst):
#     new_lst = [i for i in lst if i]
#     return new_lst + [0 for _ in range(len(lst) - len(new_lst))]

def move_zeros(array):
    return sorted(array, key=lambda x: x == 0 and type(x) is not bool)


if __name__ == '__main__':
    a = move_zeros([1, 0, 1, 2, 0, 1, 3])
    print(a)
