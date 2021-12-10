import json
import importlib
import sys
from inspect import getmembers, isfunction

gbl = globals()

NUMBER_OF_QUESTIONS = 2

gradeDictionary = {}
questionDictionary = {}

# mypath = "D:\\Projects\\PythonAutoGrading\\Test1\\uploads"
mypath = sys.argv[1]
# question = "q3"
question = sys.argv[2]

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

    questionDictionary[file] = ""




def testQ3(func, fileName):
    from solutions.Q3Sol import q3 as answer

    fileArr = fileName.split('_')
    studentName = fileArr[0]

    res = ""

    if (func(50) == answer(50) and (func(1) == answer(1))):
        res += ("Q3 is correct <br>")
        questionDictionary[fileName] = "Solution for Q3 is correct <br>"
        gradeDictionary[studentName] = gradeDictionary[studentName] + 1
    else:
        res += ("Q3 is incorrect <br>")
        questionDictionary[fileName] = "Solution for Q3 is incorrect <br>"

    return res




def testQ4(func, fileName):
    from solutions.Q4Sol import q4 as answer

    fileArr = fileName.split('_')
    studName = fileArr[0]

    res = ""

    if (func(10) == answer(10) and func(2) == answer(2) and func(5) == answer(5)):
        res += ("Q4 is correct <br>")
        questionDictionary[fileName] = "Solution for Q3 is correct <br>"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += ("Q4 is incorrect <br>")
        questionDictionary[fileName] = "Solution for Q3 is incorrect <br>"

    return res



def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 



def testAll(filesToTest):
    newName = True
    prev = ""
    results = []
    for f in filesToTest:
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

        if (prev != fileArr[0]):
            newName = True

        if (newName):
            results.append("<br>" + fileArr[0] + ":<br>")


        if (fileArr[1] == "Q3"):
            results.append(testQ3(func, f))
            

        if (fileArr[1] == "Q4"):
            results.append(testQ4(func, f))

        prev = fileArr[0]
        newName = False


    results.append("<br><br>Sores: <br>")

    students = [(file.split('_')[0]) for file in filesToTest]
    studentsUnique = list(dict.fromkeys(students))

    for student in studentsUnique:
        results.append(student + " score: <strong>" + str((gradeDictionary[student]/NUMBER_OF_QUESTIONS)*100) + "%</strong>")
        results.append("<br>")

    return (listToString(results))



def filterFun(q):
    filtered = []
    for file in fileNames:
        if str(file.split('_')[1]).lower() == q:
            filtered.append(file)
    return filtered



def testQues3():
    filtered = filterFun("q3")
    return testAll(filtered)

def testQues4():
    filtered = filterFun("q4")
    return testAll(filtered)



if question == "all":
    print(testAll(fileNames))
elif question == "q3":
    print(testQues3())
elif question == "q4":
    print(testQues4())





