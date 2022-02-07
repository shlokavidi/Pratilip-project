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

# cdb_conn = MyDBConnection(defines.CONTENT_MYSQL_STR)
cdb_conn = defines.udb_conn

def do_add_content(post_data):
    content_id = 'content_id'
    title = 'title'
    story = 'story'
    date_published = 'date_published'
    last_accessed = 'last_accessed'
    user_id = 'user_id'
    read_count = 'read_count'
    like_count = 'like_count'
    
    content_id, resp_message = parameters.get_parameter(content_id, post_data)
    if resp_message:
        return resp_message
    cdb_conn.execute("use contents_db;")
    sql_cmd = "SELECT * FROM contents_table where content_id = %d;" % content_id

    add_content = cdb_conn.query(sql_cmd)
    if len(add_content) == 1:
        msg = "Content_id %d already exists" % content_id
        resp_msg = {
                'status' : '1',
                'message' : msg
                }
        return resp_msg

    else:

        title, resp_message = parameters.get_parameter(title, post_data)
        if resp_message:
            return resp_message

        story, resp_message = parameters.get_parameter(story, post_data)
        if resp_message:
            return resp_message

        date_published, resp_message = parameters.get_parameter(date_published, post_data)
        if resp_message:
            return resp_message

        last_accessed, resp_message = parameters.get_parameter(last_accessed, post_data)
        if resp_message:
            return resp_message

        user_id, resp_message = parameters.get_parameter(user_id, post_data)
        if resp_message:
            return resp_message

        read_count, resp_message = parameters.get_parameter(read_count, post_data)
        if resp_message:
            return resp_message

    like_count, resp_message = parameters.get_parameter(like_count, post_data)
    if resp_message:
        return resp_message
    
    cdb_conn.execute("use contents_db;")
    sql_cmd = 'INSERT INTO contents_table VALUES (%d, "%s", "%s", "%s", "%s", "%s", %d, %d);' % \
            (content_id, title, story, date_published, last_accessed, user_id, read_count, like_count)
    print(sql_cmd)
    logger.info(sql_cmd)
    cdb_conn.execute(sql_cmd)
    cdb_conn.execute("commit;")
    resp_msg = { 'status' : 0, 'message' : 'Success'}
    return resp_msg

def do_get_content(post_data):
    title = 'title'
    content_id = 'content_id'
    msg = ''
    
    content_id, resp_message = parameters.get_parameter(content_id, post_data)
    if resp_message:
        return(resp_message)
    cdb_conn.execute("use contents_db;")
    sql_cmd = 'SELECT * FROM contents_table WHERE content_id = % d' % content_id
    content_data = cdb_conn.query(sql_cmd)
    logger.info(content_data)

    content_data = [tuple(map(lambda i: str(i), tup)) for tup in content_data]
    sql_cmd = "describe contents_table;"

    res = cdb_conn.query(sql_cmd)
    tab_header = [i[0] for i in res]
    logger.info(tab_header) 
    content_data_to_send = [dict(zip(tab_header, fields)) for fields in content_data]

    resp_to_get_content = { 'status' : '0',
                            'message' : msg,
                            'content_data' : content_data_to_send
                            }
    return(resp_to_get_content)


def do_del_or_update_content(post_data, action):
    user_id_str = 'user_id'
    msg = ''

    content_id = 'content_id'
    title = 'title'
    story = 'story'
    date_published = 'date_published'
    last_accessed = 'last_accessed'
    read_count = 'read_count'
    like_count = 'like_count'

    resp_msg = {
            'status' : '0',
            'message' : ''
            }

    content_id, resp_message = parameters.get_parameter(content_id, post_data)
    if resp_message:
        return resp_message

    user_id, resp_message = parameters.get_parameter(user_id_str, post_data)
    if resp_message:
        return(resp_message)

    cdb_conn.execute("use contents_db;")

    sql_cmd = ("SELECT * FROM contents_table WHERE Content_id = %d;" % content_id)
    content_data = cdb_conn.query(sql_cmd)
    logger.info(content_data)

    if len(content_data) == 1:
        if action == 'DELETE_RECORD':
            sql_cmd = ("DELETE FROM contents_table WHERE content_id = %d;" % content_id)
            cdb_conn.execute(sql_cmd)
            cdb_conn.execute("commit;")
            msg = ("Record with user_id %d was successfully deleted" % content_id)
            resp_msg = {
                    'status' : '1',
                    'message' : msg
                    }
        else:
            title, resp_message = parameters.get_parameter(title, post_data)
            if resp_message:
                return resp_message

            story, resp_message = parameters.get_parameter(story, post_data)
            if resp_message:
                return resp_message

            date_published, resp_message = parameters.get_parameter(date_published, post_data)
            if resp_message:
                return resp_message

            last_accessed, resp_message = parameters.get_parameter(last_accessed, post_data)
            if resp_message:
                return resp_message

            read_count, resp_message = parameters.get_parameter(read_count, post_data)
            if resp_message:
                return resp_message
            
            like_count, resp_message = parameters.get_parameter(like_count, post_data)
            if resp_message:
                return resp_message
            values = (title, story, date_published, last_accessed, user_id)
            sql_cmd = ("UPDATE contents_table SET Title = '%s', Story = '%s',\
                    Date_published = '%s', Last_accessed = '%s', User_id = '%s', Read_count = %d,\
                    Like_count = %d WHERE  Content_id = %d;"\
                    % (title, story, date_published, last_accessed, user_id, read_count,\
                    like_count, content_id))

            logger.info(sql_cmd)
            cdb_conn.execute(sql_cmd)
            cdb_conn.execute("commit;")
            msg = ("Successfully updated row with content_id %d" % content_id)
            resp_msg = { 'status' : '0',
                                    'message' : msg
                                    }

    else:
        msg = "number of records are %d." % len(content_data)
        resp_msg = { 'status' : '1',
                        'message' : 'Cannot perform action as ' + msg
                        }

    return resp_msg


def get_new_content(post_data):
    limit = 'limit'
    
    limit, resp_message = parameters.get_parameter(limit, post_data)
    if resp_message:
        return resp_message
    cdb_conn.execute("use contents_db;")
    sql_cmd = ("select * from contents_table order by date_published desc limit %d;" % limit)
    new_content = cdb_conn.query(sql_cmd)
    logger.info(new_content)
    resp_msg = { 'status': '0',
                'message': 'success',
                'content_data': new_content
                }
    return resp_msg

def get_top_content(post_data):
    limit = 'limit'
    
    limit, resp_message = parameters.get_parameter(limit, post_data)
    if resp_message:
        return resp_message
    
    sql_cmd = "select distinct contents_db.contents_table.content_id, title,(read_count+like_count)\
            from contents_db.contents_table, interaction_db.interaction_table where\
            contents_db.contents_table.content_id in\
            (select content_id from interaction_db.interaction_table where read_count +like_count in\
            (select max(read_count + like_count) from interaction_db.interaction_table))\
            order by (read_count + like_count) desc limit %d;" % limit 

    top_content = cdb_conn.query(sql_cmd)
    logger.info(top_content)
    resp_msg = {'status' : '0',
                'message' : 'success',
                'top_content_data' : top_content
                }
    return resp_msg




