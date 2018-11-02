'''
# some error :sqlite3.OperationalError: no such column
# the reaseon you getting this is error is you match the value fetch from sqlite output, which has a 
# type list, while when doing query the macthing type should be str, or int but not list
#
'''
import sqlite3
import random

connection = sqlite3.connect('/home/carson/291/project1/project1.db')
cursor = connection.cursor()

#####################
# variable user_email is the email that user enter in the login screen 
# and pass thourgh all 5 main functionality
#

def connect(path):
    global conection, cursor

    path = "/home/carson/291/project1/project1.db"
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


#list all booking that the member(as the login email user) offer
def list_bookings(user_email):
    global connection, cursor
    
    print("The following is all the bookings match your email.")
    cursor.execute("select * from bookings b where b.email =:email",
                    {'email':user_email})
    connection.commit()
    rows = cursor.fetchall()
    for i in range(len(rows)):
        print (rows[i])
    
    
    
#cancel a booking
#cancel a booking is delete the record from the table
def cancel(user_email):
    
    global conection, cursor
    cancel_num = input('Please enter the booking number you want to cancle:')
    cancel_num = int(cancel_num)
    #first get the rno of current ride base on the bno you provide
    #and then delete it from table
    #and need to query the rno from booking table
    cursor.execute("select rno from bookings where bno=:bno",
                    {"bno":cancel_num})
    
    inbox_rno = cursor.fetchone()
    inbox_rno = inbox_rno[0]
    
    connection.commit()
    
    #delete the booking record
    cursor.execute('delete from bookings where bno =:bno', {"bno":cancel_num})
    connection.commit()
    print("The booking is deleted!")
    
    #sent the message to the member that .. just mean insert a new row into the inbox table
    #get time
    cursor.execute("select date('now');")
    
    timestamp = cursor.fetchone()
    timestamp = str(timestamp)
    timestamp = timestamp[3:13]
    connection.commit()
    print(timestamp)
    
    content = 'System successfully delete the record!'
    sender = user_email
    seen = 'n'
    #print(inbox_rno)
    
    #when delete system will send a message to the user
    #cursor.execute("insert into inbox values (email=:email, msgTimestamp=:timestamp, 'system', content=:content, rno=:rno, 'n')",
         #           {"email":user_email,"timestamp":timestamp,"content":content,"rno":inbox_rno})
    cursor.execute("insert into inbox values (?,?,?,?,?,?)",(user_email,timestamp,sender,content,inbox_rno,seen))
    
    #what the hell is the rno in the message??
    # you can get this rno from bookings table
    connection.commit()

#Also the member should be able to book other members on the rides they offer
#list all rides the member offers with the number of available seats for each ride
def list_ride():
    global conection, cursor

    print('List all rides the member offers with he number of available seats')
    print('Want to see more than 5 matching rides?(y/n)')
    cond = input()
    cond = cond.lower()
    if cond == 'n':
        cursor.execute('''select driver,r.rno, (r.seats-b.seats) as available
                       from rides r
                       left outer join bookings b on r.rno = b.rno
                       limit 5;
                       ''')
        rows = cursor.fetchall()
        print(rows)
        connection.commit()

    else:
        cursor.execute('''select driver, r.rno, (r.seats-b.seats) as available
                       from rides r
                       left outer join bookings b on r.rno = b.rno
                       ;
                       ''')
        rows = cursor.fetchall()
        for i in range(len(rows)):
            print(rows[i])
        
        connection.commit()

'''
The member should be able to select a ride and book a member for that ride
'''
def book_member(user_email):
    global conection, cursor

    rno_select = input('Please enter the rno you want to select.')
    member_email = input('Please enter the member email you want to book.')
    member_email = member_email.lower()
    num_seat = int(input('Please enter the number of seats booked.'))
    cost_per_seat = int(input('Please enter cost per seat.')) 
    print('Please enter pickup and drop off location code.')
    pickup,dropoff = input().split()
    pickup = pickup.lower()
    dropoff = dropoff.lower()
    
    #assign a unique book number
    #first create a set with all bno in it
    bno_set = set()
    cursor.execute("select bno from bookings;")
    rows = cursor.fetchall()
    for i in range(len(rows)):
        bno_set.add(rows[i])
    #unique bno
    while True:
        temp_bno = random.randint(1,5000)
        if temp_bno not in bno_set:
            break
    new_bno = temp_bno

    
    #give warning if overbook the seat
    cursor.execute('select seats from rides where rno=:rno',{"rno":rno_select})
    row = cursor.fetchone()
    if num_seat > row[0]:
        print('Warning: the seats are overbooked. Do you want to comfirm?(y/n)')
        key = input()
        key = key.lower()
        
        if key == 'y':
            #comfirm this booking 
            cursor.execute("insert into bookings values(bno=:bno, email=:email,rno=:rno,cost=:cost,seats=:seats,pickup=:pickup,dropoff=:dropoff)",
                            {"bno":new_bno,"email":member_email, "rno":rno_select,"cost":cost_per_seat,"seats":num_seat,"pickup":pickup,"dropoff":dropoff})
        else:
            print('Overbooked, booking not complete.')

    
    #After a successful booking, a proper message should be sent to the other member that s/he is booked on the ride.
    #first find the emil of member base on rno user input
    #fetchone return a list, list[0] to get the date
    cursor.execute("select datetime('now');")
    time = cursor.fetchone()
    time = time[0]
    #cursor.execute("insert into inbox values(email=:eamil,msgTimestamp=:time,sender=:sender,'you are booked', rno=:rno,'n')",
                    #{"email":member_email, "time":time,"sender":user_email,"rno":rno_select})
    cursor.execute("insert into inbox values (?,?,?,?,?,?)",(member_email,time,user_email,'you are booked',rno_select,'n'))
    connection.commit()
    print("Insert a new message into inbox.")




def main():
    global connection,cursor
    path = "/home/carson/291/project1/project1.db"
    #path = raw_input("Please enter the path of your databese file")
    connect(path)

    '''#****************
    list_bookings function need a parameter emial that is passing from login, so email is user email
    '''
    user_email = 'davood@abc.com'
    list_bookings(user_email)
    cancel(user_email)
    list_ride()
    book_member(user_email)
   
    
    return


if __name__ == "__main__":
    main()

