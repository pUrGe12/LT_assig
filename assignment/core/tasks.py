import pdfplumber
from assignment.core.utils.huey_config import huey
from assignment.core.github_api import get_open_members
from assignment.core.database.db import insert_into_db_logs
from assignment.core.gemini.parser import parse


@huey.task(retries=3, retry_delay=2)
def new_upload_task(save_file):
	with pdfplumber.open(save_file) as pdf:
		extracted_text = ""
		pages = pdf.pages
		for page in pages:
			extracted_text += page.extract_text() + "\n"

	companies_list = []

	output_json = parse(extracted_text)
	for _ in range(0, int(output_json.get("num_companies", 1))):
		companies_list.append(output_json.get("github_username_{}".format(_+1)))

	for company in companies_list:
		response = get_open_members(company)
		if response:
			insert_into_db_logs(pdf_name=save_file, company_name=company, response=response)
		else: # hard luck
			return None

	return None