import pandas as pd
import os
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

## Same dabatase methods used in the database_service.py file for the chatbot
def create_engine():
    server = os.getenv("db_endpoint")
    database = os.getenv("database")
    username = os.getenv("database_user")
    password = os.getenv("database_pass")

    connection_url = URL.create(
        "postgresql+psycopg2",
        username=username,
        password=password,
        host=server,
        database=database,
    )

    return sa.create_engine(connection_url)


def open_db_conn():
    return create_engine().connect()


def query_db(query: str) -> pd.DataFrame:
    with open_db_conn() as conn:
        try:
            df = pd.read_sql(query, conn)
        except Exception as e:
            print("Error fetching data. Error: ", e)
            return pd.DataFrame()

    return df

# Load the data and clean it keeping null values for the model to decide what to do with them
df = pd.read_csv("train.csv")
df = df[['REF_DATE', 'TARGET', 'VAR2', 'IDADE', 'VAR4', 'VAR5', 'VAR8']]
df = df.set_axis(['ref_date', 'target', 'sexo', 'idade','obito', 'uf', 'classe'], axis='columns')
df['ref_date'] = pd.to_datetime(df['ref_date'], format='%Y-%m-%d %H:%M:%S+00:00')

df.to_csv("train_cleaned.csv", index=False)

# df = pd.read_csv("train_cleaned.csv")

# Insert the data into the database
try:
    conn = open_db_conn()
    conn.autocommit = True
    
    df.to_sql('credit_sc', con=conn, if_exists='replace', 
            index=False) 

    conn.commit() 
    conn.close() 
except Exception as e:
    print("Failed to insert data into database. Error: ", e)
else:
    print("Data inserted successfully")