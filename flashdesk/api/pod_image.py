import os
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
    try:
        data = frappe.request.get_json()
        pod_id = data.get("pod_id")
        if not pod_id:
            frappe.throw("pod_id is required")
        
        pod_image = frappe.get_all("Pod Image", fields=["image_file", "image_name"], filters={"name": pod_id})
        if not pod_image:
            frappe.throw(f"No Pod Image found for pod_id {pod_id}")

        image_file = pod_image[0].image_file
        image_name = pod_image[0].image_name

        frappe.enqueue(
            tar_image_create,
            filename=image_file,
            image_name=image_name,
            queue="default",  # one of short, default, long
            timeout=None,  # pass timeout manually
            now=False,  # if this is True, method is run directly (not in a worker)
            job_name= f"Loading Tar file to Runnable Image : {image_name}",  # specify a job name
            enqueue_after_commit=False,  # enqueue the job after the database commit is done at the end of the request
            at_front=False,  # put the job at the front of the queue
        )
        return {"status": "success", "message": "The image extraction process has started in the background. Please check Events for more informstion."}

    except Exception as e:
        frappe.throw(str(e))


@frappe.whitelist(allow_guest=True)
def create_file_from_image(image_name):
    try:
        tar_dir = frappe.get_site_path("private/files/tarfiles/")
        full_save_path = os.path.join(tar_dir,secure_filename(filename))
        check_file = os.path.isfile(full_save_path)
        if check_file:
            return {"status": "success", "message": "Tar File is already saved"}
        else:
            save_to_tar_file(name,full_save_path)
        return "hello"
    except Exception as e:
        frappe.throw(str(e))