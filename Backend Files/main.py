
=======
# TODO drop classes without meeting days/room numbers? not sure how to reference empty matrix cell
# if dirtyCLM[x][15] == '':
#   print('skipped class with no room number')
# else:
#   CourseListMatrix[x][6] = dirtyCLM[x][15]
# TODO figure out why column titles on the es iteration are overwritten

# import pandas a powerful data science module for python
import pandas as pd

# method for creating hardcoded input
def hardinput():
    # 2d array of courses. Each Row is a course, and each column contains information about the course
    hardcourseinput = [["COSC480", "Topics in Computer Science", "01", "SH", "165",
                        "MW", "2:40:00PM-4:30:00PM"],
                       ["COSC480", "Topics in Computer Science", "02", "SH", "165",
                        "TR", "2:00:00PM-3:50:00PM"],
                       ["ANTH340", "Cultural Anthropology", "01", "AAW", "215",
                        "MWF", "8:00:00AM-9:10:00AM"],
                       ["ARTH465", "Topics in Art History", "01", "MH", "151",
                        "TR", "12:00:00PM-1:50:00PM"]]

    hardscheduleinput = [['MWF', '800', '12/10/18', '900', '1115'],
                         ['MW-', '1440', '12/12/18', '1400', '1615'],
                         ['TR-', '1200', '12/13/18', '1400', '1615'],
                         ['TR-', '1400', '12/10/18', '1900', '2115']]

# fill a data frame with the CourseList(cl) and ExamSchedule(es)
# user will feed program this adress
dfcl = pd.read_excel('C:\\Users\\mason\\PycharmProjects\\480MajorProjects\\Input Test Files\\cl.xlsx')
dfes = pd.read_excel('C:\\Users\\mason\\PycharmProjects\\480MajorProjects\\Input Test Files\\es.xlsx')

# print to make sure data is good
# print(dfcl)
# print(dfes)

dirtyCLM = dfcl.as_matrix(columns=None)

# in our matrix the important data can be found in the columns as follows
# Course Number      - Column 0
# Course Title       - Column 1
# Course Number      - Column 5
# Class Meeting Time - Column 9
# Class Meeting Days - Column 13
# Building Code      - Column 14
# Room Number        - Column 15
# every row is new class

# munge
w, h = len(dfcl.columns), len(dfcl.index);
CourseListMatrix = [[0 for x in range(w)] for y in range(h)]

# starting with header row because we know that data
CourseListMatrix[0] = [['Course Number'], ['Course Title'], ['Section Number'], ['Class Meeting Time'], ['Class Meeting Days'], ['Building Code'], ['Room Number']]

# now have to iterate through the dirty matrix on proper columns to fill CourseListMatrix
for x in range(len(dfcl.index)):
    CourseListMatrix[x][0] = dirtyCLM[x][0]
    CourseListMatrix[x][1] = dirtyCLM[x][1]
    CourseListMatrix[x][2] = dirtyCLM[x][5]
    CourseListMatrix[x][3] = dirtyCLM[x][9]
    CourseListMatrix[x][4] = dirtyCLM[x][13]
    CourseListMatrix[x][5] = dirtyCLM[x][14]
    CourseListMatrix[x][6] = dirtyCLM[x][15]
    print(CourseListMatrix[x][0], CourseListMatrix[x][1], CourseListMatrix[x][2], CourseListMatrix[x][3], CourseListMatrix[x][4], CourseListMatrix[x][5], CourseListMatrix[x][6])
print()
print()
print()
# now for ExamSchedule(es)
dirtyESM = dfes.as_matrix(columns=None)
w, h = len(dfes.columns), len(dfes.index);
ExamScheduleMatrix = [[0 for x in range(w)] for y in range(h)]
ExamScheduleMatrix[0] = [['Exam Date'], ['Exam Begin Time'], ['Exam End Time']]
# not sure why the column titles are overwritten on es iterations but not cl iterations ¯\_(ツ)_/¯
# for now just hard coding a print of the first row before it gets overwritten by for loop
print(ExamScheduleMatrix[0])
for x in range(len(dfes.index)):
    ExamScheduleMatrix[x][0] = dirtyESM[x][2]
    ExamScheduleMatrix[x][1] = dirtyESM[x][3]
    ExamScheduleMatrix[x][2] = dirtyESM[x][4]
    print(ExamScheduleMatrix[x][0], ExamScheduleMatrix[x][1], ExamScheduleMatrix[x][2])

    
# Assign dates, put into output file

T = []
T.append(["M-----",	800, "12/10/18",900,1115])
T.append(["--W---",	800,"12/10/18",900,	1115])



def ConvertTime (i):
    temp = (str)(i)
    return temp[:1] + ":" + temp[1:]

print(ConvertTime(900))    
