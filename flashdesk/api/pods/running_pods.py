import frappe
from werkzeug.wrappers import Response
from werkzeug.wsgi import wrap_file
from werkzeug.utils import secure_filename
from flashdesk.docker_utils.docker_client import *
from flashdesk.docker_utils.docker_low_level_client import *

@frappe.whitelist()
def get_all_actively_running_pod_images():
        return get_all_actively_running_docker_images()
    
@frappe.whitelist()
def terminate_pod(container_id):
        return kill_container_using_container_id(container_id)
    
@frappe.whitelist()
def run_pod(image_id):
        return start_container_using_image_id(image_id)

@frappe.whitelist()
def get_all_terminated_pods():
        return get_terminated_containers()


@frappe.whitelist(allow_guest=True)
def commit_pod(container_id,container_params=None):
        return container_id
        # return save_container(container_id,container_params)
