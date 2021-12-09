def q3(x):
    if x < 0: 
        f = open('test.txt', 'w+')
        f.write(str(x))
        return True
    else:
        return False


def q4(x):
    return (x % 2 == 0 and x % 5 == 0)
        