from sqlalchemy import Column, Integer, Text, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Logs(Base):
	"""
	This class defines the table schema of the log table.
	"""

	__tablename__ = "github_results"

	id = Column(Integer, primary_key=True, autoincrement = True)
	pdf_name = Column(String, nullable=False)  # original PDF filename
	company_name = Column(String, nullable=False)  # extracted from PDF
	timestamp = Column(DateTime)

	# Basicallt writing a seperate class for the GitHub members so that in the future, I can include as much data as I need about them
	members = relationship("GitHubMember", back_populates="log", cascade="all, delete-orphan")

class GitHubMember(Base):
	"""
	The defining properties of the members
	"""
	__tablename__ = "github_members"

	# The metadata I need and I am defining
	id = Column(Integer, primary_key=True)		# The main sort of id
	node_id = Column(Integer, nullable=False)	# another sort of id 
	login = Column(String, nullable=False)	# Some variant of a username accorind go the API
	# can add more here as and when needed

	log_id = Column(Integer, ForeignKey("github_results.id"))

	# Basically a primarykey foreign key thingie.
	log = relationship("Logs", back_populates="members")