import docker
import json
from datetime import datetime

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
    print(container.short_id)
    return container.short_id


def delete_container_using_container_id(container_id):
    client.containers.get(container_id).kill()

def get_all_docker_images():
    try:
        images = client.images.list()
        image_list = []
        for image in images:
            print(image)
            image_info = {
                "Image ID": image.id,
                "Tags": image.tags,
                "Created": image.attrs["Created"],
                "Size": image.attrs["Size"],
            }
            image_list.append(image_info)
        return image_list
    except docker.errors.APIError as e:
        print("Error:", e)
        return []
