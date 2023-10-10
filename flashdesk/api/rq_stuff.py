import frappe
    
@frappe.whitelist()
def get_new_completed_queues():

    last_fetch_timestamp = frappe.cache().get_value("last_fetch_timestamp")

    # Use a default timestamp if it's not found in the cache
    if not last_fetch_timestamp:
        last_fetch_timestamp = "2000-01-01 00:00:00"

     # Fetch completed RQ Jobs that were either created or modified after last_fetch_timestamp
    completed_jobs = frappe.get_all(
        "RQ Job",
        fields=["name", "status", "queue", "method", "creation", "runtime"]
    )

    # Compute virtual values for each document
    computed_completed_jobs = []
    for job in completed_jobs:
        doc = frappe.get_doc("RQ Job", job.get("name"))
        valid_dict = doc.get_valid_dict()
        computed_completed_jobs.append(valid_dict)

    new_fetch_timestamp  = frappe.utils.now_datetime()
    frappe.cache().set_value("last_fetch_timestamp",new_fetch_timestamp)

    # Return the results along with metadata
    result = {
        "last_fetch_timestamp" : last_fetch_timestamp,
        "new_fetch_timestamp" : new_fetch_timestamp,
        "completed_jobs": completed_jobs,
    }

    frappe.publish_realtime('global_admin_notifications',{'data':result})


@frappe.whitelist()
def get_new_completed_queues2():

    last_fetch_timestamp = frappe.cache().get_value("last_fetch_timestamp")

    # Use a default timestamp if it's not found in the cache
    if not last_fetch_timestamp:
        last_fetch_timestamp = "2000-01-01 00:00:00"

     # Fetch completed RQ Jobs that were either created or modified after last_fetch_timestamp
    completed_jobs = frappe.get_all(
        "RQ Job",
        fields=["name", "status", "queue", "method", "creation", "runtime"]
    )

    new_fetch_timestamp  = frappe.utils.now_datetime()
    frappe.cache().set_value("last_fetch_timestamp",new_fetch_timestamp)

    # Return the results along with metadata
    result = {
        "last_fetch_timestamp" : last_fetch_timestamp,
        "new_fetch_timestamp" : new_fetch_timestamp,
        "completed_jobs": completed_jobs,
    }

    return result
