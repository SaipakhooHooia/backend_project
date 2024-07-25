import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
import logging
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

mydb = {
    "host" : MYSQL_HOST,
    "user" : MYSQL_USER,
    "password" : MYSQL_PASSWORD
}

pool = MySQLConnectionPool(pool_name="mypool", pool_size=5, **mydb)

connection = pool.get_connection()
mycursor = connection.cursor()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection():
    global connection, mycursor
    pool = MySQLConnectionPool(pool_name="mypool", pool_size=5, **mydb)

    connection = pool.get_connection()
    mycursor = connection.cursor()

def check_connection():
    if connection:
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

    connection.commit()

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
    sql = "DELETE FROM chat_broad.chat_record WHERE id < 47;"
    mycursor.execute(sql)
    connection.commit()
