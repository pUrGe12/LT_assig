import os
from pathlib import Path


base_dir = Path.cwd()
web_dir = base_dir / "web"

class WebPaths:
	upload_html = web_dir / "templates/upload.html"
	base_html = web_dir / "templates/base.html"
	css_html = web_dir / "static/css/style.css"
	js_html = web_dir / "static/js/upload.js"

class WebDirs:
	static_dir = web_dir / "static"
	templates_dir = web_dir / "templates"

class Config:
	path = WebPaths()
	dirs = WebDirs()