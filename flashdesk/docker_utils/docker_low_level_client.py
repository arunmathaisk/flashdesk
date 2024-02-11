import os
import json
import docker
import json
import frappe
from frappe import _dict

ll_client = docker.APIClient()

def tar_image_create(filename, image_name):
    try:
        tar_file = os.path.join(filename)
        image_name = image_name.replace(' ', '').lower()
        if not os.path.isfile(tar_file):
            print("File does not exist:", tar_file)
        result = ll_client.import_image_from_file(tar_file, repository=image_name)
    except Exception as e:
        print("Exception occurred:", str(e))


def save_container(container_id, container_params):
    try:
        # Assuming container_params['image_name'] holds the repository name
        image_name = container_params['image_name']
        tag = container_params['tag']
        message = container_params['message']
        pause = container_params.get('pause', True)  # Correcting comment to match default value

        # Combine repository name and tag
        repository_tag = f"{image_name}:{tag}"

        # Pass the combined repository and tag to the commit method
        result = ll_client.commit(container=container_id, repository=repository_tag, message=message, pause=pause)
        print(result)
    except Exception as e:
        frappe.throw(f"Failed to commit Container {container_id}: {e}")
