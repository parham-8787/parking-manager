# Parking System Project

## Overview
This is a Python-based parking management system that stores all data in a MySQL database.  
It supports Persian (Shamsi) date and time using the `jdatetime` library, VIP memberships with discounts, and enforces a maximum limit of 30 cars in the parking lot.  
It also includes an admin panel for managing the system and viewing errors.

---

## Features

- **Enter and Exit Cars**
  - Register cars with **license plate (`pelak`)** and **telephone number**.  
  - Validates correct plate and phone formats.

- **Time Tracking & Billing**
  - Calculates parking duration in hours.  
  - Calculates payable amount:
    - Base fee: 5,000
    - Each hour: 10,000
    - VIP discount: 20%

- **VIP Membership**
  - Registers VIP members with a unique randomly generated code.  
  - Membership valid for 1 year.  
  - VIP discount applied automatically on exit.

- **Parking Capacity Limit**
  - Prevents entry if there are already 30 cars in the parking lot.

- **Admin Panel**
  - View system errors.  
  - Sleep the script (pause until admin logs in again).  
  - Shut down the script safely.  
  - Add or remove admins.  
  - View any table (`cars`, `available_car`, `vip`).  
  - Clear car history.

- **Error Logging**
  - All exceptions and errors are stored in a list for review by the admin.

---

## Database

The project creates the following tables in MySQL:

1. **available_car**
   - `ID` (Primary Key, Auto Increment)  
   - `pelak` (License Plate)  
   - `telephone`  
   - `enter_time` (Shamsi datetime)

2. **cars**
   - `ID` (Primary Key, Auto Increment)  
   - `pelak`  
   - `telephone`  
   - `enter_time`  
   - `exit_time`  
   - `time_spend` (in hours)  
   - `factor` (payment amount)

3. **vip**
   - `ID` (Primary Key, Auto Increment)  
   - `vip_code`  
   - `telephone`  
   - `pelak`  
   - `join_time`  
   - `expire_time`

4. **admin**
   - `ID` (Primary Key, Auto Increment)  
   - `username`  
   - `password`

---

## Using `.env` File
To keep your database credentials secure, create a `.env` file in the project folder with:

```env
db_host=localhost
db_user=root
db_password=your_password
db_port=3306
The Python code automatically reads these values using python-dotenv:
from dotenv import load_dotenv
import os

load_dotenv()
db_host = os.getenv("db_host")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_port = os.getenv("db_port")
Installation

Install dependencies using pip:
pip install -r requirements.txt
How to Run

Make sure MySQL is running.

Run the script:
python parking.py

Sample Usage

Enter a Car
***main menu***
1-enter
2-exit
3-vip
4-admin
please enter a number-->> 1
Pelak : 12A345
Telephone : 09123456789
Data Has Been Inserted..Sample Usage

Exit a Car
***main menu***
1-enter
2-exit
3-vip
4-admin
please enter a number-->> 2
Pelak : 12A345
Telephone : 09123456789
Time spend: 2.5
Payable Amount: 30,000

Register VIP
***main menu***
1-enter
2-exit
3-vip
4-admin
please enter a number-->> 3
Pelak : 12A345
Telephone : 09123456789
Payable Amount 20,000
Your VIP code is: 123456


Admin Panel
***admin menu***
1-see error
2-sleep Script
3-shut down script
4-new admin
5-remove admin
6-admin list
7-show tables
8-removed cars history
9-exit