import mysql.connector
import logging
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

mydb = mysql.connector.connect(
    host = MYSQL_HOST,
    user = MYSQL_USER,
    password = MYSQL_PASSWORD
)

mycursor = mydb.cursor(buffered=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection():
    global mydb, mycursor
    mydb = mysql.connector.connect(
    host = MYSQL_HOST,
    user = MYSQL_USER,
    password = MYSQL_PASSWORD
    )

    mycursor = mydb.cursor(buffered=True)

def check_connection():
    if mydb:
        logging.info("Connected to RDS success.")
    else:
        logging.error("Connected to RDS failed.")

def show_tables():
    sql = "SHOW COLUMNS FROM chat_broad.chat_record;"
    mycursor.execute(sql)
    row = mycursor.fetchall()

    for result in row:
        print("column name: ",result[0], "\ttype: ", result[1])

def add_data(comment = None, image = None):
    sql = "INSERT INTO chat_broad.chat_record (comment, image) VALUES (%s, %s)"
    val = (comment, image)
    mycursor.execute(sql, val)

    mydb.commit()

def show_data():
    sql = "SELECT * FROM chat_broad.chat_record;"
    mycursor.execute(sql)
    row = mycursor.fetchall()

    for result in row:
        print(result)

def get_data():
    check_connection()
    sql = "SELECT * FROM chat_broad.chat_record;"
    mycursor.execute(sql)
    row = mycursor.fetchall()

    return row

def manage_data():
    actions = {
        'show_tables': show_tables,
        'add_data': add_data,
        'show_data': show_data,
        'get_data': get_data
    }

    action = input("Input the action you want to do (show_tables, add_data, show_data, get_data): ").strip()

    if action in actions:
        if action == 'add_data':
            comment = input("Input comment: ")
            image = input("Input image: ")
            actions[action](comment, image)
        else:
            actions[action]()
    else:
        pass

def delete_data():
    sql = "DELETE FROM chat_broad.chat_record WHERE id < 45;"
    mycursor.execute(sql)
    mydb.commit()

delete_data()