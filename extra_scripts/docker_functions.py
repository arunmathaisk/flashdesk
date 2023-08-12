import docker
# create a client 
client = docker.from_env()
DOCKER_EXISTS = False
# lets check if docker exits on the server this is kinda dumb but yeah
def check_if_docker_exists():
    if bool(client.version()):
        DOCKER_EXISTS = True
        return DOCKER_EXISTS
    else:
        return DOCKER_EXISTS

# start a containter off an image
# a lot of docs says name but i find name of the image a bit risky for
# surround all of this code with try and catch block
# for images name for conatiner id
def start_container(image_id):
    built_images = client.images.list(all=True)
    for image in built_images:
        if image_id == image.id.split(":")[1] or image_id == image.short_id.split(":")[1]:
            container = client.containers.run(image.attrs["RepoTags"][0],detach=True,ports={"5901": "5901", "6901": "6901"})
            print(container.short_id)
            return container.short_id
        else:
            print("error")

def delete_container(container_id):
    client.containers.get(container_id).kill()