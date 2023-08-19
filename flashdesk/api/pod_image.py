import frappe
from werkzeug.wrappers import Response
from werkzeug.wsgi import wrap_file
from werkzeug.utils import secure_filename
from flashdesk.docker_utils.docker_client import *

@frappe.whitelist()
def get_all_published_pod_images():
    fields = [
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
    return get_all_docker_images()


