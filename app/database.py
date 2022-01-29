from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2             # for querying of POSTGRES database
from psycopg2.extras import RealDictCursor
from .config import settings
import time

# Has the format 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

''' When not using SQLAlchemy, the below can be used to connect to a database
# Use try statements when connecting to databases in case they don't immediately connect
while True:
    try:
        # A PSYCOPG2 connect requires: database = the name of the database name in PGRS
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='standard', cursor_factory=RealDictCursor)

        # Code is straight from library details
        cursor = conn.cursor()
        print('Database connection was successful')
        break

    except Exception as error:
        print('Connection to database failed')
        print('Error: ', error)
        time.sleep(5)
'''

# The SessionLocal is responsible for connecting to the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()