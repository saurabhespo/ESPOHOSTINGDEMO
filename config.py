import os
import urllib
from pathlib import Path

path = Path(__file__).parent

##llmconfig
AZURE_OPENAI_API_KEY = "36542e1630604f028ee1f9a06b12b5c1"
AZURE_OPENAI_ENDPOINT = "https://espo-ai-01.openai.azure.com/"

OPENAI_API_VERSION = "2024-02-15-preview"
AZURE_DEPLOYMENT = "gpt-4"

##dbconfig
# CONNECTION_STRING = "sqlite:///test.db"

# SERVER = "tcp:espo-ai-sqldb.database.windows.net,1433"
# DATABASE = "AzureSQL-ESPO-SQL"
# USERNAME = "CloudSAb19cb3dc"
# PASSWORD = "Espoai@12auth"
# SQL_STRING = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD} ;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

# CONNECTION_STRING = f"mssql+pyodbc:///?odbc_connect={SQL_STRING}"

##
#params = urllib.parse.quote_plus(r"""Driver={ODBC Driver 18 for SQL Server};Server=tcp:espo-ai-sqldb.database.windows.net,1433;Database=AzureSQL-ESPO-SQL;Uid=CloudSAb19cb3dc;Pwd=Espoai@12auth;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;""")
servername="LAPTOP-SDO1R816\MSSQLSERVER01";
dbname="testdata";
engine = 'mssql+pyodbc://@' + servername + '/' + dbname + '?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'

CONNECTION_STRING  =engine #'mssql+pyodbc:///?odbc_connect={}'.format(params)

#'ODBC Driver 17 for SQL Server'

##Prompt
PROMPT_FILE = f"{path}\\prompts.yml"
HISTORY_FILE = f"{path}\\history.yml"
