from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

## = 'postgresql://username:password@path:port/database_name'
DB_URL = 'postgresql://postgres:ismoil01@localhost:5432/QuizApplication'

# this engine is used for creating sessions:
engine = create_engine(DB_URL)

# this is the first and local session:
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# this one is used for creating PostgreSQL Tables Classes
Base = declarative_base()