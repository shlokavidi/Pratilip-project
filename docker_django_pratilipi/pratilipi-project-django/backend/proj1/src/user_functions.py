import argparse
import mysql.connector
from conn2db import MyDBConnection
import json

import logging.config
import logging

import defines
import parameters
import conn2db

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

defines.udb_conn = MyDBConnection(defines.USER_MYSQL_STR)
udb_conn = defines.udb_conn

def do_del_or_update_user(post_data, action):
    
    user_id = 'user_id'
    msg = ''

    user_fname = 'firstname'
    user_lname = 'lastname'
    user_email = 'email'
    user_ph = 'phone_number'
    resupdate_user = {
            'status' : '0',
            'message': ''
            }

    user_id, resp_message = parameters.get_parameter(user_id, post_data)
    if resp_message:
        return(resp_message)

    sql_cmd = "SELECT * from user_info where user_id = %d;" % user_id
    user_data = udb_conn.query(sql_cmd)
    logger.info(user_data)

    if len(user_data) == 1: # Perform action only if one record found

        if action == 'DELETE_RECORD':
            sql_cmd = "DELETE from user_info where user_id = %d;" % user_id
            udb_conn.execute(sql_cmd)
            udb_conn.execute("Commit;")
            msg = ("Record with user_id %s was successfully deleted" % user_id)
            resp_update_user = {
                    'status' : '1',
                    'message': msg
                    }
        else:

            firstname, resp_message = parameters.get_parameter(user_fname, post_data)
            if resp_message:
                return(resp_message)
    
            lastname, resp_message = parameters.get_parameter(user_lname, post_data)
            if resp_message:
                return(resp_message)

            email, resp_message = parameters.get_parameter(user_email, post_data)
            if resp_message:
                return(resp_message)

            phone_number, resp_message = parameters.get_parameter(user_ph, post_data)
            if resp_message:
                return(resp_message)

            # Got all the detail for updating
            values = (firstname, lastname, email, phone_number, user_id)
            sql_cmd = ("UPDATE user_info SET Firstname = '%s', \
                    Lastname = '%s', Email = '%s', Phone_number = '%s' \
                    WHERE User_id = '%s';" % (firstname, lastname, \
                    email, phone_number, user_id))
            '''
            sql_cmd = """UPDATE user_info SET Firstname =%s
                            Lastname =%s, Email =%s, Phone_number =%s
                            WHERE User_id=%s; % (firstname, lastname, email, phone_number, user_id)"""
            sql_cmd = """UPDATE user_info SET Firstname =%s
                            Lastname =%s, Email =%s, Phone_number =%s
                            WHERE User_id=%s;"""
            '''
            logger.info(sql_cmd)
            udb_conn.execute(sql_cmd)
            # udb_conn.execute(sql_cmd, values)
            # udb_conn.execute(sql_cmd, (firstname, lastname, email, phone_number, user_id))
            #user_data = udb_conn.query(sql_cmd)
            #logger.info(user_data)
            udb_conn.execute("Commit;")
            resp_update_user = {
                    'status' : '0',
                    'message': ("Successfully updated user_id %s "% user_id)
                    }
    
    else:
        msg = ("number of records are %d" % len(user_data))
        resp_update_user = {
                'status' : '1',
                'message': 'Can not perform action as ' + msg,
                }
        # IMPROVEMENT: list the records found. So user can decide which one to delete
    return(resp_update_user)




def do_get_user(post_data):


    user_id = 'user_id'
    msg = ''

    user_id, resp_message = parameters.get_parameter(user_id, post_data)
    if resp_message:
        return(resp_message)

    # IMPROVEMENT: User should be able to get user details with 
    # any know field. For exmpl: SELECT lname FROM user_info WHERE fname = '<field>';

    sql_cmd = "SELECT * from user_info where user_id = %d;" % user_id
    user_data = udb_conn.query(sql_cmd)
    logger.info(user_data)

    # There could be some integers. Convert them to string
    user_data = [tuple(map(lambda i: str(i), tup)) for tup in user_data]

    # Get table header to form the JSON value pair
    sql_cmd = "describe user_info;"

    result = udb_conn.query(sql_cmd)
    table_header = [i[0] for i in result]
    logger.info(table_header)

    user_data_to_send = [dict(zip(table_header, fields)) for fields in user_data]

    # IMPROVEMENT: Provide meaningful message when no record found

    resp_get_user = {
                    'status' : '0',
                    'message': msg,
                    'user_data' : user_data_to_send
                    }
    return(resp_get_user)

def do_add_user(post_data): 

    user_fname = 'firstname'
    user_lname = 'lastname'
    user_email = 'email'
    user_ph = 'phone_number'
    user_id  = 'user_id'
    
    user_id, resp_message = parameters.get_parameter(user_id, post_data)
    if resp_message:
        return resp_message
    udb_conn.execute("use user_db;")
    sql_cmd = "SELECT * FROM user_info where user_id = %d;" % user_id

    add_content = udb_conn.query(sql_cmd)
    if len(add_content) == 1:
        msg = "User_id %d already exists" % user_id
        resp_msg = {
                'status' : '1',
                'message' : msg
                }
        return resp_msg

    firstname, resp_message = parameters.get_parameter(user_fname, post_data)
    if resp_message:
        return(resp_message)

    lastname, resp_message = parameters.get_parameter(user_lname, post_data)
    if resp_message:
        return(resp_message)

    email, resp_message = parameters.get_parameter(user_email, post_data)
    if resp_message:
        return(resp_message)

    phone_number, resp_message = parameters.get_parameter(user_ph, post_data)
    if resp_message:
        return(resp_message)

    sql_cmd = "INSERT INTO user_info VALUES (%d, '%s', '%s', '%s', '%s');" \
            % (user_id, firstname, lastname, email, phone_number)
    udb_conn.execute(sql_cmd)
    udb_conn.execute("commit;")
    # user_id_value = user_id_value + 1
    resp_msg = { 'status' : '0', 'message' : 'Success'}
    
    return resp_msg

