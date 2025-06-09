import databases
import sqlalchemy
from sqlalchemy import Table, Column, String, Boolean, Integer
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

postgre_host=os.getenv("host")
postgre_user=os.getenv("user")
postgre_pass=os.getenv("pass")
postgre_port=os.getenv("port")
postgre_db=os.getenv("db")

DATABASE_URL = f"postgresql+psycopg://{postgre_user}:{postgre_pass}@{postgre_host}:{postgre_port}/{postgre_db}"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_admin", Boolean, default=False, nullable=False),
    Column("is_deleted", Boolean, default=False, nullable=False),  # new column
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)   # creates tables if missing