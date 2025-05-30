import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()



db = SQLAlchemy()

class DBConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv('PARAM2_DB')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
