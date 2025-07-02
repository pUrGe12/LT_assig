import pdfplumber
from assignment.core.utils.huey_config import huey

@huey.task(retries=3, retry_delay=2)
def new_upload_task(save_file):

	company = ""
	# As seen in https://github.com/jsvine/pdfplumber/README.md
	with pdfplumber.open(save_file) as pdf:
		first_page = pdf.pages[0]
		for i in first_page.chars:
			company += i.get("text", "").strip()	# case sensitivity doesn't matter

	print(f"This is the company name: {company}")
	return company
	# This is where the processing logic should be