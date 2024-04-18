# -*- coding: utf-8 -*-
# Copyright (c) 2021, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint

class Approvals(Document):
	pass

def get_permission_query_conditions(user):
	if not user: user = frappe.session.user

	if "System Manager" in frappe.get_roles(user):
		return None
	else:
		return """(`tabApprovals`.owner = {user})"""\
			.format(user=frappe.db.escape(user))

def has_permission(doc, user):
	if "System Manager" in frappe.get_roles(user):
		return True
	else:
		return doc.owner==user

@frappe.whitelist()
def approve_record(document, document_name):
	doc = frappe.get_doc(document,document_name)
	if document == "Payment Request":
		doc.status = "Requested"
	elif document == "Timesheet":
		doc.status = "Submitted"	
	else:
		doc.status = "Approved"
#	doc.workflow_state = "Approved

	doc.docstatus = 1
	doc.run_method('submit')
	update_approval = frappe.db.sql("""update `tabApprovals` set status='Approved' where document_name='{0}'
					""".format(document_name))
	frappe.db.commit()
	
# 	delete_approval = frappe.db.sql("""delete `tabApprovals` where document='{0}' and document_name='{1}""".format(document,document_name), as_dict = True)	
	
	return 0

@frappe.whitelist()
def reject_record(document, document_name):
	doc = frappe.get_doc(document,document_name)
	doc.status = "Rejected"
	doc.workflow_state = "Rejected"
	doc.run_method('submit')
	update_approval = frappe.db.sql("""update `tabApprovals` set status='Rejected' where document_name='{0}'
					""".format(document_name))
	frappe.db.commit()
	return 0

