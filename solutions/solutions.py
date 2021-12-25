### WEEK 1 ###

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


# Q5
def q5v1():
    stri = ""
    for i in range (6):
        stri += (str(i ** 2) + "\n")
    return stri

def q5v2():
    stri = ""
    for i in range (6):
        stri += (str(i ** 2))
    return stri

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


# Q9
def string_manipulation(string):  
    c = string[:3] 
    return c 

        

# Q10
def strings(a,b):
    c = a[-1] + b[-1]
    c = c.lower()
    return c


### WEEK 2 ###

# Q1
def minimum(lists): 
    minimum = lists[0] 
    for i in range(1, len(lists)): 
        if lists[i] < minimum: 
            minimum = lists[i] 
    return minimum 


# Q2
def sums(lists): 
    count = 0 
    for i in range(len(lists)): 
        count += lists[i] 
    return count 

# Q3
def unique(lists): 
    new_list = [] 
    for i in range(len(lists)): 
        if lists[i] not in new_list: 
            new_list.append(lists[i]) 
    return new_list

# Q4
def string_index(lists, string): 
    for i in range(len(lists)): 
        if lists[i] == string: 
            return i

# Q5
def elements(tuples): 
    stri = ""
    for i in range(len(tuples)): 
        if len(tuples[i]) > 3: 
            stri += (tuples[i] + "\n")
    return stri 

def elementsV2(tuples): 
    stri = ""
    for i in range(len(tuples)): 
        if len(tuples[i]) > 3: 
            stri += tuples[i]
    return stri 

# Q6
def letter_a(tuples): 
    stri = ""
    for i in range(len(tuples)): 
        if 'a' in tuples[i]: 
            stri += (tuples[i] + "\n")
    return stri

def letter_aV2(tuples): 
    stri = ""
    for i in range(len(tuples)): 
        if 'a' in tuples[i]: 
            stri += tuples[i]
    return stri

# Q7
def even_numbers(tuples):  
    new_list = [] 
    for i in range(len(tuples)): 
        if tuples[i] % 2 == 0: 
            new_list.append(tuples[i]) 
    return new_list 

# Q8
import math  
def square_root(lists): 
    new_list = [] 
    for i in range(len(lists)): 
        new_list.append(math.sqrt(lists[i])) 
    return new_list 

# Q9
def sets(set1, set2): 
    return set1.union(set2) 

# Q10
def remove_elements(set1, set2): 
    return set1.difference(set2) 