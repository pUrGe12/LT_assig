import requests
import json

def get_open_members(company_name):
	'''
	This is supposed to take the company name, hit the github restapi, and return the list of open sourced members
	'''
	API_URL = "https://api.github.com/orgs/{}".format(company_name)
	response = json.loads(requests.get(API_URL).text)
	public_members_url = response.get("public_members_url", "")

	if public_members_url:
		PM_API_URL = public_members_url.split("{")[0]	# Assuming the URL doesn't have { anywhere else otherwise things may get awkward
		response = json.loads(requests.get(PM_API_URL).text)

		for member in response:
			print(member)
	
	else:
		reponse = ""			# hard luck

	return response