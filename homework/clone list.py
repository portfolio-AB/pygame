x = [1, 2, 3]


# def clone(my_list):
#     lst = []
#     for i in my_list * 2:
#         lst.append(i)
#
#     return lst

def clone(my_list):
    for i in range(len(my_list)):
        my_list.append(my_list[i])

    return my_list


print(clone(x))
