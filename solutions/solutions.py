# Q1
def positive_integer(x):
    if x > 0: 
        return True
    else:
        return False


# Q2
def multiples(x):
    return (x % 2 == 0 and x % 5 == 0)


# Q3
def product(x, y):
    return x**y


# Q4
def student_grade(x):
    if x >= 0 and x < 50:
        return("F")
    elif x >= 50 and x < 60:
        return("D")
    elif x >= 60 and x < 70:
        return("C")
    elif x >= 70 and x < 80:
        return("B")
    elif x >= 80 and x < 90:
        return("A")
    elif x >= 90 and x <= 100:
        return("A*")
    else:
        return("N")


# # Q5
# for i in range (6):
#     print(i ** 2)

# Q6
def odd_numbers():
    odd = 0
    for i in range(20):
        if i % 2 != 0:
            odd += 1
    return odd


# Q7
def loops(x):
    res = ""
    i = 0
    while i < x:
        res  += (str(i) + "\n")
        i += 4
    return res


def loopsV2(x):
    res = ""
    i = 0
    while i < x:
        res  += str(i)
        i += 4
    return res


# # Q8
# x = 0
# while x < 30:
#     if x % 3 == 0:
#         print(x)
#         x += 2
#     x += 2


# Q9
def string_manipulation():
    exercise = "The quick brown fox jumps over the lazy dog"
    a = exercise [4:9]
    b = exercise [16:19]
    c = a + " " + b
    return c

        

# Q10
def strings(a,b):
    c = a[-1] + b[-1]
    c = c.lower()
    return c