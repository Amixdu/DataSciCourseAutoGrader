def q8v1():
    x = 0
    res = ""
    while x < 30:
        if x % 3 == 0:
            res += (str(x) + "\n")
            x += 2
        x += 2
    return res


def q8v2():
    x = 0
    res = ""
    while x < 30:
        if x % 3 == 0:
            res += str(x)
            x += 2
        x += 2
    return res