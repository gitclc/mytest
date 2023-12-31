# The marketing team is spending way too much time typing in hashtags.
# Let's help them with our own Hashtag Generator!
#
# Here's the deal:
#
# It must start with a hashtag (#).
# All words must have their first letter capitalized.
# If the final result is longer than 140 chars it must return false.
# If the input or the result is an empty string it must return false.
# Examples
# " Hello there thanks for trying my Kata"  =>  "#HelloThereThanksForTryingMyKata"
# "    Hello     World   "                  =>  "#HelloWorld"
# ""                                        =>  false


# def generate_hashtag(s):
#     result = ''.join([i[0].upper() + i[1:].lower() for i in s.split(' ') if i])
#     if len(result) > 139 or len(result) == 0:
#         return False
#     return '#' + result


def generate_hashtag(s):
    output = "#"
    for word in s.split():
        output += word.capitalize()

    return False if (len(s.split()) == 0 or len(output) > 140) else output


if __name__ == '__main__':
    a = generate_hashtag('  ')
    print(a)
