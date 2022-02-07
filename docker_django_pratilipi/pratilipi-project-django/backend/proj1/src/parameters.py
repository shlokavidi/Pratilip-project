import argparse
import mysql.connector
from conn2db import MyDBConnection
import json

import logging.config
import logging

import defines


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_parameter(key, post_data):

    response_msg = '' # None indicates there is no error
    value = ''

    try:
        value = post_data[key]
        logger.info("value: %s" % value)
        
    except KeyError as err:
        err_msg = ("*** key/value %s is missing in API request" % err)
        response_msg = { 'status' : '1', 'message' : err_msg }
        logger.error(err_msg)
    except Exception as err:
        logger.error("*** %s" % err)
        response_msg = { 'status' : '1', 'message' : err }
    # return HttpResponse(json.dumps(response_msg), content_type='text/plain')
    return value, response_msg


