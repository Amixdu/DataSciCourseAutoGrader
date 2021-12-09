import json
import importlib
import sys

from solutions.Q4Sol import q4

gbl = globals()

gradeDictionary = {}

# mypath = "D:\\Projects\\PythonAutoGrading\\Test1\\uploads"
mypath = sys.argv[1]
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

fileNames = []
for file in onlyfiles:
    lst = file.split(".")
    fileName = lst[0]
    fileNames.append(fileName)

    # initialize points
    gradeDictionary[fileName] = 0




def testQ1(func, studName):
    from solutions.Q3Sol import q3 as answer

    res = ""

    if (func(50) == answer(50) and (func(1) == answer(1))):
        res += (studName + ": solution for Q3 is working <br>")
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += (studName + ": solution for Q3 is incorrect <br>")

    return res




def testQ2(func, studName):
    from solutions.Q4Sol import q4 as answer

    res = ""

    if (func(10) == answer(10) and func(2) == answer(2) and func(5) == answer(5)):
        res += (studName + ": solution for Q4 is working <br>")
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += (studName + ": solution for Q4 is incorrect <br>")

    return res



def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 


results = []
for f in fileNames:
    fileToImport = 'uploads.' + f
    testModule = importlib.import_module(fileToImport)

    q1Func = testModule.q3
    results.append(testQ1(q1Func, f))

    q2Func = testModule.q4
    results.append(testQ2(q2Func, f))

    results.append(f + " points: " + str(gradeDictionary[f]))
    results.append("<br><br>")



print(listToString(results))








# print(fileNames)

# from uploads.personA import positive as attemptA
# from uploads.personB import positive as attemptB


# from solutions.Q1Sol import positive as answer

# res = ""

# if (attemptA(50) == answer(50)):
#     res += ("Person A's solution is working <br>")
# else:
#     res += ("Person A's solution is incorrect, the output for 1 should be True <br>")



# if (attemptB(50) == answer(50)):
#     res += ("Person B's solution is working <br>")
# else:
#     res += ("Person B's solution is incorrect, the output for 1 should be True <br>")

# print(res)

# print(onlyfiles)

