x = "abde"


# def how_many_clicks(txt):
#     click_val = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11, "l": 12,
#                  "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, "t": 20,
#                  "u": 21, "v": 22, "w": 23, "x": 24, "y": 25, "z": 26}
#     total_clicks = 0
#
#     for i in range(len(txt)):
#         if txt[i] in click_val:
#             total_clicks += click_val[txt[i]]
#
#     return total_clicks

def how_many_clicks(txt):
    total_clicks = 0
    alpha = "abcdefghijklmnopqrstuvwxyz"
    click_val = {}
    for i in range(len(alpha)):
        click_val[alpha[i]] = i + 1

    for i in range(len(txt)):
        if txt[i] in click_val:
            total_clicks += click_val[txt[i]]

    return total_clicks


print(how_many_clicks(x))
