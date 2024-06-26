from sqlalchemy import create_engine
from azure.identity import DefaultAzureCredential
import os
import dbutils
from sqlalchemy.orm import sessionmaker
from langchain_community.utilities.sql_database import SQLDatabase
import os
import pyodbc, struct
from azure.identity import DefaultAzureCredential



#CONNECTION_STRING = f"mssql+pyodbc:///?odbc_connect={SQL_STRING}"
connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:espo-ai-sqldb.database.windows.net,1433;Database=AzureSQL-ESPO-SQL;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"

# def get_all():
#     with get_conn() as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM Persons")
#         # Do something with the data
#     return

def get_conn():
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn

conn = get_conn()
cur = conn.cursor()
cur.execute("select * from CoursePublishTable ")
print(cur.fetchone())

def create_pyodbc_engine():
    pyodbc_conn = get_conn()

    def creator():
        return pyodbc_conn
    
    engine = create_engine("mssql+pyodbc://", creator=creator)

    return engine


# CONNECTION_STRING = f"mssql+pyodbc:///?odbc_connect={conn}"
# engine = create_engine(CONNECTION_STRING, echo=False)
# # Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# # db = Session()
engine = create_pyodbc_engine()
db = SQLDatabase(engine)
table_info = db.get_table_info()
print(table_info)