'''USER_MYSQL_STR
Here, we have defined the constants we use in our project.

CONFIG_FILE - path to the file containing the required credentials (MySQL and Snowflake)
TABLE_NAME - name of MySQL table
MYSQL_DB_NAME - name of MySQL database

SNOWFLAKE_STR - string to represent snoflake
MYSQL_STR - string to respent MySQL

CSV_FILE - path to sample data
LOGGER_FILE_PATH - path to the logger file

'''


# CONFIG_FILE = "../config/app_config.ini"
CONFIG_FILE = "proj1/config/app_config.ini" #for django
TABLE_NAME = 'user_info'
MYSQL_DB_NAME = 'user_db'
MYSQL_STR = 'mysql'
USER_MYSQL_STR = 'user_mysql'
CONTENT_MYSQL_STR = 'content_mysql'
INERACTION_MYSQL_STR = 'interaction_mysql'
# DATA FILE
DATA_FILE_PATH = "proj1/data/"

CSV_FILE = "../data/sample_data.csv"
# LOGGER_FILE_PATH = '../config/app_logger.ini'
LOGGER_FILE_PATH = 'proj1/config/app_logger.ini' # for django


# USER API RELATED
ADD_USER_API = 'add_user'
GET_USER_API = 'get_user'
UPDATE_USER_API = 'update_user'
DELETE_USER_API = 'delete_user'

# CONTENT API RELATED
ADD_CONTENT_API = 'add_content'
GET_CONTENT_API = 'get_content'
UPDATE_CONTENT_API = 'update_content'
DELETE_CONTENT_API = 'delete_content'
NEW_CONTENT_API = 'new_content'
TOP_CONTENT_API = 'top_content'


# USER INTERACTION API
LIKE_CONTENT_API = 'like_content'
READ_CONTENT_API = 'read_content'

udb_conn = ''
