import frappe


@frappe.whitelist()
def get_logged_in_user_details():
	user = frappe.get_doc("User", frappe.session.user)
	user_details = {
		"full_name": user.full_name,
		"email": user.email,
		"username": user.username,
		"roles": [role.role for role in user.get("roles")],
	}
	return user_details


@frappe.whitelist()
def get_last_login():
	last_login = frappe.get_value("User", frappe.session.user, "last_login")
	return last_login
