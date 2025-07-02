import pdfplumber
from assignment.core.utils.huey_config import huey
from assignment.core.github_api import get_open_members
from assignment.core.database.db import insert_into_db_logs

@huey.task(retries=3, retry_delay=2)
def new_upload_task(save_file):

	company = ""
	# As seen in https://github.com/jsvine/pdfplumber/README.md
	with pdfplumber.open(save_file) as pdf:
		first_page = pdf.pages[0]
		for i in first_page.chars:
			company += i.get("text", "").strip()	# case sensitivity doesn't matter

	print(f"This is the company name: {company}")

	response = get_open_members(company)

	if response:
		print(f"I am getting this response: {response}")
		# Add it to database here
		# Note that the response is the raw json of multiple guys. The parsing needs to be done inside the addition function itself
		insert_into_db_logs(response)
	else: # hard luck
		return None
	
	return response
	# This is where the processing logic should be