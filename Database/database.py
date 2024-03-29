from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sys import stderr
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError, InterfaceError
import urllib

Persisted = declarative_base()

def connect_to_database(authority, port, database_name, username, password):
    try:
        url = WarehouseDatabase.construct_mysql_url(authority, port, database_name, username, password)
        warehouse_database = WarehouseDatabase(url)
        warehouse_database.ensure_tables_exist()
        return warehouse_database.create_session()
    except InterfaceError as ex:
        print(f'Cannot connect to database! Did you type the authority/port correctly?\nAuthority: {authority}, Port: {port}\nCause: {ex}', file=stderr)
        exit(1)
    except ProgrammingError:
        print(f'Unknown database name! Make sure to create a database named "{database_name}".\nIf you typed the database name correctly then double check your credentials!', file=stderr)
        exit(1)
    except ValueError as exception:
        print(f'Please enter a valid port number!', file=stderr)
    except SQLAlchemyError as exception:
        print('Database setup failed!', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)

class WarehouseDatabase(object):
    @staticmethod
    def construct_mysql_url(authority, port, database, username, password):
        password = urllib.parse.quote_plus(password)
        return f'mysql+mysqlconnector://{username}:{password}@{authority}:{port}/{database}'

    @staticmethod
    def construct_in_memory_url():
        return 'sqlite:///'

    def __init__(self, url):
        self.engine = create_engine(url)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def ensure_tables_exist(self):
        Persisted.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()
