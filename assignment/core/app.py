from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid

from assignment.config import Config
from assignment.core.tasks import new_upload_task
from assignment.core.database.db import fetch_from_id

app = Flask(__name__, template_folder = Config.dirs.templates_dir, static_folder = Config.dirs.static_dir)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Keeping a 16 MB limit

ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename: str) -> bool:
    # Not the best way
    # TODO update this
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/api/documents/upload", methods=["POST"])
def upload_file():
    if "pdf" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["pdf"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        file_ext = os.path.splitext(filename)[1]
        save_filename = f"{unique_id}{file_ext}"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], save_filename)
        
        # Eventually, I might not have to save the pdf because it doesn't really matter, but i will keep this for now
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file.save(save_path)

        # Returning a uuid once the upload is finished
        new_upload_task(unique_id, save_path)             # huey task for processing in the backgroud using a huey consumer. (assuming I can spawn multiple processes on render)
        # We don't need its value here
        return jsonify({"id": unique_id}), 200

    return jsonify({"error": "Invalid file type"}), 400

@app.route("/<_id>")
def document_page(_id):
    result = fetch_from_id(_id)

    if result is None:
        abort(404)      # Here we can show the scan progress!

    return render_template("document.html", doc_id=_id, data=result)

def run():
    app.run(debug=True, host="0.0.0.0", port=5000)

# Can run directly as well
if __name__ == "__main__":
    run()