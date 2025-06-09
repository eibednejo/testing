import databases
import sqlalchemy
from sqlalchemy import Table, Column, String, Boolean, Integer
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

postgre_host = os.getenv("host")
postgre_user = os.getenv("user")
postgre_pass = os.getenv("pass")
postgre_port = os.getenv("port")
postgre_db = os.getenv("db")
db_url = os.getenv("db_url")

DATABASE_URL = db_url

# Create database instance but don't connect yet
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_admin", Boolean, default=False, nullable=False),
    Column("is_deleted", Boolean, default=False, nullable=False),
)

# Don't create engine/tables during import - do it lazily
_engine = None
_tables_created = False

def get_engine():
    global _engine
    if _engine is None:
        _engine = sqlalchemy.create_engine(DATABASE_URL)
    return _engine

async def ensure_tables():
    """Create tables if they don't exist - call this when app starts"""
    global _tables_created
    if not _tables_created:
        engine = get_engine()
        # metadata.create_all(engine)
        _tables_created = True

async def connect_db():
    """Connect to database and ensure tables exist"""
    if not database.is_connected:
        await database.connect()
        await ensure_tables()