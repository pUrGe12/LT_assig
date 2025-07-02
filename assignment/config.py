import inspect
import os
from pathlib import Path


base_dir = Path.cwd()
web_dir = base_dir / "assignment/web"

class Paths:
	database_file = base_dir / ".data/assignment.db"

class HueyPaths:
	broker_db = base_dir / ".data/broker.db"

class WebPaths:
	upload_html = web_dir / "templates/upload.html"
	base_html = web_dir / "templates/base.html"
	css_html = web_dir / "static/css/style.css"
	js_html = web_dir / "static/js/upload.js"

class WebDirs:
	static_dir = web_dir / "static"
	templates_dir = web_dir / "templates"

class ConfigBase:
	@classmethod
	def as_dict(cls):
		return {attr_name: getattr(cls, attr_name) for attr_name in cls()}

	def __init__(self) -> None:
		self.attributes = sorted(
			(
				attribute[0]
				for attribute in inspect.getmembers(self)
				if not attribute[0].startswith("_") and not inspect.ismethod(attribute[1])
			)
		)
		self.idx = 0

	def __iter__(self):
		yield from self.attributes

class Database(ConfigBase):
	"""
	Defining this through configbase because this allows us to scale this for mysql, postgresql etc.
	by just adding more parameters here.
	"""
	engine = "sqlite"
	name = base_dir / ".data/assignment.db"

class Config:
	web_path = WebPaths()
	dirs = WebDirs()
	huey = HueyPaths()
	db = Database()
	path = Paths()