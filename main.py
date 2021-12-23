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
  "minimum":               "W2Q1"
}
gradeDictionary = {}
questionDictionary = {}

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




from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(noteBookFolder) if isfile(join(noteBookFolder, f))]



fileNamesInitial = []
for file in onlyfiles:
    lst = file.split(".")
    fileName = lst[0]
    fileNamesInitial.append(fileName)

    fileArr = fileName.split('_')

    pos = fileName.find("_")
    studentID = fileName[:pos]
    functionName = fileName[pos+1:]

    # initialize points
    gradeDictionary[studentID] = 0

    questionDictionary[fileName] = ""

    noteBookPath = (noteBookFolder + "\\" + str(file))
    scriptPath = (scriptsFolder + "\\" + str(fileName) + ".py")
    try:
        convertNotebook(noteBookPath, scriptPath)
    except:
        pass

def getKey(file):
    fileArr = file.split('_')
    ques = fileArr[1]

    pos = file.find("_")
    studentID = file[:pos]
    functionName = file[pos+1:]

    week_question = functionToQuestion[functionName]
    week_num = int(week_question[1:2])
    ques_num = int(week_question[3:])

    ## ERROR HANDLING : IF NAME DOESNT MATCH QUESTION NUMBER

    # ques_num = (int(ques[1:]))
    return (fileArr[0], week_num, ques_num)

fileNames = sorted(fileNamesInitial, key=getKey)

def testProvidedCases(func, answer, testCases, params, studentName, q, w, name):
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
        questionDictionary[fileName] = "Correct"
        gradeDictionary[studentName] = gradeDictionary[studentName] + 1
    else:
        res += tableFormRecords((w_str + q_str + q_name), "&#10060")
        questionDictionary[fileName] = "Incorrect"
   
    return res

    
    
    # return allCorrect



def testW1Q1(func, fileName):
    from solutions.solutions import positive_integer as answer
    testCases = [0, 1, 50, -1]

    fileArr = fileName.split('_')
    studentName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 1, studentName, "1", "1", "positive_integer")

   

def testW1Q2(func, fileName):
    from solutions.solutions import multiples as answer

    testCases = [2, 5, 10]

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 1, studName, "2", "1", "multiples")
    


def testW1Q3(func, fileName):
    from solutions.solutions import product as answer

    testCases = [(2,2), (3, 5), (0, 10), (2, 0)]

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 2, studName, "3", "1", "product")


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
        questionDictionary[fileName] = "Correct"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords((w_str + q_str + " (student_grade)"), "&#10060")
        questionDictionary[fileName] = "Incorrect"

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
        questionDictionary[fileName] = "Correct"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords((w_str + q_str + " (squares)"), "&#10060")
        questionDictionary[fileName] = "Incorrect"

    return res


def testW1Q6(func, fileName):
    from solutions.solutions import odd_numbers as answer

    testCases = []

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 0, studName, "6", "1", "odd_numbers")


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
        questionDictionary[fileName] = "Correct"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords((w_str + q_str + " (loops)"), "&#10060")
        questionDictionary[fileName] = "Incorrect"

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
        questionDictionary[fileName] = "Correct"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords((w_str + q_str + " (even_num)"), "&#10060")
        questionDictionary[fileName] = "Incorrect"

    return res


def testW1Q9(func, fileName):
    from solutions.solutions import string_manipulation as answer

    testCases = ["abcdef", "hello world"]

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 1, studName, "9", "1", "string_manipulation")



def testW1Q10(func, fileName):
    from solutions.solutions import strings as answer

    testCases = [("a", "b"), ("hello ","world!" )]

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 2, studName, "10", "1", "strings")

def tesW2Q1(func, fileName):
    from solutions.solutions import minimum as answer
    testCases = [[2, 5, 10], [5, -4, 3], [10, 12, 13]]
    fileArr = fileName.split('_')
    studName = fileArr[0]
    return testProvidedCases(func, answer, testCases, 1, studName, "1", "2", "minimum")

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
                res += tableFormRecords("Question 1", "&#10060")
                questionDictionary[fileName] = "Incorrect"

            # if only one function
            # res += (testQ1(func, f))
            

        if (functionName.lower() == "multiples"):
            # if name of main function known:
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q2(testModule.multiples, f))
            except:
                res += tableFormRecords("Question 2", "&#10060")
                questionDictionary[fileName] = "Incorrect"


        if (functionName.lower() == "product"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q3(testModule.product, f))
            except:
                res += tableFormRecords("Question 3", "&#10060")
                questionDictionary[fileName] = "Incorrect"


        if (functionName.lower() == "student_grade"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q4(testModule.student_grade, f))
            except:
                res += tableFormRecords("Question 4", "&#10060")
                questionDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "squares"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q5(testModule.squares, f))
            except:
                res += tableFormRecords("Error Question 5", "&#10060")
                questionDictionary[fileName] = "Incorrect"
        
        if (functionName.lower() == "odd_numbers"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q6(testModule.odd_numbers, f))
            except:
                res += tableFormRecords("Question 6", "&#10060")
                questionDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "loops"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q7(testModule.loops, f))
            except:
                res += tableFormRecords("Question 7", "&#10060")
                questionDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "even_num"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q8(testModule.even_num, f))
            except:
                res += tableFormRecords("Question 8", "&#10060")
                questionDictionary[fileName] = "Incorrect"


        if (functionName.lower() == "string_manipulation"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q9(testModule.string_manipulation, f))
            except:
                res += tableFormRecords("Question 9", "&#10060")
                questionDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "strings"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (testW1Q10(testModule.strings, f))
            except:
                res += tableFormRecords("Question 10", "&#10060")
                questionDictionary[fileName] = "Incorrect"

        if (functionName.lower() == "minimum"):
            try:
                fileToImport = 'scripts.' + f
                testModule = importlib.import_module(fileToImport)
                res += (tesW2Q1(testModule.minimum, f))
            except:
                res += tableFormRecords("Question 1 Week 2", "&#10060")
                questionDictionary[fileName] = "Incorrect"


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

            res += (student + " : <strong>" + str("{:.2f}".format((gradeDictionary[student]/NUMBER_OF_QUESTIONS)*100)) + "%</strong>")
            res += "<br>"

        generateScoreSheet()


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

    generateCSV()

    return res

import csv
def generateCSV():

    current = os.getcwd() 
    save_path = "/results/"
    fn = "results_" + question + ".csv"

    with open(current + save_path + fn, mode='w', newline='') as results_file:
        results_writer = csv.writer(results_file)
        results_writer.writerow(["Student", "QuestionNumber", "Result"])
        for key in questionDictionary:
            studID = key.split('_')[0]

            pos = key.find("_")
            studentID = key[:pos]
            functionName = key[pos+1:]

            week_question = functionToQuestion[functionName]
            quesNum = week_question[2:]

            questionNum = key.split('_')[1]
            result = questionDictionary[key]
            if (question == quesNum.lower() or (question == "all")):
                results_writer.writerow([studID, quesNum, result])
            
            



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
        quesNum = week_question[2:]

        if str(quesNum).lower() == q:
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

def testQues2():
    filtered = filterFun("q2")
    return testAll(filtered)

if question == "all":
    print(testAll(fileNames))
elif question == "q1":
    print(testQues("q1"))
elif question == "q2":
    print(testQues("q2"))
elif question == "q3":
    print(testQues("q3"))
elif question == "q4":
    print(testQues("q4"))
elif question == "q5":
    print(testQues("q5"))
elif question == "q6":
    print(testQues("q6"))
elif question == "q7":
    print(testQues("q7"))
elif question == "q8":
    print(testQues("q8"))
elif question == "q9":
    print(testQues("q9"))
elif question == "q10":
    print(testQues("q10"))






