import mysql.connector
import os
from dotenv import load_dotenv
from jdatetime import datetime as dt
from jdatetime import timedelta
import random
list_error=[]
# -----------------------------------------------------------------------------------------------------------------
try:
    load_dotenv()
    database = mysql.connector.connect(
        host=os.getenv("db_host"),
        user=os.getenv("db_user"),
        password=os.getenv("db_password"),
        port=os.getenv("db_port")
    )
    cursor = database.cursor()
except Exception as e:
    list_error.append(str(e))
else:
    print("You are connected to the database")


try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS parking")
except Exception as error:
    print("Not Created DATABASE...")
    list_error.append(str(e))
else:
    print("DATABASE Created...")
# --------------------------------------------------------------------------------------------------------

try:
    cursor.execute("USE parking")
    available_car = ("""
        CREATE TABLE IF NOT EXISTS available_car (
            ID BIGINT PRIMARY KEY AUTO_INCREMENT,
            pelak VARCHAR(6) NOT NULL,
            telephone VARCHAR(11) NOT NULL,
            enter_time varchar(20))""")
    cars=("""
        CREATE TABLE IF NOT EXISTS cars  (
            ID BIGINT PRIMARY KEY AUTO_INCREMENT,
            pelak VARCHAR(6) NOT NULL,
            telephone VARCHAR(11) NOT NULL,
            enter_time varchar(20) , 
            exit_time VARCHAR(20),
            time_spend VARCHAR(50),
            factor float)""")
    vip = ("""
        CREATE TABLE IF NOT EXISTS vip (
            ID BIGINT PRIMARY KEY AUTO_INCREMENT,
            vip_code BIGINT NOT NULL,
            telephone VARCHAR(11) NOT NULL, 
            pelak VARCHAR(6) NOT NULL,
            join_time VARCHAR(20),
            expire_time VARCHAR(20))""")
    admin=("""
        CREATE TABLE IF NOT EXISTS admin (
            ID BIGINT PRIMARY KEY AUTO_INCREMENT,
            username  varchar(10) NOT NULL,
            password  VARCHAR(10) NOT NULL)""")
    cursor.execute(admin)
    cursor.execute(cars)
    cursor.execute(available_car)
    cursor.execute(vip)
except Exception as e:
    print("Not Created Tables...")
    list_error.append(str(e))
else:
    database.commit()
    print("Tables Created...")
# ---------------------------------------------------------------------------------------------------------------------------
def get_information(q):
    try:
        if q == "3":
            while True:
                pelak = input("Pelak : ")
                if len(pelak) == 6 and pelak[2].isalpha() and pelak[:2].isnumeric() and pelak[3:].isnumeric():
                    break
                else:
                    print("Pelak Not Corrected...")
                    q2=str(input("do you want to continue(yes or no)-->>")).lower()
                    if q2 == "yes":
                        continue
                    else:
                        print("The car plate was not registered")
                        return None , None ,None
            while True :
                telephone = str(input("Telephone : "))
                if len(telephone) == 11 and telephone.startswith("09") and telephone.isdigit():
                    break
                else:
                    print("Telephone Not Corrected...")
                    q2=str(input("do you want to continue(yes or no)-->>")).lower()
                    if q2 == "yes":
                        continue
                    else:
                        print("The telephon was not registered")
                        return pelak , None ,None 
            return pelak , telephone , None
        else:
            while True:
                pelak = input("Pelak : ")
                if len(pelak) == 6 and pelak[2].isalpha() and pelak[:2].isnumeric() and pelak[3:].isnumeric():
                    break
                else:
                    print("Pelak Not Corrected...")
                    q2=str(input("do you want to continue(yes or no)-->>")).lower()
                    if q2 == "yes":
                        continue
                    else:
                        print("The car plate was not registered")
                        return None , None ,None
                    
            while True :
                telephone = str(input("Telephone : "))
                if len(telephone) == 11 and telephone.startswith("09") and telephone.isdigit():
                    break
                else:
                    print("Telephone Not Corrected...")
                    q2=str(input("do you want to continue(yes or no)-->>")).lower()
                    if q2 == "yes":
                        continue
                    else:
                        print("The telephon was not registered")
                        return pelak , None ,None
                    
            while True:
                code=str(input("enter your vip key(If you don’t have a VIP code, write 'NO')-->> ")).lower()
                cursor.execute("SELECT vip_code FROM vip")
                results2=cursor.fetchall()
                if results2 == []:
                    print("we do not have vip code")
                    return pelak , telephone ,None
                else:
                    if code == "no":
                        return pelak , telephone , None
                    elif code.isdigit() :
                        codes=[int(row[0]) for row in results2]
                        if int(code) in codes:
                            print("code found")
                            return pelak , telephone , int(code)
                        else:
                            print("code not found")
                            q2=str(input("do you want to continue(yes or no)-->>")).lower()
                            if q2 == "no":
                                return pelak , telephone ,None
                        continue
                    else:
                        print("Invalid code")
                        return pelak , telephone ,None
    except Exception as e:
        list_error.append(str(e))
# ----------------------------------------------------------------------------------------------------
def enter_data(pelak,telephone):
    try:
        enter_time1= dt.now()
        enter_time=enter_time1.strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO available_car(pelak,telephone,enter_time) values(%s ,%s ,%s)"
        values = (pelak,telephone,enter_time)
        cursor.execute(sql,values)
        sql = "INSERT INTO cars(pelak,telephone,enter_time) values(%s ,%s ,%s)"
        values = (pelak,telephone,enter_time)
        cursor.execute(sql,values)
    except Exception as e:
        print("Not Connected...")
        list_error.append(str(e))
    else:
        print(f"{cursor.rowcount} Data Has Been Inserted...")
        database.commit()
# -------------------------------------------------------------------------------------------------------------------------
def exit(pelak,telephone,code):
    try:
        cursor.execute("SELECT enter_time FROM available_car WHERE pelak=%s AND telephone=%s", (pelak, telephone))
        result = cursor.fetchone()
        if not result:
            print("pelak not found")
            return None
        exit_time=dt.now()
        enter_time = dt.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        time_spend=(((exit_time-enter_time).total_seconds())/60)/60
        factor1=5000+(time_spend)*10000
        if not code:
            factor=factor1
        else:
            factor=factor1*0.8
            print("***VIP***")
        sql = """UPDATE cars 
                SET exit_time=%s, time_spend=%s, factor=%s 
                WHERE pelak=%s AND telephone=%s"""
        values = (exit_time.strftime("%Y-%m-%d %H:%M:%S"), str(time_spend), factor, pelak, telephone)
        cursor.execute(sql, values)
        sql = "DELETE FROM available_car WHERE telephone = %s and pelak=%s"
        cursor.execute(sql, (telephone,pelak))
        database.commit()
        return factor , str(time_spend)
    except Exception as e:
        list_error.append(str(e))
# ------------------------------------------------------------------------------------------------
def enter_vip(pelak,telephone):
    try:
        enter_time1= dt.now()
        enter_time=enter_time1.strftime("%Y-%m-%d %H:%M:%S")
        expire_time = (enter_time1 + timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S") 
        while True:
            code=random.randint(100000,999999)
            cursor.execute("SELECT vip_code FROM vip")
            results2 = cursor.fetchall()        
            codes = [row[0] for row in results2]
            if code  not in codes:
                break
        sql = "INSERT INTO vip(pelak,join_time ,expire_time ,telephone,vip_code) values(%s,%s,%s,%s ,%s)"
        values =(pelak,enter_time,expire_time,telephone,code)
        cursor.execute(sql,values)
        database.commit()
        return code
    except Exception as e:
        list_error.append(str(e))
# ---------------------------------------------------------------------------------------------
def start_admin():
    try:
        cursor.execute("SELECT COUNT(*) FROM admin")
        result = cursor.fetchone()
        if result[0] == 0:
            username=str(input("please enter your username(for admin) : "))
            password=str(input("please enter your password(for admin) : "))
            cursor.execute("INSERT INTO admin(username, password) VALUES(%s, %s)", (username, password))
            database.commit()
            print("admin added.")
        else:
            print("Admin already exists.")
    except Exception as e:
        list_error.append(str(e))
# ------------------------------------------------------------------------------------------
def show_table_for_admin(column_name,table_name,number_row,start_row):
    try:
        print("name tables: 'cars' , 'vip' , 'available_car'  ")
        print("name column for cars: ID , pelak , telephone , enter_time , exit_time , time_spend ,factor ")
        print("name column for available_car : ID , pelak , telephone , enter_time")
        print("name column for vip :ID , telephone , pelak , join_time , expire_time")
        cursor.execute(f"""SELECT {column_name} FROM {table_name}
                            limit {number_row}
                            offset {start_row-1}""" )
        result=cursor.fetchall()
        for i in result:
            print(*i)
    except Exception as e:
        list_error.append(str(e)) 
# -------------------------------------------------------------------------------------------
def enter_admin():
    try:
        while True:
            username=str(input("please enter your username : "))
            password=str(input("please enter your password : "))
            cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
            admin =cursor.fetchone()
            if admin:
                break
            else:
                print("admin not found")
                q2=str(input("do you want to continue(yes or no)-->>")).lower()
                if q2 == "yes":
                    continue
                else:
                    print("Returning to main menu")
                    return None
        while True:
            Q=str(input("\n***admin menu***\n1-see error\n2-sleep Script\n3-shut down script\n4-new admin\n5-remove admin\n6-admin list\n7-show tables\n8-removed cars history\n9-exit\n(please enter a numner)-->> "))
            if Q == "1":
                if list_error == []:
                    print("we do not have error")
                else:
                    for i in list_error:
                        print(i)
            elif Q == "2":
                while True:
                    print("\nsleep model\nfor exit enter password and username\n")
                    username=str(input("please enter your username : "))
                    password=str(input("please enter your password : "))
                    cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
                    admin =cursor.fetchone()
                    if admin:
                        break
            elif Q == "3":
                print("Be assured that with this approach,\nthe list of errors will be cleared,\nand if the database tables do not exist at startup,\nthey will be created again automatically\n ")
                q3=str(input("are you sure to shut down(yes/no) : ")).lower()
                if q3 == "yes" :
                    return Q
                else:
                    print("Returning to admin menu\n")
                    continue
            elif Q == "4":
                username=str(input("please enter your username : "))
                password=str(input("please enter your password : "))
                cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
                admin =cursor.fetchone()
                if not admin:
                    cursor.execute("INSERT INTO admin(username, password) VALUES(%s, %s)", (username, password))
                    database.commit()
                    print("admin added")
                else:
                    print("admin already existed")
                    continue
            elif Q == "5":
                    username=str(input("please enter your username : "))
                    password=str(input("please enter your password : "))
                    cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
                    admin =cursor.fetchone()
                    if not admin :
                        print("admin not found")
                        continue
                    else:
                        sql = "DELETE FROM admin WHERE username = %s and password=%s"
                        cursor.execute(sql,(username,password))
                        database.commit()
                        print("admin removed")
                        continue
            elif Q == "6":
                cursor.execute("SELECT * FROM admin")
                admin =cursor.fetchall()
                for i in admin:
                    print(*i,)
                continue
            elif Q =="7":
                table_name=str(input("enter table name : "))
                column_name=str(input("enter columns name : "))
                number_row=int(input("enter number of row : "))
                start_row=int(input("enter start row : "))
                show_table_for_admin(column_name,table_name,number_row,start_row)
                continue
            elif Q == "8":
                sql = "DELETE FROM CARS "
                sql2="ALTER TABLE CARS AUTO_INCREMENT = 1"
                cursor.execute(sql)
                cursor.execute(sql2)                
                database.commit()
                print("history of cars  removed")
            elif Q == "9":
                break
    except Exception as e:
        list_error.append(str(e))

# -----------------------------------------------------------------------------------------
def chek_information(information):
    if None in information[:2]:
        return None
    else:
        return information
# --------------------------------------------------------------------------------------
def number():
    try:
        cursor.execute("SELECT COUNT(*) FROM available_car ")
        result = cursor.fetchone()
        if result[0]> 30 :
            return None
        else:
            return result[0]
    except Exception as e:
        list_error.append(str(e))
# ----------------------------------------------------------------------------------------------------------------    
def main():
    e=None
    while True:
        while True:
            if number() == None:
                print("There is no space available in the parking lot")
                q=str(input("\n***main menu***\n2-exit\n3-vip\n4-admin\nplease enter a number-->> "))
                if q == "2" :
                    information=get_information(q)
                    if chek_information(information) == None :
                        print("Information incomplete. Returning to main menu.")
                        continue
                    factor=exit(information[0],information[1],information[2])
                    if factor != None:
                        print(f"time spend {(factor[1])}\nPayable Amount {int(factor[0]):,}")
                    else:
                        print("we do not have this car")
                elif q == "3" :
                    information=get_information(q)
                    if chek_information(information) == None :
                        print("Information incomplete. Returning to main menu.")
                        continue
                    code=enter_vip(information[0],information[1])
                    print("Payable Amount 20,000")
                    print(f"your vip code is {code}")
                elif q == "4":
                    e=enter_admin()
                    if e == "3" :
                        break
                else:
                    print("enter a correct number")
            else:
                break
        if e == "3" :
            break
        else:
            q=str(input("\n***main menu***\n1-enter\n2-exit\n3-vip\n4-admin\nplease enter a number-->> "))
            if q == "1" :
                information=get_information(q)
                if chek_information(information) == None :
                    print("Information incomplete. Returning to main menu.")
                    continue
                enter_data(information[0],information[1])
            elif q == "2" :
                information=get_information(q)
                if chek_information(information) == None :
                    print("Information incomplete. Returning to main menu.")
                    continue
                factor=exit(information[0],information[1],information[2])
                if factor != None:
                    print(f"time spend {(factor[1])}\nPayable Amount {int(factor[0]):,}")
                else:
                    print("we do not have this car")
            elif q == "3" :
                information=get_information(q)
                if chek_information(information) == None :
                    print("Information incomplete. Returning to main menu.")
                    continue
                code=enter_vip(information[0],information[1])
                print("Payable Amount 20,000")
                print(f"your vip code is {code}")
            elif q == "4":
                e=enter_admin()
                if e == "3" :
                    break
            else:
                print("enter a correct number")
# --------------------------------------------------------------------------------------------
start_admin()
main()
        



