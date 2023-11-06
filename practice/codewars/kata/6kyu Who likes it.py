# You probably know the "like" system from Facebook and other pages. People can "like" blog posts,
# pictures or other items. We want to create the text that should be displayed next to such an item.
#
# Implement the function which takes an array containing the names of people that like an item.
# It must return the display text as shown in the examples:
#
# []                                -->  "no one likes this"
# ["Peter"]                         -->  "Peter likes this"
# ["Jacob", "Alex"]                 -->  "Jacob and Alex like this"
# ["Max", "John", "Mark"]           -->  "Max, John and Mark like this"
# ["Alex", "Jacob", "Mark", "Max"]  -->  "Alex, Jacob and 2 others like this"


def likes(names):
    # your code here
    fun_map = {
        0: ('no one', 's'),
        1: ('{}', 's'),
        2: ('{} and {}', ''),
        3: ('{}, {} and {}', ''),
        4: ('{}, {} and {other} others', '')
    }
    p, l = fun_map[min(4, len(names))]
    return f'{p.format(*names[:3], other=len(names[2:]))} like{l} this'


if __name__ == '__main__':
    a = ['a', 'b', 'c', 'd']
    print(likes(a))
