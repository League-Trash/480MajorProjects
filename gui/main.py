# code description: This program takes in an exam schedule file and a course schedule file and outputs a file containing
#  the course and it's assigned exam period.


# Imports:
import getpass  # Used for making the initial directory when browsing, be the Documents instead of C drive
import pandas as pd # pandas will be used to handle data conversion from excel file to matrix and then matrix to either excel file or csv
import os # os will be used to open the file on the computer
import re # re will be used to compare strings in course input
import ctypes
import tkinter as tk
from tkinter import filedialog  # used for handling browsing files
from tkinter import ttk


# Global Variables
CourseScheduleMatrix = [[0][0]] # CourseScheduleMatrix will be used to hold all important information from the course file
ExamScheduleMatrix = [[0][0]] # ExamScheduleMatrix will be used to hold all the important information from the exam file
output = []  # output will be used to hold courses and their assigned exam time
file_output_name = "" # file_output_name will be used to hold the file location of the output
uploaded_file_name_1_str = ''
uploaded_file_name_2_str = ''
# These must be global for the sake of enabling/disabling based on if files are uploaded
save_output_button = 0
display_output_button = 0

# Display_output will open up the file on the computer for the user to view
def display_output():
    # This line brings in the global variable file_output_name
    global file_output_name
    # This if statement is true when file_output_name contains a file location and is not empty
    if(file_output_name != ""):
        # This line calls treatedSelectedAddress to translate the file location into one that can be used by the program
        treatedName = treatSelectedAddress(file_output_name)
        # This line opens the file on the computer
        os.startfile(treatedName)
    else:
        ctypes.windll.user32.MessageBoxW(0, "Please make sure you save before you attempt to "
                                            "display the output.", "Error", 1)


# Used by course upload button to open a file browser
def upload_callback():
    # This line opens the file browser for the user to select the course schedule
    CourseList_Input = filedialog.askopenfile(mode='rb', initialdir='/', title='Select a file',
                                   filetypes=( ("Excel files", "*.xlsx"), ("CSV files", "*.csv")))
  
   # updates the field next to the button to display filename you just uploaded
    global uploaded_file_name_1_str
    uploaded_file_name_1_str.set(CourseList_Input.name.split('/')[-1])

    # Time to handle disabling/enabling buttons based on what you've uploaded
    if uploaded_file_name_2_str.get() != '':
        save_output_button['state'] = 'normal'
        # display_output_button['state'] = 'normal' #This goes in the Save Output button now

    # This line calls the CLexcelToMatrix method to take in the course input and put the data into the CourseScheduleMatrix Matrix
    CLexcelToMatrix(CourseList_Input)


# Used by exam schedule upload buttons to open a file browser
def upload_callback2():
    # This line opens the file browser for the user to select the exam schedule
    ExamSchedule_Input = filedialog.askopenfile(mode='rb', initialdir='/', title='Select a file',
                                   filetypes=( ("Excel files", "*.xlsx"), ("CSV files", "*.csv")))
  
  # updates the field next to the button to display filename you just uploaded
    global uploaded_file_name_2_str
    uploaded_file_name_2_str.set(ExamSchedule_Input.name.split('/')[-1])  # so it doesnt show entire path

    # Handle disbling/enabling buttons based on what you've uploaded
    if uploaded_file_name_1_str.get() != '':
        save_output_button['state'] = 'normal'
        # display_output_button['state'] = 'normal'
        
    # This line calls the ESexcelToMatrix method to take in the exam schedule input and put the data into the ExamScheduleMatrix Matrix
    ESexcelToMatrix(ExamSchedule_Input)


# This is going to open a file browser
# and the user will specify where they want the output to be saved to.
def save_output():
    if len(CourseScheduleMatrix) == 1 or len(ExamScheduleMatrix) == 1: #if either matrix is empty
        ctypes.windll.user32.MessageBoxW(0, "Please make sure you have both files inputted to the program before "
                                            "you save.", "Error", 1)
    else:
        # This line brings in the global variable file_output_name
        global file_output_name
        # This line opens up a file browser and lets the user decide where the output file will be saved
        file_output_name = filedialog.asksaveasfile(mode='w', title='Save output', defaultextension=".",
                                                    filetypes=(("Excel files", "*.xlsx"), ("CSV files", "*.csv")))
        
        # Enable 'Display/Save Output...' button once the output has been saved.
        # If save dialog was opened and closed without saving, display button is not enabled.
        if file_output_name is not None:
             display_output_button['state'] = 'normal'
        
        # This line calls on the exam_assignment method to use CourseScheduleMatrix and ExamScheduleMatrix matrixes to create the output data
        exam_assignment()
        # This line calls the output_writing method to output the data to the file location the user selected
        output_writing(file_output_name)


# Called when info button is pressed
# Prints the INFO section of the README file
def info_callback():
    global info_popup  # This must be global so we can check if it's open
    info_popup = tk.Toplevel()
    info_popup['padx'] = 20
    # popup['pady'] = 20
    info_popup.configure(bg='grey95')
    info_popup.iconbitmap(seahawk_icon_path)
    info_popup.wm_title("Information")

    popup_text = ""
    f = open(README_path, 'r')
    lines = f.readlines()
    for line in lines:
        if line.__contains__('HELP'):  # stop after reaching the help section
            break
        if not line.__contains__('====='):  # so it doesn't include the ===ABOUT=== line in the file.
            popup_text += line
    f.close()
    # msg_width = info_popup.winfo_width() - 40
    popup_message = tk.Message(info_popup, text=popup_text, width=400, anchor='center', bg='grey95')

    title_message = tk.Message(info_popup, text="St. Mary's College of Maryland Exam Scheduler", width=400, anchor='center', bg='grey95')
    title_message.config(font=('calibri', 14), bg='grey95')

    seperator = ttk.Separator(info_popup, orient='horizontal')

    button1 = tk.Button(info_popup, text="Close", command=info_popup.destroy)

    title_message.grid(row=0, sticky='n')
    seperator.grid(row=1, column=0, columnspan=2, sticky='ew')
    popup_message.grid(row=2)
    button1.grid(row=3, pady=(0, 20))

    info_popup.focus()
    info_popup.rowconfigure(2, weight=2, minsize=300)
    info_popup.columnconfigure(0, weight=2, minsize=300)
    info_popup.mainloop()


# This function handles a pressed info or help button
# If the window indicated is open, it brings it to the front and focus
# If it's not open yet, it creates it. This is to prevent duplicate windows
def open_popup(pressed):
    if pressed == 'info':
        if (info_popup is not None) and info_popup.winfo_exists():
            # info popup is open
            info_popup.lift()
            info_popup.focus()
        else:
            # info popup isn't open
            info_callback()
    elif pressed == 'help':
        if (help_popup is not None) and help_popup.winfo_exists():
            # help_popup is open
            help_popup.lift()
            help_popup.focus()
        else:
            # help_popup isn't open
            help_callback()


# Called when help button is pressed
# Prints the HELP section of the README file
def help_callback():
    global help_popup
    help_popup = tk.Toplevel()
    help_popup['padx'] = 20
    help_popup.configure(bg='grey95')
    help_popup.iconbitmap(seahawk_icon_path)
    help_popup.wm_title("Help")

    popup_text = ""
    f = open(README_path, 'r')
    lines = f.readlines()
    HELP_flag = False
    messages = []
    for line in lines:
        if line.__contains__('HELP'):
            HELP_flag = True
        if HELP_flag and not line.__contains__('===='):
            popup_text += line
            if line.__contains__(':'):
                messages.append(tk.Message(help_popup, text=line, width=350, anchor='center', bg='grey95',
                                           font=('calibri', 10, 'bold'), bd=-7))
            else:
                messages.append(tk.Message(help_popup, text=line, width=350, anchor='center', bg='grey95', bd=-5))

    f.close()
    # popup_message = tk.Message(help_popup, text=popup_text, width=400, anchor='center', bg='grey95')

    # popup_message.grid()
    title_message = tk.Message(help_popup, text="St. Mary's College of Maryland Exam Scheduler", width=400,
                               anchor='center', bg='grey95')
    title_message.config(font=('calibri', 14), bg='grey95')

    seperator = ttk.Separator(help_popup, orient='horizontal')

    title_message.grid(row=1, sticky='n')
    seperator.grid(row=2, column=0, sticky='ew')

    for m in messages:
        m.grid(sticky='w')
    button1 = tk.Button(help_popup, text="Close", command=help_popup.destroy)
    button1.grid(pady=(20, 20))
    help_popup.columnconfigure(0, weight=2, minsize=25)
    help_popup.mainloop()


# The ESexcelToArray method will take in the information from the exam schedule file
#  and put the data into the ExamScheduleMatrix matrix
def ESexcelToMatrix(fa):
    # This line takes in the information from the exam schedule excel file and puts it into a pandas' data frame
    dfes = pd.read_excel(treatSelectedAddress(fa))
    # This line brings in the glabal matrix ExamScheduleMatrix
    global ExamScheduleMatrix
    # This line sets ExamScheduleMatrix as a matrix containing the data in the pandas dataframe
    ExamScheduleMatrix = dfes.as_matrix(columns=None)


# The ESexcelToArray method will take in the important information from the course schedule file
#  and put the data into the CourseScheduleMatrix matrix
def CLexcelToMatrix(fa):
    # This line takes in the information from the course schedule excel file and puts it into a pandas' data frame
    dfcl = pd.read_excel(treatSelectedAddress(fa))
    # This line creates a matrix dirtyCLM that contains all the information from the course excel file
    dirtyCLM = dfcl.as_matrix(columns=None)
    # This line defines the width and height as 7 and length of the course information dataframe
    w, h = 7, len(dfcl.index)
    # This line creates a matrix of size w, h
    CourseListMatrix = [[0 for x in range(w)] for y in range(h)]
    # This variable will be used to hold the current course location in the CourseListMatrix
    course_location = 0
    # This for loop goes through the dirtyCLM matrix
    for x in range(len(dfcl.index)):
        # This try/exempt block handles Atrribute and Type Errors
        try:
            # This variable will be used to check if the course time is not 0 or blank
            ct = dirtyCLM[x][9]
            # This line checks if the course time is not 0 or blank
            if (ct > 0 and ct != None):
                # This line gets the end date of the course
                ed = dirtyCLM[x][8]
                # This line gets the end date as a string in the Year-Month-Day format
                end_d = ed.strftime('%Y-%m-%d')
                # This line gets the month out of the end date of a course
                end_date = end_d[5:7]
                # These if statements check to see if the courses end on the last month of the semester
                # if they do, all important information is put into the CourseListMatrix
                # 0 - Course Number, 1 - Course Title, 2 - Section Title, 3 - Course Start Time, 4 -Course Meeting days
                # 5 - Building Code, 6 - Room Number
                if re.match(r'12', end_date) or re.match(r'11', end_date) or re.match(r'04', end_date) or re.match(r'05', end_date):
                    CourseListMatrix[course_location][0] = dirtyCLM[x][0]
                    CourseListMatrix[course_location][1] = dirtyCLM[x][1]
                    CourseListMatrix[course_location][2] = dirtyCLM[x][5]
                    CourseListMatrix[course_location][3] = dirtyCLM[x][9]
                    CourseListMatrix[course_location][4] = dirtyCLM[x][13]
                    CourseListMatrix[course_location][5] = dirtyCLM[x][14]
                    CourseListMatrix[course_location][6] = dirtyCLM[x][15]
                    course_location += 1
        except AttributeError:
            cl = 0
        except TypeError:
            cl = 0
    # This line brings in the CourseScheduleMatrix matrix
    global CourseScheduleMatrix
    # This line sets CourseScheduleMatrix equal to CourseListMatrix
    CourseScheduleMatrix = CourseListMatrix


# The treatSelectedAddress method takes in a file address and cleans it up so it can be used in Python
def treatSelectedAddress(fileAddress):
    strFileAddress = fileAddress.name
    strFileAddress = strFileAddress.replace("/", "\\\\")
    return strFileAddress


# Method that takes user-provided course and exam schedules,
# and assigns courses exam times based on provided exam schedule
# Output: Matrix containing exam information for every applicable course
def exam_assignment():
    global CourseScheduleMatrix
    global ExamScheduleMatrix
    global output

    for x in range(len(CourseScheduleMatrix)):  # for each course in course schedule
        closest_time = None  # reset the closest exam time for each course

        #[4] Course meeting days
        #[3] Course start time
        #[0] Exam course meeting days
        #[1] Exam course start time

        for y in range(len(ExamScheduleMatrix)):  # for each exam time in exam schedule
            # if course meeting days match the exam schedule course meeting days,
            # and course start time matches the exam schedule course start time
            if CourseScheduleMatrix[x][4] == ExamScheduleMatrix[y][0] and CourseScheduleMatrix[x][3] == ExamScheduleMatrix[y][1]:
                #[0]  # course number
                #[1]  # course title
                #[2]  # section number 
                #[3]  # building code (5 on scheduleMatrix)
                #[4]  # room number (6 on scheduleMatrix)
                #[5]  # exam date (2 on scheduleMatrix)
                #[6]  # exam start time (3 on scheduleMatrix)
                #[7]  # exam end time (4 on scheduleMatrix)
                output.append([CourseScheduleMatrix[x][0], CourseScheduleMatrix[x][1], CourseScheduleMatrix[x][2], CourseScheduleMatrix[x][5], CourseScheduleMatrix[x][6], ExamScheduleMatrix[y][2], ExamScheduleMatrix[y][3], ExamScheduleMatrix[y][4]])
                break  # perfect match found, break out of loop

            # perfect match hasn't been found yet, find the closest exam time
            elif (closest_time is None or closest_time > (CourseScheduleMatrix[x][3] - ExamScheduleMatrix[y][1])) and CourseScheduleMatrix[x][4] == ExamScheduleMatrix[y][0]:
                # Determine closest time block for the course and record its index from the Exam schedule matrix
                # Closest time will be the smallest difference between the course time from CourseScheduleMatrix and the course time from ExamScheduleMatrix

                closest_time = CourseScheduleMatrix[x][3] - ExamScheduleMatrix[y][1]
                closest_y = y  # row of exam schedule matrix with the closest time

            # if a match hasn't been found, append row of course information and exam time of closest normal course time
            if (y == len(ExamScheduleMatrix) - 1) and closest_time is not None:
                output.append([CourseScheduleMatrix[x][0], CourseScheduleMatrix[x][1], CourseScheduleMatrix[x][2], CourseScheduleMatrix[x][5], CourseScheduleMatrix[x][6], ExamScheduleMatrix[closest_y][2], ExamScheduleMatrix[closest_y][3], ExamScheduleMatrix[closest_y][4]])


# The output_writing method will output the data to the excel file selected by the user
def output_writing(file_name):
    # This line brings in the global matrix output
    global output
    # This line defines the headers for the output
    dataColumns = ['Course Number', 'Course Title', 'Section Number', 'Building Code', 'Room Number', 'Exam Date',
                   'Exam Start Time', 'Exam End Time']
    # This line creates a pandas dataframe with the data and header
    df = pd.DataFrame(data=output, columns=dataColumns)
    # This line calls the treatSelectedAddress method to clean up the output file location
    treatedName = treatSelectedAddress(file_name)

    l = len(treatedName)
    if re.match(r'.xlsx', treatedName[l - 5: l]):
        # This line creates a writer to write to the excel file
        writer = pd.ExcelWriter(treatedName, engine='xlsxwriter')
        # This line puts the information from the dataframe to the excel file
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        # This line saves the excel file and closes the writer
        writer.save()
    else :
        df.to_csv(treatedName, index=False, header=dataColumns)


def GUI():
    #################################################################
    ## SOME VARIABLES
    ## We are defining some stuff that will be used later
    ##

    smcm_blue = '#1d285a'
    logo_path = "images\\college-logo.gif"
    # print_icon_path = 'images\\print-icon.gif'
    help_icon_path = 'images\\help-icon.gif'
    about_icon_path = 'images\\info-icon.gif'
    global seahawk_icon_path, README_path, info_popup, help_popup
    seahawk_icon_path = 'images\\seahawk-icon.ico'
    README_path = 'README'
    info_popup = None  # This is necessary for checking if the window is open
    help_popup = None

    #################################################################
    ## WINDOW STUFF
    ## We are defining and packing up some widgets.
    ##

    # Window formatting
    root = tk.Tk()  # The window object
    # root.geometry("300x395") # Leaving this out makes the window resize itself
    root.title("Exam Scheduler")
    root['padx'] = 20
    root['pady'] = 20
    root.configure(bg='grey95')
    root.iconbitmap(seahawk_icon_path)

    # Logo formatting
    logo = tk.PhotoImage(
        file=logo_path)
    logo = logo.subsample(2, 2)
    logo_widget = tk.Label(root, image=logo, bg='grey95')

    # Various icon formatting
    # print_icon = tk.PhotoImage(file=print_icon_path)
    # print_icon = print_icon.subsample(100, 100)

    about_icon = tk.PhotoImage(file=about_icon_path)
    about_icon = about_icon.subsample(18, 18)

    help_icon = tk.PhotoImage(file=help_icon_path)
    help_icon = help_icon.subsample(35, 35)

    # Separator that goes under the title
    sep = ttk.Separator(root, orient='horizontal')
    sep2 = ttk.Separator(root, orient='horizontal')

    # Define title
    title_text = "Exam Scheduler"
    title = tk.Message(root, text=title_text, width=400, anchor='center')
    title.config(font=('calibri', 14), foreground=smcm_blue, bg='grey95')

    # Define the labels for upload buttons
    text_1_str = "Upload Semester Course List:"
    text_1 = tk.Message(root, text=text_1_str, width=1000, bg='grey95', fg=smcm_blue, font=('calibri', 10))

    text_2_str = "Upload Exam Schedule:"
    text_2 = tk.Message(root, text=text_2_str, width=1000, bg='grey95', fg=smcm_blue, font=('calibri', 10))

    # Labels next to upload buttons
    # These indicate what file you uploaded
    global uploaded_file_name_1_str
    uploaded_file_name_1_str = tk.StringVar()
    uploaded_file_name_1_str.set('')
    uploaded_file_name_1 = tk.Message(root, textvariable=uploaded_file_name_1_str, width=800, bg='grey95',
                                      font=('calibri', 10))

    global uploaded_file_name_2_str
    uploaded_file_name_2_str = tk.StringVar()
    uploaded_file_name_2_str.set('')
    uploaded_file_name_2 = tk.Message(root, textvariable=uploaded_file_name_2_str, width=800, bg='grey95',
                                      font=('calibri', 10))

    # Upload buttons

    upload_cschedule_button = tk.Button(root, text='Browse...',
                                        command=upload_callback, bg=smcm_blue, fg='white', font=('calibri', 10, 'bold'))  # This stuff makes her pretty

    upload_fschedule_button = tk.Button(root, text='Browse...', command=upload_callback2, bg=smcm_blue, fg='white', font=('calibri', 10, 'bold'))  # This stuff makes her pretty

    # Output buttons
    global save_output_button, display_output_button
    save_output_button = tk.Button(root, text='Save Output...', command=save_output, state='disabled', font=('calibri', 10, 'bold'))

    display_output_button = tk.Button(root, text='Display/Print Output...', command=display_output, state='disabled', font=('calibri', 10, 'bold'))

    info_buttons_frame = tk.Frame(root)  # purely for the aesthetic

    about_button = tk.Button(info_buttons_frame, image=about_icon, width=15, height=15,
                             command=lambda: open_popup('info'))

    help_button = tk.Button(info_buttons_frame, image=help_icon, width=15, height=15,
                            command=lambda: open_popup('help'))

    ################################
    # Put all the widgets into the window with a whole bunch of formatting
    #

    logo_widget.grid(row=0, column=0, columnspan=2)
    title.grid(row=1, column=0, columnspan=2)
    sep.grid(row=2, column=0, columnspan=2, sticky='ew')
    text_1.grid(row=3, column=0, columnspan=2, padx=0, pady=(20, 5), sticky="W")
    upload_cschedule_button.grid(row=4, column=0, columnspan=2, padx=20)
    uploaded_file_name_1.grid(row=4, column=1, columnspan=2, sticky='E')
    text_2.grid(row=5, column=0, columnspan=2, padx=0, pady=(10, 5), sticky='W')
    upload_fschedule_button.grid(row=6, column=0, columnspan=2, padx=20)
    uploaded_file_name_2.grid(row=6, column=1, columnspan=2, sticky='E')
    sep2.grid(row=7, column=0, columnspan=2, pady=(20, 0), sticky='ew')
    save_output_button.grid(row=8, column=0, padx=12, pady=(20, 0), sticky='E')
    display_output_button.grid(row=8, column=1, pady=(20, 0), sticky='W')
    # print_button.grid(row=8, column=0, columnspan=2, pady=(10, 0))  # rip :(
    info_buttons_frame.grid(row=10, column=1, pady=(30, 0), sticky="E")

    # These automatically pack into info_buttons_frame frame.
    about_button.pack(side="left")
    help_button.pack(side="right")

    # this is the stuff for moving buttons around when the window is resized
    root.columnconfigure(0, weight=2, minsize=125)
    root.columnconfigure(1, weight=2, minsize=125)
    root.rowconfigure(2, weight=2, minsize=1)
    root.rowconfigure(7, weight=2, minsize=21)


    # Make the window persistent
    root.mainloop()


GUI()
