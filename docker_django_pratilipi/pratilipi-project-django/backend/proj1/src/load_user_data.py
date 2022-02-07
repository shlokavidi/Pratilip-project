import mysql.connector
import pandas as pd

import defines
import logging
import conn2db
from conn2db import MyDBConnection

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# uldb_conn = MyDBConnection(defines.USER_MYSQL_STR)
uldb_conn = defines.udb_conn

def read_user_file(fname_with_path):
    userdata = pd.read_csv(fname_with_path, index_col = False,
    delimiter = ',', dtype = {"User_id" : int,
        "Firstname" : "string", "Lastname" : "string",
        "Email" : "string", "Phone_number" : "string"})
    logger.info(userdata.head())
    return userdata

def create_table():

    uldb_conn.execute("CREATE DATABASE IF NOT EXISTS user_db;")
    uldb_conn.execute("USE user_db;")
    uldb_conn.execute('''CREATE TABLE IF NOT EXISTS user_info (User_id Integer(20) 
        primary key,
        Firstname varchar(20), Lastname varchar(20), Email varchar(40),
        Phone_number varchar(10));''')
    print("******* TABLE CREATED *******")



def load_csv_to_sql_user(userdata):
    msg = ''
    curr = uldb_conn.cursor
    for i, row in userdata.iterrows():
        print( row)
        try:
            sql_cmd = ("INSERT INTO user_db.user_info VALUES (%s, %s, %s, %s, %s)" )
            logger.info(sql_cmd)
            curr.execute(sql_cmd, tuple(row))
        except Exception as load_error:
            logger.error(load_error)
            msg = str(load_error)
            
    uldb_conn.execute("Commit")
    # msg = 'Insertion successful'
    return msg


def upload_user_data(ftype, fname_with_path):
    userdata = read_user_file(fname_with_path)
    create_table()
    msg = load_csv_to_sql_user(userdata)
    if msg:
        response_msg = { 'status' : '1', \
            'message' : msg}
    else:
        response_msg = { 'status' : '0', \
            'message' : 'File %s (%s) uploaded successfully' \
            % (ftype, fname_with_path)}

    return(response_msg)


