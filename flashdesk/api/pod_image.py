import frappe
from werkzeug.wrappers import Response
from werkzeug.wsgi import wrap_file
from werkzeug.utils import secure_filename
from flashdesk.docker_utils.docker_low_level_client import *
from flashdesk.docker_utils.docker_client import *


@frappe.whitelist()
def get_all_published_pod_images():
    fields = [
	    "name",
        "image_name",
        "image_description",
        "image_file",
        "image_id",
        "tags",
        "created_by",
        "created_on",
        "modified_on",
        "is_active",
        "status",
    ]
    filters = {"status": "Published"}
    data = frappe.get_all("Pod Image", fields=fields, filters=filters)
    return data


@frappe.whitelist()
def get_all_available_pod_images():
    return get_all_filesystem_docker_images()

@frappe.whitelist()
def docker_hub_search(search_query):
    return docker_search(search_query)


@frappe.whitelist()
def docker_pull(image_name):
    result = docker_hub_pull(image_name) 
    if result == "error":
        frappe.throw("Docker Pull has failed.Please check logs for more info.")
    return result

@frappe.whitelist()
def delete_image_using_id(image_id):
    result = remove_image_using_id(image_id)
    if result == "error":
        frappe.throw("There was an error while deleting the Pod Image")
    return result

@frappe.whitelist()
def create_image_from_file():
    fields = ["image_file","image_name"]
    data = frappe.request.get_json()
    filters = {"name":data.get("pod_id")}
    file_name = frappe.get_all("Pod Image", fields=fields, filters=filters)
    result = tar_image_create(file_name[0].image_file,file_name[0].image_name)
    return result
