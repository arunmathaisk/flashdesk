import frappe
import os
from werkzeug.wrappers import Request, Response
from werkzeug.utils import secure_filename
from pathlib import Path
import json

allowed_extension = ["tar"]
@frappe.whitelist()
def file_upload():
    if frappe.request.method == "POST":
        print(frappe.form_dict)
        data = frappe.request.files["file"]
        current_chunk = int(frappe.form_dict["current_chunk"])
        total_chunks = frappe.form_dict["total_chunks"]
        file_name = frappe.form_dict["filename"]
        save_path = os.path.join(frappe.get_site_path("private/files"), secure_filename(file_name))
        
        extension = file_name.split(".")[1]
        if extension not in allowed_extension:
            return "File Not Allowed"
        if os.path.exists(save_path) and current_chunk == 0:
        # 400 and 500s will tell dropzone that an error occurred and show an error
            return "File Exists"
        
        try:
            with open(save_path,"ab") as f:
                f.seek(int(frappe.form_dict['offset']))
                f.write(data.stream.read())
        except OSError:
            return "issue in Saving file"

        if current_chunk + 1 == total_chunks:
        # This was the last chunk, the file should be complete and the size we expect
            if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
                print(f"File {file_name} was completed, "
                        f"but has a size mismatch."
                        f"Was {os.path.getsize(save_path)} but we"
                        f" expected {request.form['dztotalfilesize']} ")
                return "Size Mismatch"
            else:
                print(f'File {file_name} has been uploaded successfully')
        else:
            print(f'Chunk {current_chunk + 1} of {total_chunks} '
                    f'for file {file_name} complete')

    reply_dict = {
        "status":"Chunk Uploaded Successfully",
        "filepath":save_path
    }
    return reply_dict
        


        # print("current chunk "+str(current_chunk)+" "+str(file_name))
        # return "current chunk "+str(current_chunk)+" "+str(file_name)



        
    