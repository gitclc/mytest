# Complete the solution so that it splits the string into pairs of two characters.
# If the string contains an odd number of characters then it should replace the missing
# second character of the final pair with an underscore ('_').
#
# Examples:
#
# * 'abc' =>  ['ab', 'c_']
# * 'abcdef' => ['ab', 'cd', 'ef']

# 将一个字符串切成两个字母一组的列表
# 如果字符串的长度为奇数，则将缺少的第二个字符替换为('_')


# def solution(s):
#

# 正则
# import re
#
#
# def solution(s):
#     return re.findall(".{2}", s + "_")


# 列表生成式
# def solution(s):
#     return [s[i:i+2] if i+2 <=len(s) else (s[i]+'_') for i in range(0,len(s),2)]
#
# def solution(s):
#     return [s[i:i + 2].ljust(2, '_') for i in range(0, len(s), 2)]
#
# def solution(s):
#     s+='_'
#     return[s[x:x+2] for x in range(0,len(s)-1,2)]


# 递归
# def solution(s):
#     if len(s) == 0:
#         return []
#     elif len(s) == 1:
#         return [s + "_"]
#     else:
#         return [s[:2]] + solution(s[2:])


#
# def solution(s):
#     return list(map(''.join, zip(*[iter(s + '_')] * 2)))

if __name__ == '__main__':
    # print(solution('ab'))

    pass
