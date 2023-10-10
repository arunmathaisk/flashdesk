import docker
import frappe
import os 
import json


ll_client = docker.APIClient()

def tar_image_create(filename,image_name):
    tar_file = os.path.join(frappe.get_site_path("private/files"),filename)
    image_name = image_name.replace(' ','')
    image_name = image_name.lower()
    if os.path.isfile(tar_file):
        create = ll_client.import_image_from_file(tar_file,repository=image_name)
        result_json = json.loads(create)
        if result_json["status"]:
            reply_dict = {"type":"success","title":"Image ready","body":"Go to Active Pod Images"}
            return reply_dict