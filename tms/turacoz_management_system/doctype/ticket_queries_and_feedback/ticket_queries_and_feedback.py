# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class TicketQueriesandFeedback(Document):
	pass

def get_permission_query_conditions(user):
	if not user: user = frappe.session.user

	if "System Manager" in frappe.get_roles(user):
		return None
	else:
		return """(`tabTicket Queries and Feedback`.owner = {user} or `tabTicket Queries and Feedback`.troubleshooter = {user})"""\
			.format(user=frappe.db.escape(user))

def has_permission(doc, user):
	if "System Manager" in frappe.get_roles(user):
		return True
	else:
		return doc.owner==user or doc.troubleshooter==user
