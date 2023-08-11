import frappe
import os
from pathlib import Path
from werkzeug.wrappers import Response
from werkzeug.wsgi import wrap_file
from werkzeug.utils import secure_filename
import uuid
import hashlib
import json


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
