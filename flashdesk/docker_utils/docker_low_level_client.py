import os
import json
import docker
import json

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
