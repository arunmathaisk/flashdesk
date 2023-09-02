import frappe
import os
from werkzeug.wrappers import Request, Response
from werkzeug.utils import secure_filename
from pathlib import Path
import bleach
import json

@frappe.whitelist()
def insert_image():
	if frappe.request.method == "POST":
		data = frappe.request.get_json()
		print(data)
		doc = frappe.get_doc({
			"doctype": "Pod Image",
			"image_name":bleach.clean(data["image_name"]),
			"image_description":bleach.clean(data["image_description"]),
			"image_file":data["image_file"],
			"image_id":bleach.clean(data["image_id"]),
			"tags":bleach.clean(data["tags"]),
			"status":data["status"]
		})
		print(doc.insert())
		return doc