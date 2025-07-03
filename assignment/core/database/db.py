from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from assignment.config import Config
from assignment.core.database.models import Logs, GitHubMember


def extract_github_members_list(response):
	return_list = []
	for member in response:
		login = member.get("login", "")
		id_ = int(member.get("id", ""))
		node_id = member.get("node_id", "")

		return_list.append(GitHubMember(login=login, id=id_, node_id=node_id))
	return return_list


def db_inputs(connection_type):
    """
    This simply returns the context for connection to the sqlite database
    Again, defined as a function to scale it later. Can add mysql and postgres here
    """
    context = Config.db.as_dict()
    return {
        "sqlite": "sqlite:///{name}".format(**context),
    }[connection_type]


def create_connection():
	"""
	a function to create connections to db with pessimistic approach. 
	Currently we only have sqlite, but we can expand if needed
	"""
	connection_args = {}

	if Config.db.engine.startswith("sqlite"):
		connection_args["check_same_thread"] = False

	db_engine = create_engine(
		db_inputs(Config.db.engine),
		connect_args=connection_args,
		pool_size=50,
		pool_pre_ping=True,
	)
	Session = sessionmaker(bind=db_engine)

	return Session()


def send_submit_query(session):
	"""
	This function is to make sure that our logs are added to the db
	It tries very hard
	"""
	try:
		for _ in range(1, 100):
			try:
				print("trying")
				session.commit()
				print("commited")
				return True
			except Exception as e:
				print(f"hitting: {e}")
				time.sleep(0.1)
	except Exception as e:		# bad news
		print(f"hitting this: {e}")
		return False
	return False



def insert_into_db_logs(id_, pdf_name, company_name, response):
	assert isinstance(response, list)	# Making sure that I always pass only a json.loads() output here

	github_members_list = extract_github_members_list(response)		# Ideally there should be a seperate file for helper fucntiosn but I guess its not too bad

	print("i am inside here")
	session = create_connection()
	session.add(
		Logs(
			id = id_,
			pdf_name = pdf_name,
			company_name = company_name,
			timestamp = datetime.utcnow(),	# The current timestamp as they mentioned
			members = github_members_list
		)
	)
	print("added")
	return send_submit_query(session)