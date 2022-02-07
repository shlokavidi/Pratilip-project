'''
Establish connections to MySQL 
'''
import mysql.connector
import pandas as pd
import hashlib
import numpy as np
import time
import threading
import defines

from get_config import get_ini_config

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MyDBConnection:

    def __init__(self, db_choice):
        mysql_config = get_ini_config(defines.CONFIG_FILE, db_choice)
        self.conn = mysql.connector.connect(**mysql_config)
        self.cur = self.conn.cursor()
        logger.info("MySQL %s connected" % db_choice)

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def execute(self, sql, params=None):
        #self.cursor.execute(sql)
        logger.info("params:%s" % params)
        logger.info("SQL:%s" % sql)
        self.cursor.execute(sql, params or ())

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql):
        logger.info("SQL: %s" % sql)
        self.cursor.execute(sql)
        return self.fetchall()

    def my_write_pandas(self, df, table_name, schema, quote_identifiers):
        write_pandas(self.conn, df, table_name = table_name,
            schema = schema, quote_identifiers = quote_identifiers)

    def get_table_hash(self, arg):
        reselt_set = get_hash(self.conn, self.cursor, arg)
        return reselt_set
        pass
