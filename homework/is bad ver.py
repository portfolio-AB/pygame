import random


def generate_number(left, right):
    return random.randint(left, right)


n = 10
BAD_VERSION = generate_number(1, n)


def is_bad_version(guess):
    global BAD_VERSION
    return guess >= BAD_VERSION


def first_bad_ver(n):
    left = 1
    right = n
    middle = n // 2
    while True:
        if is_bad_version(middle):
            right = middle
        elif not is_bad_version(middle):
            left = middle
        middle = (left + right) // 2
        if middle == left or middle == right:
            return right


print(first_bad_ver(n))
print(BAD_VERSION)
