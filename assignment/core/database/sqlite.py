# This is where the initial database creation will take place. Running this with assignment.py
from sqlalchemy import create_engine

from assignment.config import Config
from assignment.core.database.models import Base

def sqlite_create_tables():
    """
	This function is supposed to run whenever we run the code for the first time 
    """
    db_engine = create_engine(
        "sqlite:///{name}".format(**Config.db.as_dict()),
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(db_engine)
