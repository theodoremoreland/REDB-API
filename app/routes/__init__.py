# Third party
import sqlalchemy
import databases

# Custom
from app.config import DATABASE_URL # DB connection information in local gitignored file
from app.models.models import *

print(f"_________________________________________________________________{DATABASE_URL}__________________________________________")


database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})