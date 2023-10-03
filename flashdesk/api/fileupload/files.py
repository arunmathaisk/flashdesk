import os
import frappe
from werkzeug.wrappers import Request, Response
from werkzeug.utils import secure_filename
from pathlib import Path

ALLOWED_EXTENSIONS = {"tar", "zip"}

def is_allowed_extension(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@frappe.whitelist()
def file_upload():  
    # Get request data
    data = frappe.request.files.get("file")
    current_chunk = int(frappe.form_dict.get("current_chunk", 0))
    total_chunks = int(float(frappe.form_dict.get("total_chunks", 1)))
    file_name = frappe.form_dict.get("filename", "")

    # Define the save path
    save_path = os.path.join(frappe.get_site_path("private/files"), secure_filename(file_name))

    # Check if the file extension is allowed
    if not is_allowed_extension(file_name):
        return "File Not Allowed"

    # Check if the file already exists and it's the first chunk
    if os.path.exists(save_path) and current_chunk == 0:
        return "File Exists"

    try:
        # Open the file in binary append mode and write the data chunk
        with open(save_path, "ab") as f:
            f.seek(int(frappe.form_dict.get("offset", 0)))
            f.write(data.stream.read())
    except OSError:
        return "Issue in Saving file"

    if current_chunk + 1 == total_chunks:
        # This was the last chunk, check the file size
        expected_size = int(frappe.form_dict.get("dztotalfilesize", 0))
        actual_size = os.path.getsize(save_path)
        if actual_size != expected_size:
            print(f"File {file_name} has a size mismatch: {actual_size} != {expected_size}")
            return "Size Mismatch"
        else:
            print(f"File {file_name} has been uploaded successfully")
    else:
        print(f"Chunk {current_chunk + 1} of {total_chunks} for file {file_name} complete")

    reply_dict = {"status": "Chunk Uploaded Successfully", "filepath": save_path}
    return reply_dict
