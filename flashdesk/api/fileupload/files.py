import os
import frappe
from werkzeug.wrappers import Request, Response
from werkzeug.utils import secure_filename
from pathlib import Path
import math

ALLOWED_EXTENSIONS = {"tar", "zip","pdf"}

def is_allowed_extension(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_extension(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() 

@frappe.whitelist()
def file_upload():  
    # Get request data
    data = frappe.request.files.get("file")
    current_chunk = int(frappe.form_dict.get("current_chunk", 0))
    total_chunks = math.ceil(float(frappe.form_dict.get("total_chunks", 1)))
    file_name = frappe.form_dict.get("filename", "")


    upload_dir = frappe.get_site_path("private/files/tarfiles/uploaded") 

    if get_extension(file_name) == "pdf":
        upload_dir = frappe.get_site_path("private/files/pdffiles")
    
    # Define the save path
    save_path = os.path.join(upload_dir, secure_filename(file_name))



    # Check if the file extension is allowed
    if not is_allowed_extension(file_name):
        reply_dict = {"type": "warning", "title":"File Not Allowed","body":"Check file type"}
        return reply_dict

    # Check if the file already exists and it's the first chunk
    if os.path.exists(save_path) and current_chunk == 0:
        reply_dict = {"type": "warning", "title":"File Exists","body":"We have it already"}
        return reply_dict

    
    try:
        # Open the file in binary append mode and write the data chunk
        with open(save_path, "ab") as f:
            f.seek(int(frappe.form_dict.get("offset", 0)))
            f.write(data.stream.read())
    except OSError:   
        reply_dict = {"type": "warning", "title":"Issue in Saving file","body":"Please reupload"}
        return reply_dict

    if current_chunk + 1 == total_chunks:
        # This was the last chunk, check the file size
        expected_size = int(frappe.form_dict.get("filesize"))
        actual_size = os.path.getsize(save_path)
        if actual_size != expected_size:
            reply_dict = {"type": "warning", "title":"Size Mismatch","body":"Please reupload"}
            return reply_dict
        else:
           reply_dict = {"type": "success", "success":"File Uploaded","body":"Yay!","filepath": save_path}
           return reply_dict
    else:
        print(f"Chunk {current_chunk + 1} of {total_chunks} for file {file_name} complete")

    reply_dict = {"status": "Chunk Uploaded Successfully"}
    return reply_dict


@frappe.whitelist()
def file_delete():
    data = frappe.request.get_json()
    file_dir=frappe.get_site_path("private/files/tarfiles")
    if frappe.request.headers.get('Referer').split("/")[-1] == "UploadPDFS":
        file_dir=frappe.get_site_path("private/files/pdffiles")
    file_path = os.path.join(file_dir,data['name'])
    if os.path.isfile(file_path):
        os.unlink(file_path)
        return "deleted"


@frappe.whitelist()
def list_all_pdf_files():
    return os.listdir(frappe.get_site_path("private/files/pdffiles"))