# Third party
import sqlalchemy
import databases

# Custom
from app.config import DATABASE_URL
from app.models.models import *

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})