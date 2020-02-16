import sqlite3
import sys

class library:

    def __init__(self):
        self.name = ""
        self.surname = ""
        self.rollno = ""
        self.userlib = ""
        self.pinlib = ""
        self.admin_user=""
        self.admin_pass=""
        self.conn = sqlite3.connect('Librarydata.db')
        self.c = self.conn.cursor()

    def create_table1(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS Login(Name TEXT, Surname TEXT, RollNo TEXT, Username TEXT, Password TEXT)')

    def dynamic_data_entry1(self,name,surname,roll,user1,pass1):
        name1 = name
        sur1 = surname
        roll1 = roll
        user_name = user1
        pass_lib = pass1
        self.c.execute("INSERT INTO Login(Name, Surname, RollNo, Username, Password) VALUES (?, ?, ?, ?, ?)",(name1, sur1, roll1, user_name, pass_lib))
        self.conn.commit()

    def create_table2(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS Books(Name TEXT, Author TEXT, Code TEXT)')
    
    def admin(self,admin_user,admin_pass):
        self.c.execute("SELECT * FROM Admin ")
        data = self.c.fetchall()
                
        if data[0][2]==admin_user and data[0][3]==admin_pass:
            print("Login Successful")
            self.book_entry()
        else:
            print("Username or Password Incorrect")
    
    def book_entry(self):
        print("1. Enter new books in stock ")
        #print("2. Remove Book")
        print("2. Logout ")
        ch = int(input("Enter your option : "))
        self.create_table2()
        if ch==1:
            n = int(input("How many books would you like to enter : "))
            for i in range(n):
                name = input("Enter Book name : ")
                author = input("Enter Author name : ")
                code = input("Enter Book Code : ")
                self.c.execute("INSERT INTO Books(Name, Author, Code) VALUES (?, ?, ?)",(name, author, code))
                self.conn.commit()
        elif ch==2:
            print("Logged out Successfully")
        else:
            print("Invalid Input")


    def close_conn(self):
        self.c.close()
        self.conn.close()

    def login(self,userlib,pinlib):
        self.c.execute("SELECT * FROM Login ")
        data = self.c.fetchall()
        flag = 0
        for i in range(len(data)):
            if data[i][3] == userlib and data[i][4] == pinlib:
                flag = 1
                loc = i
                break
            else:
                flag = 0
        if flag==1:
            print("")
            print("Login Successful")
            print("")
            print("Welcome " + data[loc][0] +" "+ data[loc][1])
            self.login_info(data[loc])
        elif flag==0:
            print("\n"+"Username or Password Incorrect")

    def search_book(self,roll,bname):
        rollno1 = roll
        self.c.execute("SELECT * FROM Books ")
        data = self.c.fetchall()
        flag = 0
        for i in range(len(data)):
            if data[i][0]==bname:
                loc = i
                flag = 1
                break
            else:
                flag=0
        if flag==1:
            print("")
            print("----------------------------------------------")
            print("Book Found")
            print("----------------------------------------------")
            print("Book Name : "+data[loc][0])
            print("Book Author : "+data[loc][1])
            print("Book Code : "+data[loc][2])
            print("----------------------------------------------")
            ch = input("Do you want to issue [y/n] : ")
            if ch=='y':
                date = int(input("Enter Todays date : "))
                print("")
                print("Book Issued Successfully ")
                print("----------------------------------------------")
                self.create_table3()
                self.issued_entry(rollno1,data[loc][0],date)
            elif ch=='n':
                print("\n"+"Returned to the main")
        else:
            print("Book Not Found")

    def return_book(self,roll):
        roll1 = roll
        L=[]
        
        self.c.execute("SELECT * FROM Issued ")
        data = self.c.fetchall()

        if data[0][0]==roll1:
            print("Book Name : "+data[0][1])
            ch = input("Confirm Return [y/n] : ")
            if ch == 'y':
                print("")
                print("Book Returned Successfully")
            elif ch=='n':
                print("Returned to main menu")
        else:
            print("No return left")
        '''
        for j in range(len(data)):
            if data[j][0]==roll1:
                print("Matched")'''
        
 
    def login_info(self,t):
        print("")
        print("1. Profile Info") 
        print("2. Issue Book(s)") 
        print("3. Return Book(s)")
        print("4. Log out")
        ch = int(input("Enter your option : "))

        if(ch==1):
            print("")
            print("------------------------------------------------------------")
            print("Profile Info ")
            print("------------------------------------------------------------")
            print("Name : "+t[0])
            print("Surname : "+t[1])
            print("RollNo : "+t[2])
            print("Username : "+t[3])
            #print("Books Issued : ")
            print("------------------------------------------------------------")
        
        elif ch==2:
            print("------------------------------------------------------------")
            print("Issue Book")
            print("------------------------------------------------------------")
            self.bookname = input("Enter book name : ")
            self.search_book(t[2],self.bookname)
        
        elif ch==3:
            print("------------------------------------------------------------")
            print("Return Book")
            print("------------------------------------------------------------")
            self.return_book(t[2])

        

        elif ch==4:
            print("\n"+"Logged Out Successfully")
        else:
            print("\n"+"Invalid Input")
    
    def create_table3(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS Issued(RollNo TEXT, Name TEXT, Date_Issued TEXT)')

    def issued_entry(self,roll,bname,date):
        self.c.execute("INSERT INTO Issued(RollNo, Name, Date_Issued) VALUES (?, ?, ?)",(roll,bname,date))
        self.conn.commit()
    
    def get_data(self):
        print("")
        print("-------------------------------------------------------------")
        print("ONLINE LIBRARY")
        print("-------------------------------------------------------------")
        print('''Select your Option
            1:Librarian Login
            2:Student Login
            3:Create Account
            4:Exit''')
        print("-------------------------------------------------------------")    
        opt1=int(input("Please Enter your option:"))

        if opt1==1:
            print("")
            print("------------------------------------------------------------")
            self.admin_user = input("Enter your username : ")
            self.admin_pass = int(input("Enter your Pin : "))
            self.admin(self.admin_user,self.admin_pass)

        elif opt1==2:
            print("")
            print("------------------------------------------------------------")
            self.userlib = input("Enter your username : ")
            self.pinlib = input("Enter your pin : ")
            self.login(self.userlib,self.pinlib)
        
        elif opt1==3:
            print("")
            print("------------------------------------------------------------")
            self.name = input("Enter your name : ")
            self.surname = input("Enter your surname : ")
            self.rollno = input("Enter your roll no : ")
            self.userlib = input("Enter a username : ")
            self.pinlib = input("Enter a pin : ")
            self.create_table1()
            self.dynamic_data_entry1(self.name,self.surname,self.rollno,self.userlib,self.pinlib)
            print("")
            print("Account Created Successfully")
        elif opt1==4:
            print("\n"+"Exit Successfull")
            sys.exit(0)
            


lib=library()
while(True):
    print("")
    ch = int(input("Press 1 to continue and 2 to exit : "))
    if ch == 2:
        break
    elif ch  == 1:
        lib.get_data()
    else:
        print("")
        print("Invalid Input")
lib.close_conn()
