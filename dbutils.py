import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_community.utilities.sql_database import SQLDatabase

def get_db():

    connection_string = config.CONNECTION_STRING  # "sqlite:///test.db"
    engine = create_engine(connection_string, echo=False)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = Session()

    return db

def get_table_info():

    connection_string = config.CONNECTION_STRING  # "sqlite:///test.db"
    engine = create_engine(connection_string, echo=False)
    db = SQLDatabase(engine)
    table_info = db.get_table_info()

    return table_info

if __name__=="__main__":
    ti = get_table_info()
    print(ti)