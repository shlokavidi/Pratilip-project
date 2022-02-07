import mysql.connector
import pandas as pd

import defines
import logging
import conn2db
from conn2db import MyDBConnection

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# cldb_conn = MyDBConnection(defines.CONTENT_MYSQL_STR)
cldb_conn = defines.udb_conn

def read_content_file(fname_with_path):
    contentdata = pd.read_csv(fname_with_path, index_col = False,
    delimiter = ',', dtype = {"Content_id" : int,
        "Title" : "string", "Story" : "string",
        "Date_published" : "string", "Last_accessed" : "string"})
    logger.info(contentdata.head())
    return contentdata

def create_table():

    cldb_conn.execute("CREATE DATABASE IF NOT EXISTS contents_db;")
    cldb_conn.execute("USE contents_db;")
    cldb_conn.execute('''CREATE TABLE IF NOT EXISTS contents_table (Content_id INT PRIMARY KEY,
            Title varchar(50), Story varchar(100), Date_published varchar(10),
            Last_accessed varchar(10));''')
    logger.info("******* TABLE CREATED *******")

def load_csv_to_sql_content(contentdata):
    msg = ''
    curr = cldb_conn.cursor
    for i, row in contentdata.iterrows():
        print( row)
        try:
            sql_cmd = ("INSERT INTO contents_db.contents_table VALUES (%s, %s, %s, %s, %s)" )
            logger.info(sql_cmd)
            curr.execute(sql_cmd, tuple(row))
        except Exception as load_error:
            logger.error(load_error)
            msg = str(load_error)

    cldb_conn.execute("Commit")
    # msg = 'Insertion successful'
    return msg


def upload_content_data(ftype, fname_with_path):
    contentdata = read_content_file(fname_with_path)
    create_table()
    msg = load_csv_to_sql_content(contentdata)
    if msg:
        response_msg = { 'status' : '1', \
            'message' : msg}
    else:
        response_msg = { 'status' : '0', \
            'message' : 'File %s (%s) uploaded successfully' \
            % (ftype, fname_with_path)}

    return(response_msg)

