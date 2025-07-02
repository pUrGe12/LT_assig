from huey import SqliteHuey

from assignment.config import Config

print(f"This is {Config.huey.broker_db}")
huey = SqliteHuey(
    filename=Config.huey.broker_db,    # Alternatively can use immediate mode here if thats needed
)
