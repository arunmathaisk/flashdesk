import frappe
import os

@frappe.whitelist()
def insert_image():
    data = frappe.request.get_json()
    doc = frappe.get_doc(
        {
            "doctype": "Pod Image",
            "image_name": data.get("image_name"),
            "image_description": data.get("image_description"),
            "image_file": os.path.basename(data.get("image_file")),
            "image_id": data.get("image_id"),
            "tags": data.get("tags"),
            "status": data.get("status"),
        }
    )
    doc.insert()
    return doc