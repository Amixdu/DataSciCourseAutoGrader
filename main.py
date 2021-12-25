import json
import importlib
import sys
from inspect import getmembers, isfunction
import os

import nbformat
from nbconvert import PythonExporter

gbl = globals()

NUMBER_OF_QUESTIONS = 11
functionToQuestion = {
    "positive_integer":      "W1Q1",
    "multiples":             "W1Q2",
    "product":               "W1Q3",
    "student_grade":         "W1Q4",
    "squares":               "W1Q5",
    "odd_numbers":           "W1Q6",
    "loops":                 "W1Q7",
    "even_num":              "W1Q8",
    "string_manipulation":   "W1Q9",
    "strings":               "W1Q10",
    "minimum":               "W2Q1",
    "sums":                  "W2Q2",
    "unique":                "W2Q3",
    "string_index":          "W2Q4",
    "elements":              "W2Q5",
    "letter_a":              "W2Q6",
    "even_numbers":          "W2Q7",
    "square_root":           "W2Q8",
    "sets":                  "W2Q9",
    "remove_elements":        "W2Q10"
}


gradeDictionary = {}
questionResultsDictionary = {}

# noteBookFolder = "D:\\Projects\\PythonAutoGrading\\Test1\\sample_uploads"
noteBookFolder = sys.argv[1]
# question = "all"
question = sys.argv[2]


def createFolder(name):
    d = os.path.dirname(__file__) # directory of script
    p = (r'{}/'+str(name)).format(d) # path to be created

    try:
        os.makedirs(p)
    except OSError:
        pass

# create folder for converted python scripts
createFolder("scripts")

# to convert note book to python script
def convertNotebook(notebookPath, modulePath):

  with open(notebookPath) as fh:
    nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)

  exporter = PythonExporter()
  source, meta = exporter.from_notebook_node(nb)

  with open(modulePath, 'w+') as fh:
    fh.writelines(source)


# scriptsFolder = "D:\\Projects\\PythonAutoGrading\\Test1\\scripts"
current = os.getcwd() 
save_path = "/scripts"
scriptsFolder = current + save_path

def getKey(file):
    MAX = 99999

    fileName = file.split('.')[0]

    fileArr = fileName.split('_')
    # ques = fileArr[1]

    pos = fileName.find("_")
    studentID = fileName[:pos]
    functionName = fileName[pos+1:]

    try:
        week_question = functionToQuestion[functionName]
        week_num = int(week_question[1:2])
        ques_num = int(week_question[3:])
    except:
        week_num = MAX
        ques_num = MAX

    ## ERROR HANDLING : IF NAME DOESNT MATCH QUESTION NUMBER

    # ques_num = (int(ques[1:]))
    return (fileArr[0], week_num, ques_num)


def cleanFiles(files):
    res = []
    for file in files:
        if len(file.split("_")) > 1:
            res.append(file)
    return res





from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(noteBookFolder) if isfile(join(noteBookFolder, f))]
cleaned_files = cleanFiles(onlyfiles)
onlyfiles_sorted = sorted(cleaned_files, key=getKey)

not_marked = len(onlyfiles) - len(cleaned_files)



fileNames = []
for file in onlyfiles_sorted:
    lst = file.split(".")
    fileName = lst[0]
    fileNames.append(fileName)

    fileArr = fileName.split('_')

    pos = fileName.find("_")
    studentID = fileName[:pos]
    functionName = fileName[pos+1:]

    # initialize points
    gradeDictionary[studentID] = 0

    questionResultsDictionary[fileName] = ""

    noteBookPath = (noteBookFolder + "\\" + str(file))
    scriptPath = (scriptsFolder + "\\" + str(fileName) + ".py")
    try:
        convertNotebook(noteBookPath, scriptPath)
    except:
        pass



# fileNames = sorted(fileNamesInitial, key=getKey)

def testProvidedCases(func, answer, testCases, params, studentName, q, w, name, fileName):
    allCorrect = True
    res = ""
    try:
        for case in testCases:
            if (params == 0):
                if (func() != answer()):
                    allCorrect = False
            elif (params == 1):
                if (func(case) != (answer(case))):
                    allCorrect = False
            elif (params == 2):
                if (func(case[0], case[1]) != answer(case[0], case[1])):
                    allCorrect = False
    except:
        allCorrect = False

    q_str = " Question " + q
    w_str = "Week " + w
    q_name = " (" + name + ")"

    if (allCorrect):
        res += tableFormRecords((w_str + q_str + q_name), "&#9989")
        questionResultsDictionary[fileName] = "Correct"
        gradeDictionary[studentName] = gradeDictionary[studentName] + 1
    else:
        res += tableFormRecords((w_str + q_str + q_name), "&#10060")
        questionResultsDictionary[fileName] = "Incorrect"
   
    return res

    
    
    # return allCorrect




def testW1Q1(func, fileName):
    from solutions.solutions import positive_integer as answer
    testCases = [0, 1, 50, -1]

    fileArr = fileName.split('_')
    studentName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 1, studentName, "1", "1", "positive_integer", fileName)

   

def testW1Q2(func, fileName):
    from solutions.solutions import multiples as answer

    testCases = [2, 5, 10]

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 1, studName, "2", "1", "multiples", fileName)
    


def testW1Q3(func, fileName):
    from solutions.solutions import product as answer

    testCases = [(2,2), (3, 5), (0, 10), (2, 0)]

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 2, studName, "3", "1", "product", fileName)


def testW1Q4(func, fileName):
    from solutions.solutions import student_grade as answer
    import io

    testCases = [0, 10, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, -1]
    # testCases = [60]

    fileArr = fileName.split('_')
    studName = fileArr[0]

    allCorrect = True
    res = ""
    try:
        for case in testCases:
            capturedOutput = io.StringIO()
            sys.stdout = capturedOutput      
            func(case)
            sys.stdout = sys.__stdout__  
            if (capturedOutput.getvalue() != (answer(case)) and (capturedOutput.getvalue() != (answer(case) + "\n"))):
                allCorrect = False
    except:
        allCorrect = False

    q_str = " Question 4"
    w_str = "Week 1"
    if (allCorrect):
        res += tableFormRecords((w_str + q_str + " (student_grade)"), "&#9989")
        questionResultsDictionary[fileName] = "Correct"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords((w_str + q_str + " (student_grade)"), "&#10060")
        questionResultsDictionary[fileName] = "Incorrect"

    return res


def testW1Q5(func, fileName):
    from solutions.solutions import q5v1 as answer1
    from solutions.solutions import q5v2 as answer2

    import io

    fileArr = fileName.split('_')
    studName = fileArr[0]

    correct = False
    res = ""

    q_str = "Question 5"
    w_str = "Week 1 "
    try:
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput      
        # current = os.getcwd() 
        # path = "/scripts/"
        # fn = fileName  + ".py"
        # full_path = current + path + fn
        # exec(open(full_path).read())
        func()
        sys.stdout = sys.__stdout__  
        if ((capturedOutput.getvalue() == answer1()) or (capturedOutput.getvalue() == answer2())):
            correct = True
    except:
        correct = False

    
    
    if (correct):
        res += tableFormRecords((w_str + q_str + " (squares)"), "&#9989")
        questionResultsDictionary[fileName] = "Correct"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords((w_str + q_str + " (squares)"), "&#10060")
        questionResultsDictionary[fileName] = "Incorrect"

    return res


def testW1Q6(func, fileName):
    from solutions.solutions import odd_numbers as answer

    testCases = []

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 0, studName, "6", "1", "odd_numbers", fileName)


def testW1Q7(func, fileName):
    from solutions.solutions import loops as answer1
    from solutions.solutions import loopsV2 as answer2
    import io

    fileArr = fileName.split('_')
    studName = fileArr[0]

    testCases = [0, 4, 10, 16, 24]

    correct = True
    res = ""

    q_str = "Question 7"
    w_str = "Week 1 "
    try:
        for case in testCases:
            capturedOutput = io.StringIO()
            sys.stdout = capturedOutput      
            func(case)
            sys.stdout = sys.__stdout__  
            if ((capturedOutput.getvalue() != answer1(case)) and (capturedOutput.getvalue() != answer2(case))):
                correct = False
    except:
        correct = False
    
    if (correct):
        res += tableFormRecords((w_str + q_str + " (loops)"), "&#9989")
        questionResultsDictionary[fileName] = "Correct"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords((w_str + q_str + " (loops)"), "&#10060")
        questionResultsDictionary[fileName] = "Incorrect"

    return res


def testW1Q8(func, fileName):
    from solutions.solutions import q8v1 as answer1
    from solutions.solutions import q8v2 as answer2

    import io

    fileArr = fileName.split('_')
    studName = fileArr[0]

    correct = False
    res = ""

    q_str = "Question 8"
    w_str = "Week 1 "
    try:
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput      
        # current = os.getcwd() 
        # path = "/scripts/"
        # fn = fileName  + ".py"
        # full_path = current + path + fn
        # exec(open(full_path).read())
        func()
        sys.stdout = sys.__stdout__  
        if ((capturedOutput.getvalue() == answer1()) or (capturedOutput.getvalue() == answer2())):
            correct = True
    except:
        correct = False

    
    
    if (correct):
        res += tableFormRecords((w_str + q_str + " (even_num)"), "&#9989")
        questionResultsDictionary[fileName] = "Correct"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords((w_str + q_str + " (even_num)"), "&#10060")
        questionResultsDictionary[fileName] = "Incorrect"

    return res


def testW1Q9(func, fileName):
    from solutions.solutions import string_manipulation as answer

    testCases = ["abcdef", "hello world"]

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 1, studName, "9", "1", "string_manipulation", fileName)



def testW1Q10(func, fileName):
    from solutions.solutions import strings as answer

    testCases = [("a", "b"), ("hello ","world!" )]

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 2, studName, "10", "1", "strings", fileName)

def testW2Q1(func, fileName):
    from solutions.solutions import minimum as answer
    testCases = [[2, 5, 10], [5, -4, 3], [10, 12, 13]]
    fileArr = fileName.split('_')
    studName = fileArr[0]
    return testProvidedCases(func, answer, testCases, 1, studName, "1", "2", "minimum", fileName)


def testW2Q2(func, fileName):
    from solutions.solutions import sums as answer
    testCases = [[2, 5, 10], [5, -4, 3], [10, 12, 13]]
    fileArr = fileName.split('_')
    studName = fileArr[0]
    return testProvidedCases(func, answer, testCases, 1, studName, "2", "2", "sums", fileName)


def testW2Q3(func, fileName):
    from solutions.solutions import unique as answer
    testCases = [[2, 2, 10], [5, -4, 3], [10, 12, 13]]
    fileArr = fileName.split('_')
    studName = fileArr[0]
    return testProvidedCases(func, answer, testCases, 1, studName, "3", "2", "unique", fileName)

def testW2Q4(func, fileName):
    from solutions.solutions import string_index as answer
    testCases = [(["hello", "world", "python"], "python"), (["java", "data science"], "data science")]
    fileArr = fileName.split('_')
    studName = fileArr[0]
    return testProvidedCases(func, answer, testCases, 2, studName, "4", "2", "string_index", fileName)

def testW2Q5(func, fileName):
    from solutions.solutions import elements as answer1
    from solutions.solutions import elementsV2 as answer2

    import io

    fileArr = fileName.split('_')
    studName = fileArr[0]

    correct = False
    res = ""

    q_str = "Question 5"
    w_str = "Week 2 "
    try:
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput      
        func(("Hello", "world", "a", ""))
        sys.stdout = sys.__stdout__  
        if ((capturedOutput.getvalue() == answer1(("Hello", "world", "a", ""))) or (capturedOutput.getvalue() == answer2(("Hello", "world", "a", "")))):
            correct = True
    except:
        correct = False

    
    
    if (correct):
        res += tableFormRecords((w_str + q_str + " (elements)"), "&#9989")
        questionResultsDictionary[fileName] = "Correct"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords((w_str + q_str + " (elements)"), "&#10060")
        questionResultsDictionary[fileName] = "Incorrect"

    return res

def testW2Q6(func, fileName):
    from solutions.solutions import letter_a as answer1
    from solutions.solutions import letter_aV2 as answer2

    import io

    fileArr = fileName.split('_')
    studName = fileArr[0]

    correct = False
    res = ""

    q_str = "Question 6"
    w_str = "Week 2 "
    try:
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput      
        func(("data", "hello", "world", ""))
        sys.stdout = sys.__stdout__  
        if ((capturedOutput.getvalue() == answer1(("data", "hello", "world", ""))) or (capturedOutput.getvalue() == answer2(("data", "hello", "world", "")))):
            correct = True
    except:
        correct = False

    
    
    if (correct):
        res += tableFormRecords((w_str + q_str + " (letter_a)"), "&#9989")
        questionResultsDictionary[fileName] = "Correct"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords((w_str + q_str + " (letter_a)"), "&#10060")
        questionResultsDictionary[fileName] = "Incorrect"

    return res

def testW2Q7(func, fileName):
    from solutions.solutions import even_numbers as answer
    testCases = [(1,2,3,4), (0,2,3,4,5,7)]
    fileArr = fileName.split('_')
    studName = fileArr[0]
    return testProvidedCases(func, answer, testCases, 1, studName, "7", "2", "even_numbers", fileName)

def testW2Q8(func, fileName):
    from solutions.solutions import square_root as answer
    testCases = [[1,2,3,4,5]]
    fileArr = fileName.split('_')
    studName = fileArr[0]
    return testProvidedCases(func, answer, testCases, 1, studName, "8", "2", "square_root", fileName)

def testW2Q9(func, fileName):
    from solutions.solutions import sets as answer
    testCases = [[{1,2,3}, {1,2}]]
    fileArr = fileName.split('_')
    studName = fileArr[0]
    return testProvidedCases(func, answer, testCases, 2, studName, "9", "2", "sets", fileName)

def testW2Q10(func, fileName):
    from solutions.solutions import remove_elements as answer
    testCases = [[{1,2,3}, {1,2}]]
    fileArr = fileName.split('_')
    studName = fileArr[0]
    return testProvidedCases(func, answer, testCases, 2, studName, "10", "2", "remove_elements", fileName)

def runTest(functionName, name_str, f, func, q):
    res = ""
    if (functionName.lower() == name_str):
        try:
            fileToImport = 'scripts.' + f
            testModule = importlib.import_module({fileToImport})
            res += (func(testModule.name_str, f))
        except:
            res += tableFormRecords(q, "&#10060")
    return res

    
def testAll(filesToTest):
    createFolder("results")
    newName = True
    prev = ""
    res = """
    <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8"/>
            <title>Data Sci Course Grader</title>
            <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.1/font/bootstrap-icons.css">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
            <script>
                function goBack(){
                    location.href = "index.html";
                }
            </script>
          </head>
          <body style="background-color: #2f6fa3;">
            <div id="container">
                <div id="title" style="color: #d0dfe8; font-size: 3em; margin-bottom: 1em; text-align: center;">
                    <u><strong>Grading Results:</strong></u>
                </div>
                <div id="table" style="background-color:white; width: 75%; margin: auto;">
                    <table class="table">
                        <thead>
                            <tr>
                                <th scope="col" style="font-size: 1.35em;">Student</th>
                                <th scope="col" style="font-size: 1.35em;">Question</th>
                                <th scope="col" style="font-size: 1.35em;">Result</th>
                              </tr>
                        </thead>
                        <tbody>
    """
    for f in filesToTest:
        # fileToImport = 'scripts.' + f
        # testModule = importlib.import_module(fileToImport)

        # below line gets funtion name from script
        # functionName = (getmembers(testModule, isfunction)[0][0])
        # func = getattr(testModule, functionName)
        fileArr = f.split('_')

        pos = f.find("_")
        studentID = f[:pos]
        functionName = f[pos+1:]

        if (prev != fileArr[0]):
            newName = True

        if (newName):
            res += tableFormHeading(fileArr[0])
        else:
            res += tableFormHeading("")
            
            
        if (functionName.lower() == "positive_integer"):
            # if name of main function known:
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q1(testModule.positive_integer, f))
            except:
                res += tableFormRecords(("Week 1 Question 1 (positive_integer)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        # res += runTest(functionName, "positive_integer", f, testW1Q1, "Question 1")

            # if only one function
            # res += (testQ1(func, f))
            

        if (functionName.lower() == "multiples"):
            # if name of main function known:
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q2(testModule.multiples, f))
            except:
                res += tableFormRecords(("Week 1 Question 2 (multiples)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"


        if (functionName.lower() == "product"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q3(testModule.product, f))
            except:
                res += tableFormRecords(("Week 1 Question 3 (product)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"


        if (functionName.lower() == "student_grade"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q4(testModule.student_grade, f))
            except:
                res += tableFormRecords(("Week 1 Question 4 (student_grade)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "squares"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q5(testModule.squares, f))
            except:
                res += tableFormRecords(("Week 1 Question 5 (squares)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"
        
        if (functionName.lower() == "odd_numbers"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q6(testModule.odd_numbers, f))
            except:
                res += tableFormRecords(("Week 1 Question 6 (odd_numbers)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "loops"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q7(testModule.loops, f))
            except:
                res += tableFormRecords(("Week 1 Question 7 (loops)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "even_num"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q8(testModule.even_num, f))
            except:
                res += tableFormRecords(("Week 1 Question 8 (even_num)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"


        if (functionName.lower() == "string_manipulation"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q9(testModule.string_manipulation, f))
            except:
                res += tableFormRecords(("Week 1 Question 9 (string_manipulation)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "strings"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q10(testModule.strings, f))
            except:
                res += tableFormRecords(("Week 1 Question 10 (strings)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "minimum"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW2Q1(testModule.minimum, f))
            except:
                res += tableFormRecords(("Week 2 Question 1 (minimum)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "sums"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW2Q2(testModule.sums, f))
            except:
                res += tableFormRecords(("Week 2 Question 2 (sums)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "unique"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW2Q3(testModule.unique, f))
            except:
                res += tableFormRecords(("Week 2 Question 3 (unique)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "string_index"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW2Q4(testModule.string_index, f))
            except:
                res += tableFormRecords(("Week 2 Question 4 (string_index)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "elements"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW2Q5(testModule.elements, f))
            except:
                res += tableFormRecords(("Week 2 Question 5 (elements)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "letter_a"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW2Q6(testModule.letter_a, f))
            except:
                res += tableFormRecords(("Week 2 Question 6 (letter_a)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "even_numbers"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW2Q7(testModule.even_numbers, f))
            except:
                res += tableFormRecords(("Week 2 Question 7 (even_numbers)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "square_root"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW2Q8(testModule.square_root, f))
            except:
                res += tableFormRecords(("Week 2 Question 8 (square_root)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "sets"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW2Q9(testModule.sets, f))
            except:
                res += tableFormRecords(("Week 2 Question 9 (sets)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "remove_elements"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW2Q10(testModule.remove_elements, f))
            except:
                res += tableFormRecords(("Week 2 Question 10 (remove_elements)"), "&#10060")
                questionResultsDictionary[fileName] = "Incorrect"
        
       


        prev = fileArr[0]
        newName = False

    
    res += """
    </tbody>
            </table>
            </div><br><br>        
    """

    if (question == "all"):
        res += """
                <div id="totalScore">
                    <div id="subtitle" style="color: #d0dfe8; font-size: 1.5em; margin-bottom: 1em; text-align: center;">
                        <strong>Final Results</strong>
                    </div>
                    <div class="card text-dark bg-light mb-3" style="width: 50%; margin: auto;">
                        <div class="card-header">Results Overview</div>
                        <div class="card-body">
                """
        students = [(file.split('_')[0]) for file in filesToTest]
        studentsUnique = list(dict.fromkeys(students))

        for student in studentsUnique:
            try:
                res += (student + " : <strong>" + str("{:.2f}".format((gradeDictionary[student]/NUMBER_OF_QUESTIONS)*100)) + "%</strong>")
                res += "<br><br>"
            except:
                res += (student + " : Error in file naming")
                res += "<br><br>"

        generateScoreSheet()

    if (not_marked > 0):
        res += (str(not_marked) + " file not marked due to file naming issues")

    res += """     
                        </div>
                      </div>
                      <div class="col text-center">
                        <button type="button" class="btn btn-light" onClick="goBack()" style="margin-top: 1.5rem; margin-bottom: 0.5em;"><i class="bi bi-arrow-left"></i> Go Back</button>
                    </div>
                </div>
            </div>
          </body>
        </html>"""

    works = generateCSV()
    if (not works):
        res = "Please try closing the CSV files in the results folder and running again"

    return res

import csv
def generateCSV():

    current = os.getcwd() 
    save_path = "/results/"
    fn = "results_" + question + ".csv"

    res = True

    try:
        with open(current + save_path + fn, mode='w', newline='') as results_file:
            results_writer = csv.writer(results_file)
            results_writer.writerow(["Student", "QuestionNumber", "Result"])
            for key in questionResultsDictionary:
                studID = key.split('_')[0]

                pos = key.find("_")
                studentID = key[:pos]
                functionName = key[pos+1:]

                try:
                    week_question = functionToQuestion[functionName]
                    weekNum = week_question[0:2]
                    quesNum = week_question[2:]
                except:
                    quesNum = "Question Name Not Recognized (Check File Name)"

                questionName = key.split('_')[1]
                result = questionResultsDictionary[key]
                if (question == week_question.lower() or (question == "all")):
                    results_writer.writerow([studID, (weekNum + " "+ quesNum + " (" + functionName + ")"), result])
    except:
        res = False

    return res
            
            



def generateScoreSheet():
    current = os.getcwd() 
    save_path = "/results/"
    fn = "grades.csv"
    

    # with fpath.open(mode='w+', newline='') as grades_file:
    with open(current + save_path + fn, mode='w', newline='') as grades_file:
        grades_writer = csv.writer(grades_file)
        grades_writer.writerow(["Student", "TotalGrade", "FinalResult"])
        for key in gradeDictionary:
            score = "{:.2f}".format((gradeDictionary[key]/NUMBER_OF_QUESTIONS) * 100)
            result = ""
            if float(score) >= 50:
                result = "Pass"
            else:
                result = "Fail"

            grades_writer.writerow([key, (str(score) + "%"), result])



def filterFun(q):
    filtered = []
    for file in fileNames:
        pos = file.find("_")
        studentID = file[:pos]
        functionName = file[pos+1:]

        week_question = functionToQuestion[functionName]
        

        if str(week_question).lower() == q:
            filtered.append(file)
    return filtered


def tableFormHeading(val):
    return (""" 
            <tr>
                <td>""" 
                + val + """</td>
            """)

def tableFormRecords(ques, result):
    return (""" 
                <td>""" 
                + ques + """</td>

                <td>""" 
                + result + """</td>

            </tr>
            """)


def testQues(q):
    filtered = filterFun(q)
    return testAll(filtered)

if question == "all":
    print(testAll(fileNames))
elif question == "w1q1":
    print(testQues("w1q1"))
elif question == "w1q2":
    print(testQues("w1q2"))
elif question == "w1q3":
    print(testQues("w1q3"))
elif question == "w1q4":
    print(testQues("w1q4"))
elif question == "w1q5":
    print(testQues("w1q5"))
elif question == "w1q6":
    print(testQues("w1q6"))
elif question == "w1q7":
    print(testQues("w1q7"))
elif question == "w1q8":
    print(testQues("w1q8"))
elif question == "w1q9":
    print(testQues("w1q9"))
elif question == "w1q10":
    print(testQues("w1q10"))

elif question == "w2q1":
    print(testQues("w2q1"))
elif question == "w2q2":
    print(testQues("w2q2"))
elif question == "w2q3":
    print(testQues("w2q3"))
elif question == "w2q4":
    print(testQues("w2q4"))
elif question == "w2q5":
    print(testQues("w2q5"))
elif question == "w2q6":
    print(testQues("w2q6"))
elif question == "w2q7":
    print(testQues("w2q7"))
elif question == "w2q8":
    print(testQues("w2q8"))
elif question == "w2q9":
    print(testQues("w2q9"))
elif question == "w2q10":
    print(testQues("w2q10"))








