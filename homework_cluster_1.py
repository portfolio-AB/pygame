# n = int(input("positive intiger"))
# nums = "1"
# for i in range(2, n + 2, 2):
#     print(nums)
#     nums += str(i) + str(i + 1)

# ----------------------------------

# n = int(input("how many squares?"))
# dashes = 0
# nums = 2
#
# for _ in range(n):
#     print("-" * dashes + str(nums))
#     dashes = nums
#     nums = nums**2

# ----------------------------------
# string_eg = "jkjk"
# non_rep_max = 0
# streak = {}
# current_alpha = 0
#
# for i in string_eg:
#     res = streak.get(i, 0)
#     if res != 0:
#         if current_alpha > non_rep_max:
#             non_rep_max = current_alpha
#         current_alpha = 0
#         streak = {}
#
#     streak[i] = 1
#     current_alpha += 1
#
# if current_alpha > non_rep_max:
#     non_rep_max = current_alpha
#
# print(non_rep_max)

# -------------------------------------

a = [2, 3, 4 ,7, 11, 13]


def two_sum(lst, target):
    for i in range(len(lst)):
        for h in range(i, len(lst)):
            if target - lst[i] == lst[h]:
                return i + 1, h + 1


# print(two_sum(a, 10))


def two_sum_ver2(lst, target):
    left = 0
    right = len(lst) - 1
    while left < right:
        if lst[left] + lst[right] == target:
            return left + 1, right + 1
        elif lst[left] + lst[right] > target:
            right -= 1
        elif lst[left] + lst[right] < target:
            left += 1


print(two_sum_ver2(a, 10))
