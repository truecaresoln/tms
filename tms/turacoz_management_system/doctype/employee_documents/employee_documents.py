# -*- coding: utf-8 -*-
# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EmployeeDocuments(Document):
	pass

def get_permission_query_conditions(user):
	status = "Approved"
	if not user: user = frappe.session.user

	if "System Manager" in frappe.get_roles(user) or "Salary Slip Uploader" in frappe.get_roles(user):
		return None
	else:
		return """(`tabEmployee Documents`.owner = {user} and `tabEmployee Documents`.status = 'Approved')"""\
			.format(user=frappe.db.escape(user))

def has_permission(doc, user):
	status = "Approved"
	if "System Manager" in frappe.get_roles(user) or "HR Manager" in frappe.get_roles(user):
		return True
	else:
		return doc.owner==user and doc.status=='Approved'