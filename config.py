import os
import logging

APP_ROOT = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
   
# Load .env file using:
from dotenv import load_dotenv

# load_dotenv('.env')
load_dotenv(dotenv_path)

logging.basicConfig(
    filename = os.path.join(APP_ROOT,'logs/python_flask.log'),
    level = logging.DEBUG,
    format = '%(asctime)s - %(name)s - %(levelname)s : %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

DATABASE    = os.getenv("DATABASE")
DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = os.getenv("DB_PORT")
SECRET_KEY  = os.getenv("SECRET_KEY")

# Database
SQLALCHEMY_DATABASE_URI = 'mysql://{0}@{1}/{2}'.format(DB_USER,DB_HOST,DATABASE)
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config:
    def __init__(self):
        self.app_base_path = APP_ROOT
 



