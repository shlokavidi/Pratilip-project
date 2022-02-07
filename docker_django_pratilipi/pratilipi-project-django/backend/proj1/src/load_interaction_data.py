import mysql.connector
import pandas as pd

import defines
import logging
import conn2db
from conn2db import MyDBConnection

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# ildb_conn = MyDBConnection(defines.INERACTION_MYSQL_STR)
ildb_conn = defines.udb_conn

def read_interaction_file(fname_with_path):
    interactiondata = pd.read_csv(fname_with_path, index_col = False,
    delimiter = ',', dtype = {"Content_id" : int, "User_id" : int, 
        "Read_count" : int, "Like_count" : int})
    logger.info(interactiondata.head())
    return interactiondata

def create_table():

    ildb_conn.execute("CREATE DATABASE IF NOT EXISTS interaction_db;")
    ildb_conn.execute("USE interaction_db;")
    ildb_conn.execute('''CREATE TABLE IF NOT EXISTS interaction_table 
        (Content_id INT, User_id INT, Read_count INT, Like_count INT,\
                PRIMARY KEY(Content_id, User_id));''')
    logger.info("******* TABLE CREATED *******")

def load_csv_to_sql_interaction(interactiondata):
    msg = ''
    curr = ildb_conn.cursor
    for i, row in interactiondata.iterrows():
        try:
            sql_cmd = ("INSERT INTO interaction_db.interaction_table VALUES (%s, %s, %s, %s)" )
            curr.execute(sql_cmd, tuple(row))
        except Exception as load_error:
            logger.error(load_error)
            msg = str(load_error)

    ildb_conn.execute("Commit")
    # msg = 'Insertion successful'
    return msg


def upload_interaction_data(ftype, fname_with_path):
    interactiondata = read_interaction_file(fname_with_path)
    create_table()
    msg = load_csv_to_sql_interaction(interactiondata)
    if msg:
        response_msg = { 'status' : '1', \
            'message' : msg}
    else:
        response_msg = { 'status' : '0', \
            'message' : 'File %s (%s) uploaded successfully' \
            % (ftype, fname_with_path)}

    return(response_msg)

