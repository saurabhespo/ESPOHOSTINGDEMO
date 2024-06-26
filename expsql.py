import struct
from sqlalchemy import create_engine, event, text
from sqlalchemy.engine.url import URL
from azure import identity


SQL_COPT_SS_ACCESS_TOKEN = 1256  # Connection option for access tokens, as defined in msodbcsql.h
TOKEN_URL = "https://database.windows.net/"  # The token URL for any Azure SQL database

# Get the connection string from environment variable
connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:espo-ai-sqldb.database.windows.net,1433;Database=AzureSQL-ESPO-SQL;Encrypt=yes;TrustServerCertificate=no;Timeout=30"



# Create the engine
engine = create_engine(connection_string)

azure_credentials = identity.DefaultAzureCredential()

@event.listens_for(engine, "do_connect")
def provide_token(dialect, conn_rec, cargs, cparams):
    # remove the "Trusted_Connection" parameter that SQLAlchemy adds
    cargs[0] = cargs[0].replace(";Trusted_Connection=Yes", "")

    # create token credential
    raw_token = azure_credentials.get_token(TOKEN_URL).token.encode("utf-16-le")
    token_struct = struct.pack(f"<I{len(raw_token)}s", len(raw_token), raw_token)

    # apply it to keyword arguments
    cparams["attrs_before"] = {SQL_COPT_SS_ACCESS_TOKEN: token_struct}


# Define the function to get all persons
def get_all():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM CoursePublishTable"))
        for row in result:
            print(row)  # Do something with the data
            break
    return

# Example usage
if __name__ == "__main__":
    get_all()
