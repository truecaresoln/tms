# -*- coding: utf-8 -*-
# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from tms.utils.approvals import insert_approvals

class EmployeeSalarySlip(Document):
	def validate(self):
		self.update_approval()
	
	def update_approval(self):
		document = "Employee Salary Slip"
		approver = frappe.db.sql("""select thr.parent,usr.full_name from `tabHas Role` thr 
				left join `tabUser` usr on thr.parent=usr.name
				where `role` ='Salary Slip Approver' limit 1""",as_dict = True)
		reporting_manager_id = approver[0]['parent']
		full_name = approver[0]['full_name']
		insert_approvals(document,self.name,reporting_manager_id,full_name,self.salary_slip_to,self.employee_name,self.workflow_state)	

def get_permission_query_conditions(user):
	status = "Approved"
	if not user: user = frappe.session.user

	if "System Manager" in frappe.get_roles(user) or "Salary Slip Uploader" in frappe.get_roles(user):
		return None
	else:
		return """(`tabEmployee Salary Slip`.salary_slip_to = {user} and `tabEmployee Salary Slip`.status = 'Approved')"""\
			.format(user=frappe.db.escape(user))

def has_permission(doc, user):
	status = "Approved"
	if "System Manager" in frappe.get_roles(user) or "Salary Slip Uploader" in frappe.get_roles(user):
		return True
	else:
		return doc.salary_slip_to==user and doc.status=='Approved'
