import frappe
from frappe.model.document import Document

class PodImage(Document):
    def before_insert(self):
        # Populate "Created On" field with the current timestamp
        self.created_on = frappe.utils.now()
        # Populate "Created By" field with the current user's ID
        self.created_by = frappe.session.user
