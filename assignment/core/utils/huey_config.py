from huey import SqliteHuey

from assignment.config import Config

huey = SqliteHuey(
    filename=Config.huey.broker_db,    # Alternatively can use immediate mode here if thats needed
)
