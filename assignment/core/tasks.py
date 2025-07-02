import pdfplumber
from assignment.core.utils.huey_config import huey
from assignment.core.github_api import get_open_members

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
	print(f"I am getting this response: {response}")
	return response
	# This is where the processing logic should be