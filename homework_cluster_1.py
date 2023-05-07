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
#
# a = [2, 3, 4 ,7, 11, 13]
#
#
# def two_sum(lst, target):
#     for i in range(len(lst)):
#         for h in range(i, len(lst)):
#             if target - lst[i] == lst[h]:
#                 return i + 1, h + 1
#
#
# # print(two_sum(a, 10))
#
#
# def two_sum_ver2(lst, target):
#     left = 0
#     right = len(lst) - 1
#     while left < right:
#         if lst[left] + lst[right] == target:
#             return left + 1, right + 1
#         elif lst[left] + lst[right] > target:
#             right -= 1
#         elif lst[left] + lst[right] < target:
#             left += 1
#
#
# print(two_sum_ver2(a, 10))
# -------------------------------------
# a = [-4, -1, 0, 3, 10]
#
# for i in range(len(a)):
#     a[i] **= 2
#
# a = sorted(a)
# print(a)

# -------------------------------------

# a = [-4, -1, 0, 3, 10]
# res = [0] * len(a)
#
# left = 0
# right = len(a) - 1
# current_i = len(a) - 1
#
# while left <= right:
#     left_val = a[left] ** 2
#     right_val = a[right] ** 2
#
#     if left_val >= right_val:
#         res[current_i] = left_val
#         left += 1
#     if left_val <= right_val:
#         res[current_i] = right_val
#         right -= 1
#     current_i -= 1
#
# print(res)

# ----------------------------------------

# eg = "Let's take LeetCode contest"
#
#
# def reverse_str(s):
#     words = s.split(" ")
#     rev_words = ""
#
#     for w in words:
#         i = len(w)
#         while i > 0:
#             i -= 1
#             rev_words += w[i]
#         rev_words += " "
#     return rev_words
#
#
# print(reverse_str(eg))

# ----------------------------------------
# num_lst = [0, 1, 0, 3, 12]
#
#
# def zero_finder(nl):
#     last_zero = 0
#     for i in range(len(nl)):
#         if nl[i] != 0:
#             nl[last_zero], nl[i] = nl[i], nl[last_zero]
#             last_zero += 1
#
#     return nl
#
#
# print(zero_finder(num_lst))
