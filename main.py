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
# question = "all"
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

    questionDictionary[fileName] = ""




def testQ3(func, fileName):
    from solutions.Q3Sol import q3 as answer

    fileArr = fileName.split('_')
    studentName = fileArr[0]

    res = ""

    if (func(50) == answer(50) and (func(1) == answer(1))):
        res += tableFormRecords("Question 3", "Correct")
        questionDictionary[fileName] = "Correct"
        gradeDictionary[studentName] = gradeDictionary[studentName] + 1
    else:
        res += tableFormRecords("Question 3", "Incorrect")
        questionDictionary[fileName] = "Incorrect"

    return res




def testQ4(func, fileName):
    from solutions.Q4Sol import q4 as answer

    fileArr = fileName.split('_')
    studName = fileArr[0]

    res = ""

    if (func(10) == answer(10) and func(2) == answer(2) and func(5) == answer(5)):
        res += tableFormRecords("Question 4", "Correct")
        questionDictionary[fileName] = "Correct"
        gradeDictionary[studName] = gradeDictionary[studName] + 1
    else:
        res += tableFormRecords("Question 4", "Incorrect")
        questionDictionary[fileName] = "Incorrect"

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
            res += tableFormHeading(fileArr[0])
        else:
            res += tableFormHeading("")
            
            
        if (fileArr[1] == "Q3"):
            res += (testQ3(func, f))
            

        if (fileArr[1] == "Q4"):
            res += (testQ4(func, f))

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

            res += (student + " : <strong>" + str((gradeDictionary[student]/NUMBER_OF_QUESTIONS)*100) + "%</strong>")
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
    with open('results.csv', mode='w', newline='') as results_file:
        results_writer = csv.writer(results_file)
        results_writer.writerow(["Student", "QuestionNumber", "Result"])
        for key in questionDictionary:
            studID = key.split('_')[0]
            questionNum = key.split('_')[1]
            result = questionDictionary[key]
            if (question == questionNum.lower()):
                results_writer.writerow([studID, questionNum, result])
            
            



def generateScoreSheet():
    with open('grades.csv', mode='w', newline='') as grades_file:
        grades_writer = csv.writer(grades_file)
        grades_writer.writerow(["Student", "TotalGrade", "FinalResult"])
        for key in gradeDictionary:
            score = ((gradeDictionary[key]/NUMBER_OF_QUESTIONS) * 100)
            result = ""
            if score >= 50:
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





