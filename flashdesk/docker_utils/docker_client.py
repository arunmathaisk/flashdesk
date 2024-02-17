import docker
import socket
import json
from datetime import datetime
import humanize

import frappe
from frappe import _dict

client = docker.from_env()

DOCKER_EXISTS = False


def find_available_ports(num_ports, starting_port=49152, ending_port=65535):
    reserved_ports = [22, 80, 443, 3306]  # List of reserved ports

    available_ports = []
    current_port = starting_port

    while len(available_ports) < num_ports and current_port <= ending_port:
        if current_port not in reserved_ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("0.0.0.0", current_port))
                    available_ports.append(current_port)
                except:
                    pass
        current_port += 1

    return available_ports


def check_if_docker_exists():
    global DOCKER_EXISTS
    if bool(client.version()):
        DOCKER_EXISTS = True
        return DOCKER_EXISTS
    else:
        return DOCKER_EXISTS


def start_container_using_image_id(image_id):
    container_metadata = frappe.get_doc({
        "doctype": "Container Metadata",
        "container_id": "",
        "container_short_id": "",
        "image_id": "",
        "available_ports": "",
        "vnc_port": 6969696969,  # Default value in case available_ports has no element
        "port_bindings": "",
        "container_image_tags": "",
        "container_labels": "", 
    })

    exposed_ports = {"6080/tcp": {}, "56780/tcp": {}}
    num_exposed_ports = len(exposed_ports)
    available_ports = find_available_ports(num_exposed_ports)
    port_bindings = {}

    # Iterate through exposed ports and assign them to available ports
    for index, (exposed_port, _) in enumerate(exposed_ports.items()):
        if index < len(available_ports):
            port_bindings[exposed_port] = available_ports[index]

    # Start the container with port bindings
    container = client.containers.run(
        image=image_id,
        detach=True,
        ports=port_bindings,
    )

    # Set the values in the document
    container_metadata.container_id = container.id
    container_metadata.container_short_id = container.short_id
    container_metadata.image_id = image_id
    container_metadata.available_ports = ",".join(map(str, available_ports))
    container_metadata.vnc_port = available_ports[0] if len(available_ports) > 1 else 6969696969
    container_metadata.port_bindings = str(port_bindings)
    container_metadata.container_image_tags = str(container.image.tags)
    container_metadata.container_labels = str(container.labels)

    # Save the document
    container_metadata.insert()

    return container_metadata


def get_terminated_containers():
    terminated_containers = frappe.get_all(
        "Container Metadata",
        filters={"terminated_timestamp": ["!=", None]},
        fields=["name", "container_id", "container_short_id", "image_id", "container_image_tags", "available_ports", "vnc_port", "port_bindings", "timestamp", "container_labels", "terminated_timestamp"],
    )
    return terminated_containers


def kill_container_using_container_id(container_id):
    container_doc = frappe.get_doc("Container Metadata", {"container_id": container_id})
    if container_doc:
        try:
            client.containers.get(container_id).kill()
        except Exception as e:
            frappe.log_error(f"Error killing container {container_id}: {e}")
        else:
            container_doc.terminated_timestamp = datetime.now()
            container_doc.save()
    else:
        frappe.throw(f"Container with ID {container_id} not found.")


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
            fields = ["image_id","available_ports","vnc_port","port_bindings"]
            filters = {"container_id":container.id}
            result = frappe.db.get_value('Container Metadata',filters,fields,as_dict=True )
            print(container)
            running_container = {
                "container_id": container.id,
                "container_image_tags": container.image.tags,
                "container_name": container.name,
                "container_labels": container.labels,
                "container_shortid": container.short_id,
                "container_status": container.status,
                "container_image_id" : result.image_id,
                "container_available_ports" : result.available_ports,
                "container_vnc_port" : result.vnc_port,
                "container_port_bindings" : result.port_bindings,
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


def remove_image_using_id(image_id):
    try:
        client.images.remove(image_id, force=True)
        return "sucess"
    except docker.errors.ImageNotFound:
        print(f"Image {image_id} not found")
        return "error"
    except docker.errors.APIError as e:
        print(f"An error occurred: {e}")
        return "error"


def fetch_images(image_name):
    images = client.images.pull(image_name, all_tags=True)


def docker_hub_pull(image_name):
    try:
        frappe.enqueue(
            fetch_images,
            image_name=image_name,
            queue="default",  # one of short, default, long
            timeout=None,  # pass timeout manually
            now=False,  # if this is True, method is run directly (not in a worker)
            job_name=None,  # specify a job name
            enqueue_after_commit=False,  # enqueue the job after the database commit is done at the end of the request
            at_front=False,  # put the job at the front of the queue
        )
        return "sucess"
    except docker.errors.ImageNotFound:
        print(f"Docker Hub Pull failed {image_name}")
        return "error"
    except docker.errors.APIError as e:
        print(f"An error occurred: {e}")
        return "error"


def docker_events():
    events = client.events(decode=True)
    for event in events:
        print(event)
        # frappe.publish_realtime('docker_events', data={'event': event})


def save_to_tar_file(image_id,file_path):
    saved_image = client.images.get(image_id)
    f = open(file_path, 'wb')
    for chunk in saved_image.save():
        f.write(chunk)
    f.close()

def get_image_name_from_id(image_id):
    return client.images.get(image_id).attrs['RepoTags'][0]