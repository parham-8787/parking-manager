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
def get_information():
    try:
        while True:
            pelak = input("Pelak : ")
            if len(pelak) == 6 and pelak[2].isalpha() and pelak[:2].isnumeric() and pelak[3:].isnumeric():
                break
            else:
                print("Pelak Not Corrected...")
                q2=str(input("do you want to continue(yes or no)-->>")).lower()
                if q2 == "no":
                    return None , None , None
                continue
        while True :
            telephone = str(input("Telephone : "))
            if len(telephone) == 11 and telephone.startswith("09"):
                break
            else:
                print("Telephone Not Corrected...")
                q2=str(input("do you want to continue(yes or no)-->>")).lower()
                if q2 == "no":
                    return pelak , None ,None
            continue

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
            return
        exit_time=dt.now()
        cursor.execute("SELECT enter_time FROM available_car WHERE pelak=%s and telephone=%s ",(pelak,telephone))
        results2 = cursor.fetchone()
        print(results2)
        enter_time = dt.strptime(results2[0], "%Y-%m-%d %H:%M:%S")
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
def enter_vip(telephone):
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
        sql = "INSERT INTO vip(join_time ,expire_time ,telephone,vip_code) values(%s,%s,%s ,%s)"
        values =(enter_time,expire_time,telephone,code)
        cursor.execute(sql,values)
        database.commit()
        return code
    except Exception as e:
        list_error.append(str(e))
# ---------------------------------------------------------------------------------------------
def admin(username,password):
    try:
        cursor.execute("SELECT COUNT(*) FROM admin")
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.execute("INSERT INTO admin(username, password) VALUES(%s, %s)", (username, password))
            database.commit()
            print("Default admin added.")
        else:
            print("Admin already exists.")
    except Exception as e:
        list_error.append(str(e))
# -------------------------------------------------------------------------------------------
def enter_admin():
    while True:
        try:
            username=str(input("please enter your username : "))
            password=str(input("please enter your password : "))
            cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
            admin =cursor.fetchone()
            if admin:
                Q=str(input("1-see error\n2-sleep Script\n3-shut down script\n(please enter a numner)-->> "))
                if Q == "1":
                    for i in list_error:
                        print(i)
                elif Q == "2":
                    while True:
                        username=str(input("please enter your username : "))
                        password=str(input("please enter your password : "))
                        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
                        admin =cursor.fetchone()
                        if admin:
                            break
                elif Q == "3":
                    print("Be assured that with this approach,\nthe list of errors will be cleared,\nand if the database tables do not exist at startup,\nthey will be created again automatically\n-->> ")
                    return None
            else:
                print("not found admin")
                q=str(input("do you want continue(yes or no)-->> ")).lower()
                if q == "yes":
                    continue
                else:
                    break
        except Exception as e:
            list_error.append(str(e))

# -----------------------------------------------------------------------------------------
def chek_information(information):
    if None in information[:2]:
        return None
# --------------------------------------------------------------------------------------
def number():
    try:
        cursor.execute("SELECT COUNT(*) FROM available_car ")
        result = cursor.fetchone()
        if result[0] >30 :
            return None
    except Exception as e:
        list_error.append(str(e))
# ----------------------------------------------------------------------------------------------------------------    
def main():
    while True:
        while True:
            if number() == None:
                print("There is no space available in the parking lot")
                q=str(input("2-exit\n3-vip\n4-admin\nplease enter a number-->> "))
                if q == "2" :
                    information=get_information()
                    if chek_information(information) == None :
                        print("Information incomplete. Returning to main menu.")
                        continue
                    factor=exit(information[0],information[1],information[2])
                    print(f"time spend{factor[1]}\nPayable Amount{(factor[0]):,}")
                elif q == "3" :
                    information=get_information()
                    if chek_information(information) == None :
                        print("Information incomplete. Returning to main menu.")
                        continue
                    code=enter_vip(information[1])
                    print("Payable Amount 20,000")
                    print(f"your vip code is {code}")
                elif q == "4":
                    e=enter_admin()
                    if e == None :
                        break
                else:
                    print("enter a correct number")
            else:
                break
        q=str(input("1-enter\n2-exit\n3-vip\n4-admin\nplease enter a number-->> "))
        if q == "1" :
            information=get_information()
            if chek_information(information) == None :
                print("Information incomplete. Returning to main menu.")
                continue
            enter_data(information[0],information[1])
        elif q == "2" :
            information=get_information()
            if chek_information(information) == None :
                print("Information incomplete. Returning to main menu.")
                continue
            factor=exit(information[0],information[1],information[2])
            print(f"time spend{factor[1]}\nPayable Amount{(factor[0]):,}")
        elif q == "3" :
            information=get_information()
            if chek_information(information) == None :
                print("Information incomplete. Returning to main menu.")
                continue
            code=enter_vip(information[1])
            print("Payable Amount 20,000")
            print(f"your vip code is {code}")
        elif q == "4":
            e=enter_admin()
            if e == None :
                break
        else:
            print("enter a correct number")
# --------------------------------------------------------------------------------------------
admin("parham","87871387")
main()
        



