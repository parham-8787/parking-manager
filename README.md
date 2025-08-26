# Parking System Project

## Overview
This is a Python-based parking management system that stores all data in a MySQL database. It supports Persian (Shamsi) date and time using the `jdatetime` library, VIP memberships with discounts, and enforces a limit on the number of cars in the parking lot.

## Features
- **Enter and Exit Cars**: Records car license plate (`pelak`) and telephone number when entering or exiting the parking.
- **Time Tracking**: Calculates parking duration in hours.
- **Billing**: Automatically calculates the payable amount based on time spent.
  - Base fee: 5,000
  - Each hour: 10,000
  - VIP discount: 20%
- **VIP Membership**: 
  - Stores VIP users with a unique code.
  - Valid for 1 year from join date.
- **Maximum Parking Limit**: Prevents entry if parking has more than 30 cars.
- **Admin Panel**:
  - View errors.
  - Pause or stop the script.

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
   - `join_time`
   - `expire_time`

4. **admin**
   - `ID` (Primary Key, Auto Increment)
   - `username`
   - `password`

## Using `.env` File
This project uses a `.env` file to securely store database credentials. Using `.env` helps:

- Avoid hardcoding sensitive information like database username and password.
- Make the code portable to other machines without changing the script.

Create a `.env` file in the project folder with:
db_host=localhost
db_user=root
db_password=your_password
db_port=3306


The Python code reads these values automatically using `python-dotenv`:

```python
from dotenv import load_dotenv
import os

load_dotenv()
db_host = os.getenv("db_host")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_port = os.getenv("db_port")
```

# How to Run
Make sure MySQL is running.

Install dependencies (see below).

Run the script:

python parking.py
Follow the prompts in the terminal to enter, exit, or register VIPs.

# Sample Usage
1-enter
2-exit
3-vip
4-admin
please enter a number-->> 1
Pelak : 12A345
Telephone : 09123456789
Data Has Been Inserted...

# Installing Requirements

Install the required Python libraries using pip:

pip install -r requirements.txt

