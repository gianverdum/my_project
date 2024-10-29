# src/database.py
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Supabase PostgreSQL connection URL
DATABASE_URL = "postgres://postgres.overbatiwykqflqyuqat:09tywYLvBRcgmkG6@\
    aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode\
        =require&supa=base-pooler.x"

# Update the database engine to use the Supabase PostgreSQL URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
