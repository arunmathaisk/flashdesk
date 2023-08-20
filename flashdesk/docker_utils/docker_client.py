import docker
import json
from datetime import datetime
import humanize
# import frappe

client = docker.from_env()

DOCKER_EXISTS = False


def check_if_docker_exists():
    global DOCKER_EXISTS
    if bool(client.version()):
        DOCKER_EXISTS = True
        return DOCKER_EXISTS
    else:
        return DOCKER_EXISTS


def start_container_using_image_id(image_id):
    container = client.containers.run(
        image=image_id, detach=True, ports={"5901": "5901", "6901": "6901"}
    )
    return container.short_id

def kill_container_using_container_id(container_id):
    client.containers.get(container_id).kill()


def get_all_filesystem_docker_images():
    try:
        images = client.images.list()
        image_list = []
        for image in images:
            image_info = {
                "image_id": image.id,
                "short_id": image.short_id,
                "labels": image.labels,
                "tags": image.tags,
                "created": image.attrs["Created"],
                "size": humanize.naturalsize(image.attrs["Size"]),
                "architecture": image.attrs["Architecture"],
                "os": image.attrs["Os"],
            }
            image_list.append(image_info)
        return image_list
    except docker.errors.APIError as e:
        print("Error:", e)
        return []


def get_all_actively_running_docker_images():
    try:
        containers = client.containers.list()
        running_containers = []
        for container in containers:
            running_container = {
                "container_id": container.id,
                "container_image_tags" :container.image.tags,
                "container_name": container.name,
                "container_labels": container.labels,
                "container_shortid": container.short_id,
                "container_status": container.status,
            }
            running_containers.append(running_container)
        return running_containers
    except docker.errors.APIError as e:
        print("Error:", e)
        return []

def docker_search(query):
    try:
        search_results = client.images.search(query)
        return search_results
    except docker.errors.DockerException as e:
        print("Error:", e)
        return []


# @frappe.whitelist()
# def pull_container_from_hub(container_id):
#     resp = client.api.pull(container_id, stream=True, decode=True, all_tags=True)
#     for line in resp:
#         frappe.publish_realtime("event_name", data={"key": "value"})
#     return "done"
