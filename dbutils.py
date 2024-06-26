import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_community.utilities.sql_database import SQLDatabase
import pyodbc, struct
from azure.identity import DefaultAzureCredential

def get_conn():
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=True)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    connection_string = config.CONNECTION_STRING
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn

def get_engine():
    pyodbc_conn = get_conn()

    def creator():
        return pyodbc_conn
    
    engine = create_engine("mssql+pyodbc://", creator=creator)

    return engine

def get_db():

    # connection_string = config.CONNECTION_STRING  # "sqlite:///test.db"
    # engine = create_engine(connection_string, echo=False)
    engine = get_engine()
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = Session()

    return db

def get_table_info():

    # connection_string = config.CONNECTION_STRING  # "sqlite:///test.db"
    # engine = create_engine(connection_string, echo=False)
    engine = get_engine()
    db = SQLDatabase(engine)
    table_info = db.get_table_info()

    return table_info

if __name__=="__main__":
    ti = get_table_info()
    print(ti)