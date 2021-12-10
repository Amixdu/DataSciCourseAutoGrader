import json
import importlib
import sys

from solutions.Q4Sol import q4

gbl = globals()

NUMBER_OF_QUESTIONS = 2

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

    fileArr = fileName.split('_')

    # initialize points
    gradeDictionary[fileArr[0]] = 0




def testQ1(func, fileName):
    from solutions.Q3Sol import q3 as answer

    fileArr = fileName.split('_')
    studentName = fileArr[0]

    res = ""

    if (func(50) == answer(50) and (func(1) == answer(1))):
        res += (studentName + ": solution for Q3 is working <br>")
        gradeDictionary[studentName] = gradeDictionary[studentName] + 1
    else:
        res += (studentName + ": solution for Q3 is incorrect <br>")

    return res




def testQ2(func, fileName):
    from solutions.Q4Sol import q4 as answer

    fileArr = fileName.split('_')
    studName = fileArr[0]

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

from inspect import getmembers, isfunction

question = 3
results = []
for f in fileNames:
    # CHECK PATH
    fileToImport = 'uploads.' + f
    testModule = importlib.import_module(fileToImport)

    functionName = (getmembers(testModule, isfunction)[0][0])
    # y = testModule.__name__
    # print(y)
    
    # q3Func = testModule.q3
    # q4Func = testModule.q4
    func = getattr(testModule, functionName)

    
    fileArr = f.split('_')



    if (fileArr[1] == "Q3"):
        results.append(testQ1(func, f))
        

    if (fileArr[1] == "Q4"):
        results.append(testQ2(func, f))


    


results.append("<br><br>Sores: <br>")

students = [(file.split('_')[0]) for file in fileNames]
studentsUnique = list(dict.fromkeys(students))

for student in studentsUnique:
    results.append(student + " score: <strong>" + str((gradeDictionary[student]/NUMBER_OF_QUESTIONS)*100) + "%</strong>")
    results.append("<br>")



   




print(listToString(results))
