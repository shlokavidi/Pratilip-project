import argparse
import pandas as pd
from conn2db import MyDBConnection

import logging.config
import logging

import defines
import parameters
import conn2db

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# idb_conn = MyDBConnection(defines.INERACTION_MYSQL_STR)
idb_conn = defines.udb_conn

def validate_user(post_data, action):
    user_id = 'user_id'

    user_id, resp_message = parameters.get_parameter(user_id, post_data)
    if resp_message:
        return resp_message

    sql_cmd = ("SELECT * FROM user_db.user_info where user_id = %d;" %  user_id)
    logger.info(sql_cmd)
    user_data = idb_conn.query(sql_cmd)
    logger.info(user_data)
    
    if len(user_data) == 1 and action == 'UPDATE_READ':
        temp = read_update(post_data)
        return temp
    elif len(user_data) ==1 and action == 'UPDATE_LIKE':
        temp = like_update(post_data)
        return temp

def read_update(post_data):
    content_id  = 'content_id'
    user_id = 'user_id'

    content_id, resp_message = parameters.get_parameter(content_id, post_data)
    if resp_message:
        return resp_message

    user_id, resp_message = parameters.get_parameter(user_id, post_data)
    if resp_message:
        return resp_message


    sql_cmd = "select * from interaction_db.interaction_table where \
            Content_id = %d and User_id = %d;" % (content_id, user_id)
    check = idb_conn.query(sql_cmd)
    logger.info(len(check))
    if len(check) == 0:
        sql_cmd = "insert into interaction_db.interaction_table values\
                (%d, %d, 0, 0);" % (content_id, user_id)
        idb_conn.execute(sql_cmd)
    sql_cmd = "UPDATE interaction_db.interaction_table SET \
            read_count = read_count + 1 WHERE content_id = %d and user_id = %d;"\
            % (content_id, user_id)
    idb_conn.execute(sql_cmd)
    idb_conn.commit()
    msg = "User %d finished reading content %d and read count increased by 1"\
            % (user_id, content_id)
    resp_mes = { 'status' : '0',
                'message' : msg
                }
    return resp_mes


def like_update(post_data):
    content_id  = 'content_id'
    user_id = 'user_id'

    content_id, resp_message = parameters.get_parameter(content_id, post_data)
    if resp_message:
        return resp_message

    user_id, resp_message = parameters.get_parameter(user_id, post_data)
    if resp_message:
        return resp_message

    sql_cmd = "select like_count from interaction_db.interaction_table where \
            Content_id = %d and User_id = %d;" % (content_id, user_id)
    check = idb_conn.query(sql_cmd)

    if len(check) == 0:
        msg = "You cannot like a content you haven't finished readind yet! \n \
                User %d has not finished reading content %d yet..." % \
                (user_id, content_id)

    else:
        if check[0][0] == 1:
            msg = "User %d has already liked content %d!" \
                    % (user_id, content_id)

        else:
            sql_cmd = "UPDATE interaction_db.interaction_table SET \
            like_count =  1 WHERE content_id = %d and user_id = %d;"\
            % (content_id, user_id)
            idb_conn.execute(sql_cmd)
            idb_conn.commit()
            msg = "User %d like content %d!" \
                     % (user_id, content_id)

    resp_mes = { 'status' : '0',
                'message' : msg
                }
    return resp_mes
