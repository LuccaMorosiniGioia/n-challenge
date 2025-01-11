import pandas as pd
import os
import pandas as pd
import sqlalchemy as sa
import json
import datetime as dt
from typing import Dict, Any, Tuple, List
from sqlalchemy.engine import URL, Engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from ..models.conversations_history import ConversationHistory
from ..config.settings import Settings


class DatabaseService:
    def __init__(self) -> None:
        self.settings = Settings()
        self.server = self.settings.SERVER
        self.database = self.settings.DATABASE
        self.database_user = self.settings.DATABASE_USER
        self.database_pass = self.settings.DATABASE_PASS

    def __create_engine__(self) -> Engine:
        connection_url = URL.create(
            "postgresql+psycopg2",
            username=self.database_user,
            password=self.database_pass,
            host=self.server,
            database=self.database,
        )

        return sa.create_engine(
            connection_url, pool_pre_ping=True, pool_size=10, max_overflow=20
        )

    def __open_db_conn__(self) -> None:
        return self.__create_engine__().connect()

    def query_db(self, query: str) -> pd.DataFrame:
        with self.__open_db_conn__() as conn:
            try:
                df = pd.read_sql(query, conn)
            except Exception as e:
                print("Error fetching data. Error: ", e)
                return pd.DataFrame()

        return df

    def save_conversation(self, messages: Dict) -> bool:
        try:
            with self.__open_db_conn__() as conn:
                for msg in messages:
                    statement = text(
                        f"""INSERT INTO conv_history(user_name, role, message, created_at) VALUES(:username, :role, :message, '{dt.datetime.now()}')"""
                    )
                    conn.execute(statement, msg)
                conn.commit()
            return True

        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False

    def get_conversations(self, username: str, limit: int = 5) -> list:
        try:
            with self.__open_db_conn__() as conn:
                query = f"""SELECT role as role, message as content FROM conv_history WHERE user_name = '{username}' ORDER BY created_at DESC LIMIT {limit}"""
                df = pd.read_sql(query, conn)

            return df.to_dict(orient="records")[::-1]

        except Exception as e:
            print(f"Error getting conversation: {e}")
            return pd.DataFrame()
