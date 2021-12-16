import json
import importlib
import sys
from inspect import getmembers, isfunction
import os

import nbformat
from nbconvert import PythonExporter

gbl = globals()

NUMBER_OF_QUESTIONS = 6

gradeDictionary = {}
questionDictionary = {}

noteBookFolder = "D:\\Projects\\PythonAutoGrading\\Test1\\uploads"
# noteBookFolder = sys.argv[1]
question = "all"
# question = sys.argv[2]


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



fileNames = []
for file in onlyfiles:
    lst = file.split(".")
    fileName = lst[0]
    fileNames.append(fileName)

    fileArr = fileName.split('_')

    # initialize points
    gradeDictionary[fileArr[0]] = 0

    questionDictionary[fileName] = ""

    noteBookPath = (noteBookFolder + "\\" + str(file))
    scriptPath = (scriptsFolder + "\\" + str(fileName) + ".py")
    convertNotebook(noteBookPath, scriptPath)


def testProvidedCases(func, answer, testCases, params, studentName, q):
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

    q_str = "Question " + q
    if (allCorrect):
        res += tableFormRecords(q_str, "&#9989")
        questionDictionary[fileName] = "Correct"
        gradeDictionary[studentName] = gradeDictionary[studentName] + 1
    else:
        res += tableFormRecords(q_str, "&#10060")
        questionDictionary[fileName] = "Incorrect"
   
    return res

    
    
    # return allCorrect



def testQ1(func, fileName):
    from solutions.solutions import positive_integer as answer
    testCases = [0, 1, 50, -1]

    fileArr = fileName.split('_')
    studentName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 1, studentName, "1")

   

def testQ2(func, fileName):
    from solutions.solutions import multiples as answer

    testCases = [2, 5, 10]

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 1, studName, "2")
    


def testQ3(func, fileName):
    from solutions.solutions import product as answer

    testCases = [(2,2), (3, 5), (0, 10), (2, 0)]

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 2, studName, "3")


def testQ4(func, fileName):
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

    q_str = "Question 4"
    if (allCorrect):
        res += tableFormRecords(q_str, "&#9989")
        questionDictionary[fileName] = "Correct"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords(q_str, "&#10060")
        questionDictionary[fileName] = "Incorrect"

    return res


def testQ5(fileName):
    from solutions.Q5Sol import q5v1 as answer1
    from solutions.Q5Sol import q5v2 as answer2

    import io

    fileArr = fileName.split('_')
    studName = fileArr[0]

    correct = False
    res = ""

    q_str = "Question 5"
    try:
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput      
        current = os.getcwd() 
        path = "/scripts/"
        fn = fileName  + ".py"
        full_path = current + path + fn
        exec(open(full_path).read())
        sys.stdout = sys.__stdout__  
        if ((capturedOutput.getvalue() == answer1()) or (capturedOutput.getvalue() == answer2())):
            correct = True
    except:
        correct = False

    
    
    if (correct):
        res += tableFormRecords(q_str, "&#9989")
        # questionDictionary[fileName] = "Correct"
        # gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords(q_str, "&#10060")
        # questionDictionary[fileName] = "Incorrect"

    return res


def testQ6(func, fileName):
    from solutions.solutions import odd_numbers as answer

    testCases = []

    fileArr = fileName.split('_')
    studName = fileArr[0]

    return testProvidedCases(func, answer, testCases, 0, studName, "6")


# def testQ7(func, fileName):
#     from solutions.solutions import loops as answer1
#     from solutions.solutions import loopsV2 as answer2
#     import io

#     fileArr = fileName.split('_')
#     studName = fileArr[0]

#     testCases = [0, 4, 10, 16, 24]

#     correct = True
#     res = ""

#     q_str = "Question 7"
#     try:
#         for case in testCases:
#             capturedOutput = io.StringIO()
#             sys.stdout = capturedOutput      
#             func(case)
#             sys.stdout = sys.__stdout__  
#             if ((capturedOutput.getvalue() != answer1(case)) and (capturedOutput.getvalue() != answer2(case))):
#                 correct = False
#     except:
#         correct = False

    
    
#     if (correct):
#         res += tableFormRecords(q_str, "&#9989")
#         questionDictionary[fileName] = "Correct"
#         gradeDictionary[studName] = gradeDictionary[studName] + 1
#     else:
#         res += tableFormRecords(q_str, "&#10060")
#         questionDictionary[fileName] = "Incorrect"

#     return res


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
        # CHECK PATH
        # fileToImport = 'scripts.' + f
        # testModule = importlib.import_module(fileToImport)

        # below line gets funtion name from script
        # functionName = (getmembers(testModule, isfunction)[0][0])
        # func = getattr(testModule, functionName)
        fileArr = f.split('_')

        if (prev != fileArr[0]):
            newName = True

        if (newName):
            res += tableFormHeading(fileArr[0])
        else:
            res += tableFormHeading("")
            
            
        if ((fileArr[1]).lower() == "q1"):
            # if name of main function known:
            fileToImport = 'scripts.' + f
            testModule = importlib.import_module(fileToImport)
            res += (testQ1(testModule.positive_integer, f))

            # if only one function
            # res += (testQ1(func, f))
            

        if ((fileArr[1]).lower() == "q2"):
            # if name of main function known:
            fileToImport = 'scripts.' + f
            testModule = importlib.import_module(fileToImport)
            res += (testQ2(testModule.multiples, f))

        if ((fileArr[1]).lower() == "q3"):
            fileToImport = 'scripts.' + f
            testModule = importlib.import_module(fileToImport)
            res += (testQ3(testModule.product, f))

        if ((fileArr[1]).lower() == "q4"):
            fileToImport = 'scripts.' + f
            testModule = importlib.import_module(fileToImport)
            res += (testQ4(testModule.student_grade, f))

        if ((fileArr[1]).lower() == "q5"):
            res += (testQ5(f))
        
        if ((fileArr[1]).lower() == "q6"):
            fileToImport = 'scripts.' + f
            testModule = importlib.import_module(fileToImport)
            res += (testQ6(testModule.odd_numbers, f))

        # if ((fileArr[1]).lower() == "q7"):
        #     fileToImport = 'scripts.' + f
        #     testModule = importlib.import_module(fileToImport)
        #     res += (testQ7(testModule.loops, f))


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
            questionNum = key.split('_')[1]
            result = questionDictionary[key]
            if (question == questionNum.lower() or (question == "all")):
                results_writer.writerow([studID, questionNum, result])
            
            



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
        if str(file.split('_')[1]).lower() == q:
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


def testQues1():
    filtered = filterFun("q1")
    return testAll(filtered)

def testQues2():
    filtered = filterFun("q2")
    return testAll(filtered)

if question == "all":
    print(testAll(fileNames))
elif question == "q1":
    print(testQues1())
elif question == "q2":
    print(testQues2())

# print(testQ5("x_a"))





