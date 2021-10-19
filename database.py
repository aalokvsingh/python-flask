import mysql.connector
from mysql.connector import Error
import os
import config
import logging

# #mysql import and create mysql object
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

MYSQL_HOST = os.getenv("DB_HOST")
MYSQL_USER = os.getenv("DB_USER")
MYSQL_PASSWORD = os.environ.get("DB_PASSWORD")
MYSQL_DB = config.DATABASE

config = {
  'user': MYSQL_USER,
  'password': MYSQL_PASSWORD,
  'host': MYSQL_HOST,
  'database': MYSQL_DB,
  'raise_on_warnings': True
}



def mysql_connect():
    try:
        # connection = mysql.connector.connect(host='localhost',database='rkd',user='root',password='')
        connection = mysql.connector.connect(**config)
        

        if connection.is_connected():
            db_Info = connection.get_server_info()
            logging.debug("Connected to MySQL Server version "+ db_Info)

        return connection

    except Error as e:
        logging.error("Error while connection MySQL")
        return "Error while connection MySQL "+ str(e)
        
    # finally:
    #     if connection.is_connected():
    #         connection.close()
    #         print("MySQL connection is closed")


def executeSelectQuery(query):
    connection  = mysql_connect()
    cursor      = connection.cursor()
    cursor.execute(query)
    # rows        = cursor.fetchall()
    #To get column names with value
    rows = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    connection.commit()
    connection.close()
    return rows
    
def executeInsertQuery(query):
    connection  = mysql_connect()
    cursor      = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()
    return cursor.lastrowid,cursor.rowcount

def executeQuery(query):
    connection  = mysql_connect()
    cursor      = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()
    return cursor.rowcount

def executeUpdateQuery(query):
    connection  = mysql_connect()
    cursor      = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()
    return cursor.rowcount
