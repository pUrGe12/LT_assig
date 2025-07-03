import pdfplumber
from assignment.core.utils.huey_config import huey
from assignment.core.github_api import get_open_members
from assignment.core.database.db import insert_into_db_logs
from assignment.core.gemini.parser import parse


@huey.task(retries=3, retry_delay=2)
def new_upload_task(save_file):
	# This is to be done using gemini
	with pdfplumber.open(save_file) as pdf:
		extracted_text = ""
		pages = pdf.pages
		for page in pages:
			extracted_text += page.extract_text() + "\n"

	companies_list = []

	output_json = parse(extracted_text)
	for _ in range(0, int(output_json.get("num_companies", 1))):
		companies_list.append(output_json.get("github_username_{}".format(_+1)))

	print("This is the companies_list: {companies_list}")
	for company in companies_list:
		response = get_open_members(company)
		if response:
			print(f"I am getting this response: {response}")
			# Add it to database here
			# Note that the response is the raw json of multiple guys. The parsing needs to be done inside the addition function itself
			insert_into_db_logs(pdf_name=save_file, company_name=company, response=response)
		else: # hard luck
			return None

	return None
	# This is where the processing logic should be