import subprocess
from assignment.core import app
from assignment.config import Config
from assignment.core.database.sqlite import sqlite_create_tables

if __name__ == "__main__":
	subprocess.Popen(
		["huey_consumer", "assignment.core.tasks.huey"],
		# stdout = subprocess.PIPE,		# Saving the logs but don't need to display them
		# stderr=subprocess.PIPE
	)

	if not Config.path.database_file.exists():
		sqlite_create_tables()
		
	app.run()