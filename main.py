# Import mysql and connect to Database and set up the cursor to execute queries
import os
import bcrypt
import mysql.connector
from dotenv import load_dotenv

# connect to the database
load_dotenv()

connect = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# set up the cursor
cr = connect.cursor()



# Create Tables in Database 
create_table1 = '''
CREATE TABLE IF NOT EXISTS users_data (
username TEXT,
email TEXT,
password TEXT
);
'''
cr.execute(create_table1)


create_table2 = '''
CREATE TABLE IF NOT EXISTS deleted_data (
username TEXT,
email TEXT,
password TEXT
);
'''
cr.execute(create_table2)


# Define Variables to control loops
check_2 = True 
check_1 = True
first_try = True




def insert(username, email, password):

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    query_insert = '''
    INSERT INTO users_data (username, email, password) 
    VALUES (%s, %s, %s)
    '''
    cr.execute(query_insert, (username, email, hashed_password.decode('utf-8')))
    connect.commit()


def update_pass(new_pass, username):

    hashed = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt())
    query_update = '''
    UPDATE users_data
    SET password = %s
    WHERE username = %s
    '''
    cr.execute(query_update, (hashed.decode('utf-8'), username))
    connect.commit()
    print("\nYour password was changed successfully.\n")


def get_data():

    global full_data
    username = input("Type your Username:\n")
    email = input("Type your Email:\n")
    password = input("Type your Password:\n")
    print("")
    full_data = [username, email, password]
    return full_data


def get_and_check():

    get_data()
    query_select2 = '''
    SELECT *
    FROM users_data
    WHERE username = %s AND email = %s AND password = %s
    '''
    cr.execute(query_select2, (full_data[0], full_data[1], full_data[2]))
    old_data = cr.fetchone()
    return old_data == tuple(full_data)


def delete_and_backup():

    query_insert = '''
    INSERT INTO 
    deleted_data (username, email, password)
    VALUES (%s, %s, %s)
    '''
    cr.execute(query_insert, (full_data[0], full_data[1], full_data[2]))

    query_delete = '''
    DELETE FROM users_data
    WHERE username = %s AND email = %s AND password = %s
    '''
    cr.execute(query_delete, (full_data[0], full_data[1], full_data[2]))

    connect.commit()
    print("Your account was deleted successfully.\n")

    global check_1
    global check_2
    
    while True:

        will_delete = input("Wanna delete another account?\n").strip().capitalize()
        print("")

        if will_delete == "Yes":
            result = get_and_check()
            if result is True:               
                delete_and_backup()
            else:
                print("Incorrect data.\n")

        elif will_delete == "No":
            check_1 = False
            check_2 = True
            break 
            
        else:
            print("Please, enter just 'Yes' or 'No'.\n")
            continue


def show_menu():

    menu = {
    "Login with your account" : 1,
    "Signup with a new account" : 2,
    "Change my password" : 3,
    "Delete my account" : 4,
    "Restore deleted accounts" : 5,
    "Close the connection" : 6
    }

    for num, choice in zip (menu.values(), menu.keys()):
        print(f"{num}. {choice}")












print("Welcome to our system")



while True:  ####################################


    if check_1 is True:

            is_new = input("Is it your first time here?\n").strip().capitalize()
            print("")

    
    
    if is_new == "Yes":
        
            print("Then, you must create a new account")
            input("Ready to create your account\n")
            get_data()
            insert(full_data[0], full_data[1], full_data[2])
            print("Your account was created successfully.")
            input("Ready for the next stage?\n")
            is_new = "No"
            check_1 = False
            continue
        


    elif is_new == "No":
                       



            if check_2 is True :

                show_menu()
                print("")
                action = input("Choose an action to perform:\n")
                print("")



            if action == "1":    # Login with your account
                
                to_break = True

                while to_break == True:   ################################

                    get_data()
                    query_select = '''
                    SELECT * FROM users_data 
                    WHERE username = %s AND email = %s AND password = %s
                    '''
                    cr.execute(query_select, (full_data[0], full_data[1], full_data[2]))
                    check = cr.fetchone()

                    
                    if check is None :
                            
                            print("Incorrect data\n")

                            while True:   ####################################
                                    
                                    print("1. Try again")
                                    print("2. Create a new account")
                                    print("3. Return to the main menu")
                                    action2 =  input()
                                    print("")

                                    if action2 == "1":    # Try again
                                        break

                                    elif action2 == "2":    # Create a new account
                                        check_1 = False
                                        check_2 = False 
                                        first_try = True
                                        action = "2"                            
                                        to_break = False
                                        break                              

                                    elif action2 == "3":    # Return to the main menu
                                        check_1 = False
                                        check_2 = True
                                        first_try = True                                                                  
                                        to_break = False
                                        break

                                    else:
                                        print("Please, enter a valid value")
                                        continue

                    else:
                            print("You are already on our system\n")
                            print("Here is your stored data:")
                            print(f"Your username is \"{check[0]}\"")
                            print(f"Your email is \"{check[1]}\"")
                            print(f"Your password is \"{check[2]}\"\n")
                            check_1 = False
                            check_2 = True
                            break








            elif action == "2":   # Signup with a new account


                    if first_try is True:
                            print("Let's create your account\n")
                            user_name = input("Type your Username:\n")
                    else:
                            user_name = input("Now, try a different Username:\n")
                    
                    print("")

                    query_check_username = '''
                    SELECT username
                    FROM users_data
                    '''
                    cr.execute(query_check_username)
                    all_usernames = cr.fetchall()

                    if (user_name,) not in all_usernames:
                        
                        email = input("Type your Email:\n")
                        print("")
                        password = input("Type your Password:\n")
                        print("")
                        full_data = [user_name, email, password]
                        insert(full_data[0], full_data[1], full_data[2])
                        print("Your account was created successfully.\n")
                        check_1 = False
                        check_2 = True
                        continue
                    
                    else:

                        print(f"Username \"{user_name}\" already exists\n")
                        
                        while True:
                                
                                print("1. Try again")
                                print("2. Return to the main menu")
                                action6 = input()
                                print("")
    
                                if action6 == "1":
                                    check_1 = False
                                    check_2 = False
                                    action = "2"
                                    first_try = False
                                    break

                                elif action6 == "2":
                                    check_1 = False
                                    check_2 = True
                                    first_try = True
                                    break

                                else:
                                    print("Please, enter a valid value")
                                    continue
                                        






            elif action == "3":    # Change my password
                
                    result = get_and_check()

                    if result is True :

                            new_pass = input("Enter the new password:\n")
                            username = full_data[0]
                            update_pass(new_pass, username)
                            check_1 = False
                            check_2 = True
                            continue
                            

                    else:             
                            while True:   ###########################

                                    print("Incorrect data.\n")

                                    print("1. Try again")
                                    print("2. Create a new account")
                                    print("3. Return to the main menu")
                                    action3 = input()
                                    print("")

                                    if action3 == "1":
                                        check_1 = False
                                        check_2 = False
                                        action = "3"
                                        break
                                    elif action3 == "2":
                                        check_1 = False
                                        check_2 = False   
                                        first_try = True                                   
                                        action = "2"
                                        break
                                    elif action3 == "3":
                                        check_1 = False
                                        check_2 = True
                                        first_try = True
                                        break
                                    else:
                                        print("Please, enter a valid value")
                                        continue
                        






            elif action == "4":     # Delete my account
                    
                    result = get_and_check()

                    if result is True:               
                            delete_and_backup()
                            continue
                    
                    else:
                            print("Incorrect data.\n")
                            
                            while True:   ###########################

                                    print("1. Try again")
                                    print("2. Return to the main menu")
                                    action4 = input()
                                    print("")

                                    if action4 == "1":
                                        check_1 = False
                                        check_2 = False                    
                                        action = "4"
                                        break
                                    elif action4 == "2":
                                        check_1 = False
                                        check_2 = True
                                        first_try = True
                                        break
                                    else:
                                        print("Please, enter a valid value")
                                        continue


                          




            elif action == "5":     # Restore deleted accounts
                                
                    print("To restore your deleted account, please enter your old credentials:\n")

                    while True:
                            
                            get_data()

                            query_check_deleted = '''
                            SELECT * FROM deleted_data
                            WHERE username = %s AND email = %s AND password = %s
                            '''
                            cr.execute(query_check_deleted, (full_data[0], full_data[1], full_data[2]))
                            deleted_account = cr.fetchone()

                            if deleted_account:
                                    
                                    query_restore = '''
                                    INSERT INTO 
                                    users_data (username, email, password)
                                    VALUES (%s, %s, %s)
                                    '''
                                    cr.execute(query_restore, (full_data[0], full_data[1], full_data[2]))

                                    query_delete_from_deleted = '''
                                    DELETE FROM deleted_data
                                    WHERE username = %s AND email = %s AND password = %s
                                    '''
                                    cr.execute(query_delete_from_deleted, (full_data[0], full_data[1], full_data[2]))

                                    connect.commit()
                                    print("\nYour account has been successfully restored!\n")
                                    break
                            
                            else:

                                print("\nNo matching deleted account found.\n")

                                while True:   ###########################

                                    print("1. Try again")
                                    print("2. Return to the main menu")
                                    action5 = input()
                                    print("")

                                    if action5 == "1":
                                        check_1 = False
                                        check_2 = False                             
                                        action = "5"
                                        break
                                    elif action5 == "2":                  
                                        check_1 = False
                                        check_2 = True
                                        first_try = True
                                        break
                                    else:
                                        print("Please, enter a valid value")
                                        continue






            else:           # Close the connection
                 
                connect.close()
                break


    else:
        print("Please, enter just 'Yes' or 'No'.\n")
        check_1 = True
        continue
