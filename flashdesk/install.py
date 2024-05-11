import frappe
import os
import json


def create_dirs():
	site_path = frappe.get_site_path("private/files")
	dir_names = ["tarfiles/uploaded", "tarfiles/saved", "pdffiles", "chromadb_new", "chromadb"]

	for folder in dir_names:
		full_path = os.path.join(site_path, folder)
		print(full_path)
		os.makedirs(full_path, exist_ok=True)


def add_cors_config():
	site_config_file = frappe.get_site_path("site_config.json")
	file_r = open(site_config_file)
	config = json.loads(file_r.read())
	config.update({"allow_cors": "*"})
	file_w = open(site_config_file, "w")
	file_w.write(json.dumps(config, indent=2))


def after_install():
	create_dirs()
	add_cors_config()
