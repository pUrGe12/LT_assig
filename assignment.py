import subprocess
from assignment.core import app

if __name__ == "__main__":
	subprocess.Popen(
		["huey_consumer", "assignment.core.tasks.huey"],
		stdout = subprocess.PIPE,		# Saving the logs but don't need to display them
		stderr=subprocess.PIPE
	)
	app.run()