import pandas as pd
import os
import pandas as pd
import sqlalchemy as sa
import json
import datetime as dt
from typing import Dict, Any, Tuple, List
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import sessionmaker, Session
from ..models.conversations_history import ConversationHistory
from ..config.settings import Settings


class DatabaseService:
    def __init__(self) -> None:
        self.settings = Settings()
        self.server = self.settings.SERVER
        self.database = self.settings.DATABASE
        self.database_user = self.settings.DATABASE_USER
        self.database_pass = self.settings.DATABASE_PASS
        self.db = self.__get_db__()

    def __get_db__(self) -> Session:
        engine = self.__create_engine__()
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        try:
            yield db
        finally:
            db.close()

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

    async def save_conversation(self, conversation_data: Dict) -> bool:
        try:
            # Salva no RDS
            db_record = ConversationHistory(
                user_name=conversation_data["username"],
                role=conversation_data["role"],
                message=conversation_data["message"],
                created_at=dt.datetime.now(),
            )
            self.db.add(db_record)
            self.db.commit()

            print("Saved conversations!")

            return True

        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False

    async def get_conversations(self, username: str, limit: int = 10) -> List[Dict]:
        try:
            conversations = (
                self.db.query(ConversationHistory)
                .filter_by(user_id=username)
                .order_by(ConversationHistory.created_at.desc())
                .limit(limit)
                .all()
            )

            print("Got conversations: ")
            print(conversations)
            return [
                {
                    "username": conv.user_id,
                    "message": conv.message,
                    "tokens_used": conv.tokens_used,
                    "created_at": conv.created_at.isoformat(),
                }
                for conv in conversations
            ]
        except Exception as e:
            print(f"Error getting conversations: {e}")
            return []
