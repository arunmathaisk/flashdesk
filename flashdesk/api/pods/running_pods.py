import frappe
from werkzeug.wrappers import Response
from werkzeug.wsgi import wrap_file
from werkzeug.utils import secure_filename
from flashdesk.docker_utils.docker_client import *

@frappe.whitelist()
def get_all_actively_running_pod_images():
        return get_all_actively_running_docker_images()
    


@frappe.whitelist()
def terminate_pod(container_id):
        return kill_container_using_container_id(container_id)
    