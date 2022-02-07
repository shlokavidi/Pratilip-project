import argparse
import mysql.connector
from conn2db import MyDBConnection
import json

import defines
import parameters

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django import forms

import user_functions
import content_functions
import interaction_functions

from load_user_data import upload_user_data
from load_content_data import upload_content_data
from load_interaction_data import upload_interaction_data

import logging.config
import logging

logging.config.fileConfig(fname = defines.LOGGER_FILE_PATH,
                                    disable_existing_loggers = False)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# This is global to his module. Just like that staring with 101. No reason.
# It will keep incrementing
user_id_value = 101 

# db_conn = MyDBConnection()

class TheValidationForm(forms.Form):
    csv_file = forms.CharField()
    file_type = forms.CharField()

def post_receive_file(request):

    the_form = TheValidationForm(request.POST, request.FILES)
    if request.POST:
        logger.info("Got FORM data")
        form_data = True # we processed form-data. So body processing can be skipped
        # the_form = TheValidationForm(request.POST, request.FILES)
        '''
        logger.info(the_form)
        if not the_form.is_valid(): # some fields missing or invalid
            file_type = request.POST['file_type']
            csv_file_data = request.FILES['csv_file']
            csv_file_name = csv_file_data.name
            logger.info("csv_file_name:%s" % csv_file_name)
            logger.info("file_type:%s" % file_type)
            form_err = the_form.errors.as_json()
            logger.error(form_err)
            response_msg = { 'status' : '1', 
                    'message' : form_err}
            logger.info(response_msg)
            # response_msg.update(the_form.errors.as_json())
            # response_msg.update(str(form_err))
            return(form_data, response_msg)
        else:
            logger.info(the_form.errors.as_json())
        if request.FILES['file_type']:
            file_type = request.POST['file_type']
        else:
            response_msg = { 'status' : '1', \
                'message' : 'file_type not provided' }
            return(form_data, response_msg)
        '''
        file_type = request.POST['file_type']
        csv_file_data = request.FILES['csv_file']
        csv_file_name = csv_file_data.name
        logger.info("csv_file_name:%s" % csv_file_name)
        logger.info("file_type:%s" % file_type)
        file_sys = FileSystemStorage()
        fname_with_path = defines.DATA_FILE_PATH+csv_file_name
        filename = file_sys.save(fname_with_path, csv_file_data)
        if file_type == 'user_data':
            response_msg = upload_user_data(file_type, fname_with_path)
        elif file_type == 'content_data': 
            response_msg = upload_content_data(file_type, fname_with_path)
        elif file_type == 'interaction_data': 
            response_msg = upload_interaction_data(file_type, fname_with_path)
        else:
            response_msg = { 'status' : '1', \
                'message' : '%s is an invalid file type'% file_type }
    else:
        if request.body:
            logger.info("Got body data")
        form_data = False
        response_msg = None # Not used further. So OK to pass None


    return(form_data, response_msg)

@csrf_exempt
def process_api_request(req):

    user_api = 'user_api'
    response_msg = {"status" : "0", "message" : ""} # status 0 is success
    err_msg = ''
    api = ''
    

    form_data, response_msg = post_receive_file(req)
    if form_data: # We processed form-data. Send response
        return HttpResponse(json.dumps(response_msg), content_type='text/plain')

    post_data = json.loads(req.body)
    logger.info(post_data)
    
    api, response_msg = parameters.get_parameter(user_api, post_data)
    logger.info(response_msg)
    if response_msg:
        return HttpResponse(json.dumps(response_msg), content_type='text/plain')

    logger.info("API:%s" % api)
    # User APIs
    if api == defines.ADD_USER_API:
        response_msg = user_functions.do_add_user(post_data)
    elif api == defines.GET_USER_API:
        response_msg = user_functions.do_get_user(post_data)
    elif api == defines.UPDATE_USER_API:
        response_msg = user_functions.do_del_or_update_user(post_data, 'UPDATE_RECORD')
    elif api == defines.DELETE_USER_API:
        response_msg = user_functions.do_del_or_update_user(post_data, 'DELETE_RECORD')
    # Content APIs
    elif api == defines.ADD_CONTENT_API:
        response_msg = content_functions.do_add_content(post_data)
    elif api == defines.GET_CONTENT_API:
        response_msg = content_functions.do_get_content(post_data)
    elif api == defines.UPDATE_CONTENT_API:
        response_msg = content_functions.do_del_or_update_content(post_data, 'UPDATE_RECORD')
    elif api == defines.DELETE_CONTENT_API:
        response_msg = content_functions.do_del_or_update_content(post_data, 'DELETE_RECORD')
    elif api == defines.NEW_CONTENT_API:
        response_msg = content_functions.get_new_content(post_data)
    elif api == defines.TOP_CONTENT_API:
        response_msg = content_functions.get_top_content(post_data)

    # Interaction APIs
    elif api == defines.READ_CONTENT_API:
        response_msg = interaction_functions.validate_user(post_data, 'UPDATE_READ')
    elif api == defines.LIKE_CONTENT_API:
        response_msg = interaction_functions.validate_user(post_data, 'UPDATE_LIKE')

    else:
        err_msg = ("*** ERROR *** no such API(%s)" % api)
        logger.error(err_msg)
        response_msg = { 'status' : '1', 'message' : err_msg}
    return HttpResponse(json.dumps(response_msg), content_type='text/plain')



def main():
    process_api_request()


if __name__ == "__main__":
    main()
