#imple
import sqlite3
import getpass

connection = sqlite3.connect('/home/carson/291/project1/project1.db')
cursor = connection.cursor()


def connect(path):
    global cnnectin, cursor

    connection = sqlite3.connect(path)
    c = connection.cursor()
    c.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def user_login():
    decision = input("Are you a new member?(yes/no)")
    decision = decision.lower()

    if decision == 'n':
        input_email = raw_input('Please enter your email. ')
        input_email = input_email.lower()
        input_password = getpass.getpass(prompt = 'Please enter your password. ')

        #prevent injections using regular expression
        #but when using re.match even partical matching will pass
        cursor.execute("select pwd from members where email=:input_email",
                       {"input_email":input_email})
        user_password = cursor.fetchall()
        connection.commit()
        if user_password == input_password:
            print('Successfully login')

            #and need to display all inbox unseen
            cursor.execute("select content from inbox where email=:input_email and seen = 'n' ",
                           {"input_email":input_email})
            message = cursor.fetchall()
            print(message)
            #update all unseen to seen
            cursor.execute("update inbox set seen = 'y' ")
            connection.commit()

        #if password is wrong
        else:
            print("Wrong password, please try again!")
    
    #for new user case
    else:
        #check for unique
        #create a set to store all eamil add for later checking uniquess
        email_set = set()
        cursor.execute("select email from members;")
        all_email = cursor.fetchall()
        for i in range(len(all_email)):
            email_set.add(all_email[i])
        
        signup_email = raw_input('Enter a email address ')
        signup_email = signup_email.lower()
        
        #need to try until get the unique pwd
        while True:
            if signup_email in email_set:
                print('This email already exist, try another one. ')
        
            else:
                signup_name = raw_input('Please enter your name. ')
                sighup_phone = raw_input('Please enter your phone. ')
                sighup_pass = raw_input('Enter your password. ')
                cursor.execute("insert into members values(email=:e,name=:n,phone=:ph,pwd=pd",
                              {"e":signup_email,"n":signup_name,"p":sighup_phone, "pd":sighup_pass})
            
                connection.commit()
                print("New Account have been created!")
                break
    
    return input_email





def choose_operation():
    pass



def logout():
    pass



def main():
    pass







