# All additional modules
from tkinter import *
import csv
import os
import shutil

#
#   MAIN MENU
#

# The main elements of the main menu are defined

root=Tk()
root.geometry("450x200")
root.title("Main Menu")
root.configure(bg="#33BFFF")

root.resizable(False,False)

labelMenu=Label(root,text="Welcome to the main menu")
labelMenu.pack(side=TOP)

#
#   FEEDBACK RECIEVER
#

# Reads all relevant feedback to an array to be added to the window, so that the user can see it
def getFeedback(username,listOfFiles):
    relevantFiles=[]
    feedback=[]

    # Searches all files that end with " - marks.csv" and looks for if there is an entry with the logged in user's username
    for i in range(0,len(listOfFiles)):
        currentFile=listOfFiles[i]+" - marks.csv"
        csvFile=open(currentFile,'r+')
        csvReader=csv.reader(csvFile)
        rows=list(csvReader)

        csvFile.close()

        # Adds all relevant files to an array
        for j in range(1,len(rows)):
            if username==rows[j][0]:
                relevantFiles.append(listOfFiles[i])
                break

    # Searches array of all relevant files for any feedback either directed to the logged in user, or directed to all users who have completed the test
    for i in range(0,len(relevantFiles)):
        currentFile=relevantFiles[i]+" - feedback.csv"
        csvFile=open(currentFile,'r+')
        csvReader=csv.reader(csvFile)
        rows=list(csvReader)

        csvFile.close()

        # Adds all feedback that is relevant to the user to an array
        for j in range(1,len(rows)):
            if username==rows[j][0] or rows[j][0]=="*":
                feedback.append(rows[j][1])

    print(relevantFiles)
    print(feedback)
    
    # Opens the feedback GUI for the user to view the feedback
    if len(feedback)!=0:
        displayFeedback(feedback)

    else:
        messagebox.showinfo("No feedback","You have no feedback")

# Displays feedback in a GUI
def displayFeedback(feedback):
    displayFeedback=Tk()
    displayFeedback.geometry("450x250")
    displayFeedback.title("Your feedback")
    displayFeedback.configure(bg="#9E004F")

    displayFeedback.resizable(False,False)

    labelFeedbackReciever=Label(displayFeedback,text="Feedback reciever")
    labelFeedbackReciever.pack(side=TOP)
    
    labelFunction=Label(displayFeedback,text="Your feedback:",bg="#9E004F",font=("Courier 10 underline"), borderwidth=0)
    labelFunction.place(x=20,y=22)

    # Text widget is used to insert feedback into the GUI to display it to the user
    displayedFeedback=Text(displayFeedback,width=50,height=10,wrap=WORD)
    displayedFeedback.place(x=20,y=44)

    # Button to close the GUI
    submitButton=Button(displayFeedback,text="Close",command=lambda: displayFeedback.destroy())
    submitButton.place(x=350,y=215)

    scrollbar=Scrollbar(displayFeedback)
    scrollbar.pack(side=RIGHT,fill=Y)

    displayedFeedback.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=displayedFeedback.yview)

    for i in range(0,len(feedback)):
        currentFeedback=feedback[i]+"\n\n"
        displayedFeedback.insert(END,currentFeedback)
#
#   FEEDBACK GIVER  
#

# Allows user to select target to give feedback to
def feedbackSelectorGUI():
    username="*"
    
    feedbackSelector=Tk()
    feedbackSelector.geometry("450x160")
    feedbackSelector.title("Feedback sender")
    feedbackSelector.configure(bg="#5900FF")

    feedbackSelector.resizable(False,False)

    labelFeedbackMenu=Label(feedbackSelector,text="Feedback sender")
    labelFeedbackMenu.pack(side=TOP)

    # Button to start the process to give specific student feedback
    specificButton=Button(feedbackSelector,width=15,height=3,wraplength=80,text="Give feedback to a specific student",command=lambda: getUsernamesAndTestNames("Specific",username))
    specificButton.place(x=10,y=40)

    # Button to start the process to give whole test feedback
    wholeButton=Button(feedbackSelector,width=15,height=3,wraplength=80,text="Give feedback on a whole test",command=lambda: getUsernamesAndTestNames("Test",username))
    wholeButton.place(x=320,y=40)

    # Button to close the GUI
    closeButton=Button(feedbackSelector,text="Close",command=lambda: feedbackSelector.destroy())
    closeButton.place(x=360,y=130)

# Gets usernames and test names for button functions in the next GUI
def getUsernamesAndTestNames(function,username):
    # Creates a list of all files in the current directory
    rootFile=os.path.abspath(os.curdir)
    listOfFiles=os.listdir(rootFile)
    print(listOfFiles)

    testNamesList=[]
    usernamesList=[]

    # Searches all files on the current directory for files ending in "grades.csv", as this indicates their is a fully created test
    # List of found test files are added to the array testNamesList
    for i in range(0,len(listOfFiles)):
        file=listOfFiles[i]
        if file[-10:]=="grades.csv":
            testNamesList.append(file[0:-13])

    print(testNamesList)

    # Starts the process to recieve feedback
    if function=="Recieve":
        getFeedback(username,testNamesList)
        
    # Starts the process to give feedback on an entire test
    if function=="Test":
        nameFeedbackReciever("Test",usernamesList,testNamesList)

    # Starts the process to give feedback to a specific student    
    if function=="Specific":
        csvFile=open('login.csv','r+')
        csvReader=csv.reader(csvFile)
        rows=list(csvReader)

        print(rows)
        
        # List of all usernames is created using the 'login.csv' file
        for i in range(1,len(rows)):
            username=rows[i][0]
            usernamesList.append(username)

        print(usernamesList)

        csvFile.close()

        nameFeedbackReciever("Specific",usernamesList,testNamesList)

# Displays either a list of usernames or a list of test names using a window
def printList(function,listToPrint):
    displayList=Tk()
    displayList.geometry("450x200")
    displayList.title("Username list")
    displayList.configure(bg="#5900FF")

    displayList.resizable(False,False)  

    scrollbar=Scrollbar(displayList)
    scrollbar.pack(side=RIGHT,fill=Y)

    # Text widget to insert the list that is to be displayed
    listToDisplay=Text(displayList,bg="#5900FF", width=450,wrap=WORD)
    listToDisplay.pack()

    listToDisplay.insert(END,listToPrint)
    
    listToDisplay.config(yscrollcommand=scrollbar.set,state=DISABLED)
    scrollbar.config(command=listToDisplay.yview)

    # Title is changed depending on the function, as this function is used when giving specific and whole feedback
    if function=="Specific":
        displayList.title("Username list")
        
    elif function=="Test":
        displayList.title("Test names list")

# Checks if inputted test name exists
def checkFeedbackTest(nameOfFeedbackTest,testNamesList):
    username="*"
    testName=nameOfFeedbackTest.get()

    # Checks the inputted test name exists and displays a relevant error message if it does not exist or the input is invalid
    if testName=="":
        messagebox.showerror("Invalid input","Please enter the test name into the input box")
    else:
        for i in range(0,len(testNamesList)):
            if testName==testNamesList[i]:
                giveFeedbackGUI(testName,username)
                break
            
            elif testName!=testNamesList[i] and i==len(testNamesList)-1:
                messagebox.showerror("Test has not been found","The entered test has not been found, please try again")


#Checks if inputted test name and username exists
def checkFeedbackSpecific(nameOfFeedbackTest,nameOfFeedbackUser,testNamesList,usernamesList):
    actualUsername=nameOfFeedbackUser.get()
    actualTestName=nameOfFeedbackTest.get()
    username=""
    testName=""
    
    # Checks if both the entered username and test name exist and are not invalid inputs. Provides relevant error messages.
    if actualUsername=="" or actualTestName=="":
        messagebox.showerror("Invalid input","Please make sure both input boxes are filled")

    else:
        for i in range(0,len(testNamesList)):
            if actualTestName==testNamesList[i]:
                testName=actualTestName
                break

            elif actualTestName!=testNamesList[i] and i==len(testNamesList)-1:
                messagebox.showerror("Test has not been found","The entered test has not been found, please try again")

        for j in range(0,len(usernamesList)):
            if actualUsername==usernamesList[j]:
                username=actualUsername
                break 

            elif actualUsername!=usernamesList[j] and j==len(usernamesList)-1:
                messagebox.showerror("Username has not been found","The entered username has not been found, please try again")

        if username==actualUsername and testName==actualTestName:
            giveFeedbackGUI(testName,username)
                

# Saves inputted feedback to the appropriate .csv file            
def saveFeedback(testName,username,feedback):
    testName=testName+" - feedback.csv"
    feedback=feedback.get(1.0,'end-1c')

    if feedback=="":
        messagebox.showerror("Invalid input","Please enter feedback into the input box")
        
    # Opens feedback file linked to the test, copies all the contents, adds to the contents, then re-adds the contents to the .csv file
    elif feedback!="":
        csvFile=open(testName)
        csvReader=csv.reader(csvFile)
        rows=list(csvReader)

        rows.append([username,feedback])

        csvFile.close()
        csvFile=open(testName,'w',newline='')
        csvWriter=csv.writer(csvFile)
        csvWriter.writerows(rows)

        csvFile.close()

        messagebox.showinfo("Feedback saved","Feedback has been added successfully")

# Creates and opens the GUI to give feedback    
def giveFeedbackGUI(testName,username):
    giveFeedbackGUI=Tk()
    giveFeedbackGUI.geometry("450x250")
    giveFeedbackGUI.title("Enter feedback to give")
    giveFeedbackGUI.configure(bg="#5900FF")

    giveFeedbackGUI.resizable(False,False)

    labelFeedbackSender=Label(giveFeedbackGUI,text="Feedback sender")
    labelFeedbackSender.pack(side=TOP)

    labelFunction=Label(giveFeedbackGUI,text="Enter feedback to give:",bg="#5900FF",font=("Courier 10 underline"), borderwidth=0)
    labelFunction.place(x=20,y=22)

    # Text widget to allow the user to enter feedback
    feedback=Text(giveFeedbackGUI,width=50,height=10,wrap=WORD)
    feedback.place(x=20,y=44)

    # Button to start the process to save the entered feedback
    submitButton=Button(giveFeedbackGUI,text="Submit",command=lambda: saveFeedback(testName,username,feedback))
    submitButton.place(x=350,y=215)

    scrollbar=Scrollbar(giveFeedbackGUI)
    scrollbar.pack(side=RIGHT,fill=Y)

    feedback.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=feedback.yview)

# Allows user to enter who the feedback is for
def nameFeedbackReciever(function,usernamesList,testNamesList):
    nameFeedbackReciever=Tk()
    nameFeedbackReciever.geometry("350x90")
    nameFeedbackReciever.configure(bg="#5900FF")

    nameFeedbackReciever.resizable(False,False)

    # Entry to allow the user to enter the name of the test to give feedback on
    nameOfFeedbackTest=Entry(nameFeedbackReciever,width=52)
    nameOfFeedbackTest.place(x=22,y=22)

    label1Function=Label(nameFeedbackReciever,text="Enter the name of the test:",bg="#5900FF",font=("Courier 10"), borderwidth=0)
    label1Function.place(x=22,y=5)

    # Button to display all compatible tests in the current directory
    print1Button=Button(nameFeedbackReciever,text="Print all test names",command=lambda: printList("Test",testNamesList))
    print1Button.place(x=30,y=52)
    
    # If feedback is being given for an entire test, less elements of the GUI are defined as they are unnecessary
    if function=="Test":
        # Submit button to start the check the inputs when giving whole test feedback
        submitButton=Button(nameFeedbackReciever,text="Submit",command=lambda: checkFeedbackTest(nameOfFeedbackTest,testNamesList))
        submitButton.place(x=270,y=52)
        
        nameFeedbackReciever.title("Test name to give feedback on")
        
    # If feedback is being given to a specific student, more elements of the GUI are defined as they are necessary to send the feedback to the specific user
    elif function=="Specific":
        nameFeedbackReciever.title("Username to give feedback to")
        nameFeedbackReciever.geometry("350x150")

        # Entry to allow the user to enter the username of the student to give feedback to
        nameOfFeedbackUser=Entry(nameFeedbackReciever,width=52)
        nameOfFeedbackUser.place(x=22,y=69)
        
        label2Function=Label(nameFeedbackReciever,text="Enter the name of a user:",bg="#5900FF",font=("Courier 10"), borderwidth=0)
        label2Function.place(x=22,y=52)

        # Submit button to start the check the inputs when giving specific student feedback 
        submitButton=Button(nameFeedbackReciever,text="Submit",command=lambda: checkFeedbackSpecific(nameOfFeedbackTest,nameOfFeedbackUser,testNamesList,usernamesList))
        submitButton.place(x=270,y=107)

        print1Button.place(x=30,y=107)

        # Button to display all usernames registered in the 'login.csv' file
        print2Button=Button(nameFeedbackReciever,text="Print all usernames",command=lambda: printList("Specific",usernamesList))
        print2Button.place(x=150,y=107)

#
#   TEST COMPLETING
#

# Reads the test csv file
def readTestFile(testName,username):
    # Contents of the test .csv file are read

    if testName[-4:]!=".csv":
        testFile=testName+".csv"
    else:
        testFile=testName

    readAllQuestions(testName,testFile,username)
        


# Checks that the test file exists
def checkFileName(testName,username):
    testName=testName.get()
    # Finds the current directory and adds the test name to the file path
    rootFile=os.path.abspath(os.curdir)
    file=rootFile+"\\"+testName+".csv"

    # Checks if there is a path to the file to see if it exists
    if os.path.isfile(file)==True:
        readTestFile(testName,username)
    elif os.path.isfile(file)==False:
        messagebox.showerror("File not found","The file has not been found, please try again")

# Adds new user test attempt to the marks file
def setMarkFile(username,testName,questions,answers):
    file=testName+" - marks.csv"
    csvFile=open(file,'a')
    newLine=username+",0,U\n"
    csvFile.write(newLine)
    csvFile.close()

    file=testName+" - marks.csv"
    csvFile=open(file,'r+')
    
    csvReader=csv.reader(csvFile)
    rows=list(csvReader)
    
    # Finds the last recoreded entry by the user, so that only the most recent test attempt by the user is modified
    lastAttemptByUser=1

    print(rows)
    
    for i in range(len(rows)-1,1,-1):
        if rows[i][0]==username:
            lastAttemptByUser=i
            break

    print(lastAttemptByUser)
    csvFile.close()

    testCompletion(testName,questions,answers,lastAttemptByUser,rows)
    
# Reads all questions and answers in the test file
def readAllQuestions(testName,testFile,username):
    questions=[]
    answers=[]
    temp=[]

    # Opens the test .csv file and reads the contents
    csvFile=open(testFile)
    csvReader=csv.reader(csvFile)
    rows=list(csvReader)

    # Adds all the questions into a list
    i=1
    while i!=len(rows):
        question=rows[i][0]
        questions.append(question)
        i=i+1

    print(questions)


    # Adds all the answers to a list of lists, because there can be mulitple answers linked to one question    
    i=1
    j=1
    while i!=len(rows):
        while j!=len(rows[i]):
            answer=rows[i][j]
            temp.append(answer)
            j=j+1
        answers.append(temp)
        temp=[]
        j=1
        i=i+1

    print(answers)

    # Adds the correct headings to the mark file, if they have not been added already
    openMarkOrFeedbackFile(testName+' - marks.csv',"Mark")

    # Adds a new test attempt into the mark file
    setMarkFile(username,testName,questions,answers)
    
# Checks the inputted answer against the actual answers
def checkAnswer(answer,answers,i,testName,rowOfEntry,rows):            
    file=testName+" - marks.csv"
    csvFile=open(file,'w',newline='')
    csvWriter=csv.writer(csvFile)

    correctAnswers=answers[i]

    print(rowOfEntry)

    j=0
    
    # Checks if the input answer matches the correct answer or answers
    while j!=len(correctAnswers):
        # If the answer is correct the user's most recent entry in the mark file will gain an additional mark
        if answer==correctAnswers[j]:
            rows[rowOfEntry][1]=int(rows[rowOfEntry][1])+1
            csvWriter.writerows(rows)
            print("correct")
            break

        # If the answer is incorrect, then the function re-adds the contents of the mark file
        elif answer!=correctAnswers[j] and j+1==len(correctAnswers):
            csvWriter.writerows(rows)
            print("wrong")
        j=j+1
            
    csvFile.close()

# Displays GUI that shows results of test
def ResultsGUI(grade,marks,username,testName,totalMarks):
    results=Tk()
    results.geometry("450x140")
    results.title("Results")
    results.configure(bg="#00FF6E")

    results.resizable(False,False)

    labelResultsMenu=Label(results,text="Your results")
    labelResultsMenu.pack(side=TOP)

    labelTestName=Label(results,bg="#00FF6E",text="TestName: "+testName)
    labelTestName.place(x=5,y=40)

    labelUsername=Label(results,bg="#00FF6E",text="Username: "+username)
    labelUsername.place(x=5,y=60)

    labelMarks=Label(results,bg="#00FF6E",text="Marks: "+str(marks)+"/"+str(totalMarks))
    labelMarks.place(x=340,y=40)

    percentage=100*float(marks)/float(totalMarks)

    labelPercent=Label(results,bg="#00FF6E",text="Percentage: "+str(percentage)+"%")
    labelPercent.place(x=340,y=60)

    labelGrade=Label(results,bg="#00FF6E",text="Grade: "+grade)
    labelGrade.place(x=340,y=80)

    # Button to close the GUI
    closeButton=Button(results,text="Close",command=lambda: results.destroy())
    closeButton.place(x=340,y=100)

    # Button to start the test completion process again with the same test
    tryAgainButton=Button(results,text="Try again",command=lambda: readTestFile(testName,username))
    tryAgainButton.place(x=10,y=100)
    

# Adds new grade to marks file and prepares results screen
def updateGrade(testName,rowOfEntry):
    markFile=testName+" - marks.csv"
    csvFile=open(markFile,'r+')
    csvReader=csv.reader(csvFile)
    rows=list(csvReader)

    csvFile.close()

    print(rows)
    
    # Finds the marks of the user's most recent test attempt
    marks=rows[rowOfEntry][1]
    print(marks)

    gradeFile=testName+" - grades.csv"
    csvFile=open(gradeFile,'r+')
    csvReader=csv.reader(csvFile)
    grades=list(csvReader)

    print(grades)

    grade=""
    i=0

    # Finds the grade based on the user's marks
    for i in range(0,5):
        if marks>=grades[1][i]:
            grade=grades[0][i]
            break
        else:
            i=i+1
            
    print(grade)

    csvFile.close()
    
    # Saves the new grade
    rows[rowOfEntry][2]=grade
    username=rows[rowOfEntry][0]

    csvFile=open(markFile,'w',newline='')
    csvWriter=csv.writer(csvFile)
    csvWriter.writerows(rows)

    csvFile.close()

    totalMarks=0
    
    testFile=testName+".csv"
    contents=open(testFile)
    fileContents=(contents)
    next(contents)

    print(fileContents)

    for row in fileContents:
        totalMarks=totalMarks+1

    print(totalMarks)
    
    ResultsGUI(grade,marks,username,testName,totalMarks)
    

# Updates the question box after an answer has been submitted
def updateQuestionBox(questionBox,questions,answerBox,answers,testName,rowOfEntry,rows):
    answer=answerBox.get(1.0,'end-1c')
    questionBox.config(state=NORMAL)

    currentQuestion=questionBox.get(1.0,'end-1c')

    questionBox.delete(1.0,END)

    i=0
    
    # Checks if the current question in the text widget matches the current question in the questions array. Updates the text box with the new question.            
    while i!=len(questions):
        if currentQuestion!=questions[i]:
            i=i+1
        elif currentQuestion==questions[i]:
            # Once the next question has been found the inputted answer is checked against the actual answer/answers
            checkAnswer(answer,answers,i,testName,rowOfEntry,rows)
            if i+1<len(questions):
                newQuestion=questions[i+1]
                questionBox.insert(END,newQuestion)
                break
            break

    # If the there are no more questions, the process to update the user's marks and grades, and display their results starts
    if i+1==len(questions):
        updateGrade(testName,rowOfEntry)
        
    if answer=="":
        messagebox.showerror("Error","Please enter your answer into the answer box")
        questionBox.delete(1.0,END)
        questionBox.insert(END,questions[i])

    answerBox.delete(1.0,END)
    
    questionBox.config(state=DISABLED)
    

# GUI for test completion
def testCompletion(testName,questions,answers,rowOfEntry,rows):
    completeWindow=Tk()
    completeWindow.geometry("450x250")
    completeWindow.title(testName)
    completeWindow.configure(bg="#00FF6E")

    completeWindow.resizable(False,False)

    scrollbar=Scrollbar(completeWindow)
    scrollbar.pack(side=RIGHT,fill=Y)

    questionLabel=Label(completeWindow,text="Question:",bg="#00FF6E",font=("Courier 10 underline"), borderwidth=0)
    questionLabel.place(x=20,y=0)

    # Text widget used to insert the question into the GUI so it is visible to the user
    questionBox=Text(completeWindow,width=50,height=4,wrap=WORD)
    questionBox.place(x=20,y=20)
    
    questionBox.insert(END,questions[0])

    questionBox.config(yscrollcommand=scrollbar.set,state=DISABLED)
    scrollbar.config(command=questionBox.yview)
    
    answerLabel=Label(completeWindow,text="Answer:",bg="#00FF6E",font=("Courier 10 underline"), borderwidth=0)
    answerLabel.place(x=20,y=100)

    # Text widget used to allow the user to input their answer
    answerBox=Text(completeWindow,width=50,height=4,wrap=WORD)
    answerBox.place(x=20,y=120)

    # Submit button to check if the inputted answer is correct and diplay the new question
    submitButton=Button(completeWindow,text="Submit",command=lambda: updateQuestionBox(questionBox,questions,answerBox,answers,testName,rowOfEntry,rows))
    submitButton.place(x=200,y=200)



#
#   TEST CREATOR
#

# Saves inputted grades to csv file
def saveGrades(grades,file,gradesData,gradeWindow):
    try:
        fileHandle=open(file,'r+')
        fileContent=fileHandle.read()
        if fileContent.strip()=='':
            fileHandle.write('A,B,C,D,E,F\n')
        for item in grades:
            fileHandle.write('{A},{B},{C},{D},{E},{F}'.format(**gradesData))
            fileHandle.write('\n')
        messagebox.showinfo("Success","Grades saved successfully")
        gradeWindow.destroy()
        fileHandle.close()

    except OSError:
        messagebox.showerror("Not saved","Grades not saved successfully, please try again")

# Gets inputted grades from GUI
def getGrades(A,B,C,D,E,F,file,gradeWindow):
    # Gets all the user's grades inputs and adds them to a dictionary
    grades=[]
    a=A.get(1.0,'end-1c')
    b=B.get(1.0,'end-1c')
    c=C.get(1.0,'end-1c')
    d=D.get(1.0,'end-1c')
    e=E.get(1.0,'end-1c')
    f=F.get(1.0,'end-1c')
    gradesData={'A':a,'B':b,'C':c,'D':d,'E':e,'F':f}
    grades.append(gradesData)

    # Checks if the user has entered inputs into all input boxes and ensures grade boundaries do not overlap incorrectly
    if len(a)!=0 and len(b)!=0 and len(c)!=0 and len(d)!=0 and len(e)!=0 and len(f)!=0:
        if a>=b>=c>=d>=e>=f:
            saveGrades(grades,file,gradesData,gradeWindow)
        else:
            messagebox.showerror("Grades not added","Please ensure the grade boundaries do not overlap")
    else:
        messagebox.showerror("Grades not added","Please fill all input boxes and try again")

# Opens the grade file and formats the headings
def openGradeFile(file,A,B,C,D,E,F,gradeWindow):
    csvFile=open(file,'r+')
    csvFile.write('A,B,C,D,E,F\n')
    fileRead=csvFile.read()

    for item in fileRead:
        csvFile.write('{A},{B},{C},{D},{E},{F}'.format(**item))
        csvFile.write('\n')
    csvFile.close()

    getGrades(A,B,C,D,E,F,file,gradeWindow)

# Opens the mark file and formats the headings
def openMarkOrFeedbackFile(fileName,fileType):
    csvFile=open(fileName,'r+')
    fileRead=csvFile.read()

    # Adds the correct headings to the mark file, if they have not been added already
    if fileRead.strip()=='' and fileType=="Mark":
        fileRead=csvFile.read()
        csvFile=open(fileName,'w+')
        csvFile.write('Username,Marks,Grades\n')
        
        print("headings have been written")

    # Adds the correct headings to the feedback file, if they have not been added already    
    elif fileRead.strip()=='' and fileType=="Feedback":
        fileRead=csvFile.read()
        csvFile=open(fileName,'w+')
        csvFile.write('Username,Feedback\n')

        print("headings have been written")
        
    else:
        print("headings are already written")

# Creates the grade, mark and feedback file by copying and renaming the "empty.csv" file
def gradeFileCreator(testName,A,B,C,D,E,F,gradeWindow):
    rootFile=os.path.abspath(os.curdir)
    gradeFileName=testName.strip(".csv")
    dst1File=gradeFileName+" - grades.csv"
    dst2File=gradeFileName+" - marks.csv"
    dst3File=gradeFileName+" - feedback.csv"
    rootFile=rootFile+"\\empty.csv"

    shutil.copy2(rootFile,dst1File)
    shutil.copy2(rootFile,dst2File)
    shutil.copy2(rootFile,dst3File)

    openGradeFile(dst1File,A,B,C,D,E,F,gradeWindow)
    openMarkOrFeedbackFile(dst2File,"Mark")
    openMarkOrFeedbackFile(dst3File,"Feedback")
    

# Outputs the total marks for a test when in adding grades GUI
def checkMarks(file):
    marks=0
    
    contents=open(file)
    fileContents=(contents)
    next(contents)

    for row in fileContents:
        marks=marks+1

    if marks!=0:
        messagebox.showinfo("Total marks",marks)
    else:
        messagebox.showerror("Error","The test is empty please re-create the test")
        openCreatedTest(file)

    contents.close()

# Grade boundaries GUI    
def endTest(closeWindow,file):
    gradeWindow=Tk()
    gradeWindow.geometry("300x150")
    gradeWindow.title("Add grade boundaries")
    gradeWindow.configure(bg="#1EFF00")

    gradeTitle=Label(gradeWindow,text="Add grade boundaries to the test")
    gradeTitle.pack(side=TOP)
    
    # Text widgets to allow the user to enter grade boundaries    
    entryAgrade=Text(gradeWindow,width=5,height=1)
    entryAgrade.place(x=20,y=45)

    entryBgrade=Text(gradeWindow,width=5,height=1)
    entryBgrade.place(x=125,y=45)

    entryCgrade=Text(gradeWindow,width=5,height=1)
    entryCgrade.place(x=230,y=45)

    entryDgrade=Text(gradeWindow,width=5,height=1)
    entryDgrade.place(x=20,y=95)

    entryEgrade=Text(gradeWindow,width=5,height=1)
    entryEgrade.place(x=125,y=95)

    entryFgrade=Text(gradeWindow,width=5,height=1)
    entryFgrade.place(x=230,y=95)

    gradeAlabel=Label(gradeWindow,bg="#1EFF00",text="A:")
    gradeAlabel.place(x=20,y=25)

    gradeBlabel=Label(gradeWindow,bg="#1EFF00",text="B:")
    gradeBlabel.place(x=125,y=25)

    gradeClabel=Label(gradeWindow,bg="#1EFF00",text="C:")
    gradeClabel.place(x=230,y=25)

    gradeDlabel=Label(gradeWindow,bg="#1EFF00",text="D:")
    gradeDlabel.place(x=20,y=75)

    gradeElabel=Label(gradeWindow,bg="#1EFF00",text="E:")
    gradeElabel.place(x=125,y=75)

    gradeFlabel=Label(gradeWindow,bg="#1EFF00",text="F:")
    gradeFlabel.place(x=230,y=75)

    # Button to display a message box with the total number of marks for the test
    checkButton=Button(gradeWindow,text="Check total marks",command=lambda: checkMarks(file))
    checkButton.place(x=20,y=123)

    # Button to start the process to save the grades to a .csv file
    submitButton=Button(gradeWindow,text="Submit",command=lambda: gradeFileCreator(file,entryAgrade,entryBgrade,entryCgrade,entryDgrade,entryEgrade,entryFgrade,gradeWindow))
    submitButton.place(x=230,y=123)
    
    gradeWindow.resizable(False,False)

    closeWindow.destroy()

# Displays window representation of the test csv file
def testPreview(file):
    previewWindow=Tk()
    previewWindow.geometry("450x250")
    previewWindow.title("Test preview")
    previewWindow.configure(bg="#1EFF00")

    test=open(file,'r+')
    testData=test.read()

    scrollbar=Scrollbar(previewWindow)
    scrollbar.pack(side=RIGHT,fill=Y)

    # Text widget to insert the contents of the .csv file, to display the test to the user
    testPreview=Text(previewWindow,bg="#1EFF00",width=450,wrap=WORD)
    testPreview.pack()

    testPreview.insert(END,testData)

    testPreview.config(yscrollcommand=scrollbar.set,state=DISABLED)
    scrollbar.config(command=testPreview.yview)

    test.close()



# Saves inputted questions and answers to the csv file
def saveTestData(csv,file,csvData):
    try:
        fileHandle=open(file,'r+')
        fileContent=fileHandle.read()
        
        # If the file is empty, the necessary headings are added
        if fileContent.strip()=='':
            fileHandle.write('Question,Answer\n')
            
        # Adds the questions and answers from the dictionary
        for item in csv: 
            fileHandle.write('{Question},{Answer}'.format(**csvData))
            fileHandle.write('\n')

        # Displays message box on success
        messagebox.showinfo("Success","Question and answers added successfully")

        fileHandle.close()
    except OSError:
        print('Can\'t write to file')
        
# Gets inputted question and answers         
def appendDetails(inputtedQuestion,inputtedAnswers,testFile):
    csv=[]
    # Gets inputted question and answer/answers
    question=inputtedQuestion.get(1.0,'end-1c')
    answers=inputtedAnswers.get(1.0,'end-1c')
    # Adds inputted question and answer/answers to a dictionary
    csvData={'Question':question,'Answer':answers}
    csv.append(csvData)

    if len(question)!=0 and len(answers)!=0:
        saveTestData(csv,testFile,csvData)
    else:
        messagebox.showerror("Questions and answers not added","Both text boxes must be filled, please try again")

# Deletes last entry when creating a test
def deleteLast(testFile):
    csvFile=open(testFile,'r+')
    csvReader=csv.reader(csvFile)
    rows=list(csvReader)
    csvFile.close()
    

    if len(rows)!=1:
        rows=rows[:-1]
        
        csvFile=open(testFile,'w',newline='')
        csvWriter=csv.writer(csvFile)
        csvWriter.writerows(rows)

        csvFile.close()

        messagebox.showinfo("Entry deleted","Last question and answers have been deleted")
    else:
        messagebox.showerror("Entry not deleted","There are no entries in the test")

# GUI to create a test
def appendTestFile(testFile):
    appendWindow=Tk()
    appendWindow.geometry("450x250")
    appendWindow.title("Create a test")
    appendWindow.configure(bg="#1EFF00")

    appendWindow.resizable(False,False)
    
    labelTitle=Label(appendWindow,text="Add questions and answers to the test")
    labelTitle.pack(side=TOP)

    labelAddQuestion=Label(appendWindow,text="Add a question:",bg="#1EFF00",font=("Courier 10 underline"), borderwidth=0)
    labelAddQuestion.place(x=22,y=25)
    
    # Text widget to allow the user to enter a question
    entryAddQuestion=Text(appendWindow,width=50,height=3)
    entryAddQuestion.place(x=22,y=40)

    labelAddAnswer=Label(appendWindow,text="Add answers:",bg="#1EFF00",font=("Courier 10 underline"), borderwidth=0)
    labelAddAnswer.place(x=22,y=100)

    # text widget to allow the user to enter an answer/answers
    entryAddAnswer=Text(appendWindow,width=50,height=5)
    entryAddAnswer.place(x=22,y=115)

    # Submit button to start the process to check and save the inputted question and answer/answers
    submitButton=Button(appendWindow,text="Submit",width=8,command=lambda: appendDetails(entryAddQuestion,entryAddAnswer,testFile))
    submitButton.place(x=22,y=210)

    # Button to display the contents of the test in a window
    previewButton=Button(appendWindow,text="Preview",width=8,command=lambda: testPreview(testFile))
    previewButton.place(x=120,y=210)

    # Button to delete the last entry in the test file
    deleteButton=Button(appendWindow,text="Delete last",width=8,command=lambda: deleteLast(testFile))
    deleteButton.place(x=260,y=210)

    # Button to start the adding grades process
    finishButton=Button(appendWindow,text="Finish",width=8,command=lambda: endTest(appendWindow,testFile))
    finishButton.place(x=360,y=210)

# Opens created test csv file
def openCreatedTest(testFile):
    csvFile=open(testFile,'r+')
    csvFile.write('Question,Answer\n')
    file=csvFile.read()
    
    for item in file:
        csvFile.write('{Question},{Answer}'.format(**item))
        csvFile.write('\n')
    csvFile.close()

    appendTestFile(testFile)

# Creates test csv file
def testFileCreator(testName,fileCreator,*gradeAppend):
    # Creates the file path for the test to be created
    csv=".csv"
    userTestName=testName.get()
    rootFile=os.path.abspath(os.curdir)
    dstFile=str(rootFile)+str("\\")+str(userTestName)+str(gradeAppend)
    dstFile=dstFile.strip('()')
    dstFile=dstFile+str(csv)

    # Gets the list of all files on the current directory
    nameToCheck=str(userTestName)+str(csv)
    fileExists=False
    listOfFiles=os.listdir(rootFile)

    # Checks if the file path of the test to be created matches the path of one of the files on the directory. If so, then the name already checks.
    for i in range(0,len(listOfFiles)):
        file=listOfFiles[i]
        if file==nameToCheck:
            fileExists=True
            break
        
    rootFile=rootFile+"\\empty.csv"
    print(dstFile)

    # Creates the test if the file does not already exist and the input is not empty
    if userTestName!="" and fileExists==False:
        shutil.copy2(rootFile,dstFile)

        fileCreator.destroy()

        openCreatedTest(dstFile)

    elif fileExists==True:
        messagebox.showerror("Test not created",
                             "This test already exists, please enter another name")

    else:
        messagebox.showerror("Test not created",
                             "The test has not been created, please make sure all input boxes are filled and try again")
   



# GUI to name test file    
def nameTestFile(title,function,username):
    fileCreator=Tk()
    fileCreator.geometry("450x42")
    fileCreator.title(title)
    fileCreator.configure(bg="#1EFF00")

    fileCreator.resizable(False,False)

    labelCreator=Label(fileCreator,text="Enter the name of a test:",bg="#1EFF00",font=("Courier 10"), borderwidth=0)
    labelCreator.place(x=22,y=5)

    # Entry to allow the user to enter the test name
    nameOfTestBox=Entry(fileCreator,width=52)
    nameOfTestBox.place(x=22,y=20)

    # Changes function of the submit button based on the arguements in the function call
    if function=="Create":
        submitButton=Button(fileCreator,text="Submit",command=lambda:testFileCreator(nameOfTestBox,fileCreator))
        submitButton.place(x=375,y=13)
        
    elif function=="Complete":
        submitButton=Button(fileCreator,text="Submit",command=lambda:checkFileName(nameOfTestBox,username))
        submitButton.place(x=375,y=13)

        fileCreator.configure(bg="#00FF6E")

#
#   SECONDARY MENU
#

# Creates the secondary menu GUI
def secondaryMenu(username,adminStatus):
    sec=Tk()
    sec.geometry("450x50")
    sec.title("Features Menu")
    sec.configure(bg="#2019F7")

    sec.resizable(False,False)

    labelSecMenu=Label(sec,text="Welcome to the program")
    labelSecMenu.pack(side=TOP)

    buttonComplete=Button(sec,text="Complete a test",command=lambda: nameTestFile("Complete a test","Complete",username))
    buttonComplete.place(x=10, y=20)

    buttonRFeedback=Button(sec,text="Recieve feedback",command=lambda: getUsernamesAndTestNames("Recieve",username))
    buttonRFeedback.place(x=330,y=20)

    # Defines additional buttons if the account logged in has admin status
    if adminStatus==True:
        sec.geometry("450x200")
        buttonGFeedback=Button(sec,text="Give feedback",command=lambda: feedbackSelectorGUI())
        buttonGFeedback.place(x=330,y=150)

        buttonCreate=Button(sec,text="Create a test",command=lambda: nameTestFile("Create a test","Create",username))
        buttonCreate.place(x=10,y=150)

# Opens login csv file
def openLogin(buttonOutput):
    csvFile=open('login.csv')
    csvFileContent=(csvFile)
    next(csvFile)

    databaseList=[]
    
    # Reads the contents of the 'login.csv' file into a dictionary
    for row in csvFileContent:
        database=row.strip().split(",")
        heading=['Username','Password','Admin']
        data=zip(heading,database)
        DataDict=dict(data)
        databaseList.append(DataDict)

    # Starts either the login or registration process as this function is assigned to both buttons
    if buttonOutput=="startLogin":
        loginFunction(databaseList)
    elif buttonOutput=="startRegister":
        registerFunction()
#
#   REGISTRATION
#

# Gets inputted username and password and checks if is valid
def registerAccount(inputtedUsername,inputtedPassword,inputtedAdmin):
    login=[]
    username=inputtedUsername.get()
    password=inputtedPassword.get()
    admin=inputtedAdmin.get()

    csvFile=open('login.csv','r+')
    csvReader=csv.reader(csvFile)
    rows=list(csvReader)
    csvFile.close()

    usernameTaken=False
    usernameLength=False
    passwordLength=False
    userFirstChar=True
    passFirstChar=True

    for i in range(1,len(rows)):
        if username==rows[i][0]:
            usernameTaken=True
            break

    if len(password)>=int(8):
        passwordLength=True
        
    if len(username)>=int(8):
        usernameLength=True

    if ord(username[:1])>=int(48) and ord(username[:1])<=int(57):
        userFirstChar=False

    if ord(password[0])>=int(48) and ord(password[0])<=int(57):
        passFirstChar=False

    # Checks if the inputted username valid and does not already exist, and checks if the inputted password is valid. If these conditions are not met a relevant error message is displayed.
    if username!="" and password!="" and usernameTaken==False and usernameLength==True and passwordLength==True and userFirstChar==True and passFirstChar==True:
        logindata={'Username':username,'Password':password,'Admin':admin}
        login.append(logindata)
        # Saves login details if the inputted login details are valid
        saveLoginData(login)
    elif usernameTaken==True:
        messagebox.showerror("Username already exists","Username already exists, please enter a new username")
    elif usernameLength==False:
        messagebox.showerror("Username is too short","Username must be atleast 8 characters")
    elif passwordLength==False:
        messagebox.showerror("Password is too short","Password must be atleast 8 characters")
    elif userFirstChar==False:
        messagebox.showerror("Invalid username","Username must not start with a number")
    elif passFirstChar==False:
        messagebox.showerror("Invalid password","Password must not start with a number")
    else:
        messagebox.showerror("Registration unsuccessful","Registration unsuccessful, please try again")

# Saves inputted username and password
def saveLoginData(login):
    try:
        fileHandle=open('login.csv','r+')
        fileContent=fileHandle.read()
        # Adds headings to the file if they don't already exist
        if fileContent.strip()=='':
            fileHandle.write('Username,Password,Admin\n')
        # Writes the new login details using the necessary feedback
        for item in login:
            fileHandle.write('{Username},{Password},{Admin}'.format(**item))
            fileHandle.write('\n')
        fileHandle.close()
        
        messagebox.showinfo("Registration successful","Login details saved")
    except OSError:
        print('Can\'t write to file')


# GUI for account registration
def registerFunction():
    registerWindow=Tk()
    registerWindow.geometry("450x200")
    registerWindow.title("Registration")
    registerWindow.configure(bg="#FF2929")

    labelRegistration=Label(registerWindow,text="Registration")
    labelRegistration.pack(side=TOP)

    registerWindow.resizable(False,False)

    labelUsername=Label(registerWindow, text="Username:*",bg="#FF2929",font=("Courier 10 underline"), borderwidth=0)
    labelUsername.place(x=20,y=20)
    
    # Entry to allow the user to enter a username
    usernameBox=Entry(registerWindow,width=67)
    usernameBox.place(x=20, y=40)

    labelPassword=Label(registerWindow, text="Password:*",bg="#FF2929",font=("Courier 10 underline"), borderwidth=0)
    labelPassword.place(x=20,y=80)

    # Entry to allow the user to enter a password
    passwordBox=Entry(registerWindow,width=67,show="*")
    passwordBox.place(x=20,y=100)

    labelAdmin=Label(registerWindow,text="Admin code:",bg="#FF2929",font=("Courier 10 underline"), borderwidth=0)
    labelAdmin.place(x=20,y=130)

    # Entry to allow the user to enter an admin code
    adminBox=Entry(registerWindow,width=20)
    adminBox.place(x=20,y=150)

    # Button to check and save the inputted login details
    buttonRegister=Button(registerWindow,text="Register",command=lambda :registerAccount(usernameBox,passwordBox,adminBox))
    buttonRegister.place(x=300,y=150)

#
#   LOGIN
#

# Login GUI
def loginFunction(databaseList):
    loginWindow=Tk()
    loginWindow.geometry("450x200")
    loginWindow.title("Login")
    loginWindow.configure(bg="#FFA21F")

    labelLogin=Label(loginWindow,text="Login")
    labelLogin.pack(side=TOP)

    loginWindow.resizable(False,False)

    labelUsername=Label(loginWindow, text="Username:*",bg="#FFA21F",font=("Courier 10 underline"), borderwidth=0)
    labelUsername.place(x=20,y=20)

    # Entry to allow the user to enter a username
    usernameBox=Entry(loginWindow,width=67)
    usernameBox.place(x=20, y=40)

    labelPassword=Label(loginWindow, text="Password:*",bg="#FFA21F",font=("Courier 10 underline"), borderwidth=0)
    labelPassword.place(x=20,y=80)

    # Entry to allow the user to enter a password
    passwordBox=Entry(loginWindow,width=67,show="*")
    passwordBox.place(x=20,y=100)

    # Button to check the inputted login details
    buttonLogin=Button(loginWindow,text="Login",command=lambda :loginAccount(usernameBox,passwordBox,loginWindow,databaseList))
    buttonLogin.pack(side=BOTTOM, pady=10)

# Gets inputted login details and checks them
def loginAccount(inputtedUsername,inputtedPassword,loginWindow,databaseList):   
    username=inputtedUsername.get()
    password=inputtedPassword.get()
    loginStatus=False
    adminStatus=False
    for i in databaseList:
        # Checks if the inputted login details are ccorrect
        if i['Username']==username and i['Password']==password:
            messagebox.showinfo("Login successful","Login successful")
            loginStatus=True
            loginWindow.destroy()
            # Opens secondary menu with admin features if the registered admin code is correct
            if i['Admin']=='testadmin':
                adminStatus=True
    if loginStatus==True:
        secondaryMenu(username,adminStatus)
    else:
        messagebox.showerror("Login attempt failed","Login attempt failed, please try again")

#
#   GUIDE
#

# Creates window with 'guide.txt's contents
def openGuide():
    guideWindow=Tk()
    guideWindow.geometry("450x200")
    guideWindow.title("Guide")
    guideWindow.configure(bg="#EAFF00")

    guideWindow.resizable(False,False)
    
    textFile=open('guide.txt')
    text=textFile.read()

    scrollbar=Scrollbar(guideWindow)
    scrollbar.pack(side=RIGHT,fill=Y)

    # Text widget to insert the contents of the 'guide.txt' file into the window so that it can be displayed
    textGuide=Text(guideWindow,bg="#EAFF00", width=450,wrap=WORD)
    textGuide.pack()

    textGuide.insert(END,text)
    
    textGuide.config(yscrollcommand=scrollbar.set,state=DISABLED)
    scrollbar.config(command=textGuide.yview)

    textFile.close()

#
#   MAIN MENU BUTTONS
#

# Main menu buttons are defined and the window is opened

buttonRegisteration=Button(root,text="Register a new\n account",command=lambda: openLogin("startRegister"))
buttonRegisteration.place(x=10, y=20)

buttonLogin=Button(root,text="Login with an\n exisiting account",command=lambda: openLogin("startLogin"))
buttonLogin.place(x=330,y=20)

buttonEnd=Button(root,text="Exit the program",command=lambda: os._exit(0))
buttonEnd.place(x=330,y=150)

buttonGuide=Button(root,text="Guide on how to use this program",bg="#33BFFF",font=("Courier 10 underline"), borderwidth=0, command=openGuide)
buttonGuide.place(x=10,y=150)

root.mainloop()
