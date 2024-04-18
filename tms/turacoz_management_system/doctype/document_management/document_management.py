# -*- coding: utf-8 -*-
# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DocumentManagement(Document):
	pass

def get_permission_query_conditions(user):
	if not user: 
		user = frappe.session.user
	if user!='Administrator':
		dept = frappe.db.sql("""select department from `tabEmployee` where user_id='{0}';""".format(user), as_dict = True)
		if dept is not None:
			department = dept[0]["department"]
		else:
			department = ''	

	if "System Manager" in frappe.get_roles(user):
		return None
	else:
		return """(`tabDocument Management`.owner = {user} or `tabDocument Management`.department = {department})"""\
			.format(user=frappe.db.escape(user),department=frappe.db.escape(department))

def has_permission(doc, user):
	if user!='Administrator':
		dept = frappe.db.sql("""select department from `tabEmployee` where user_id='{0}';""".format(user), as_dict = True)
			
		if dept is not None:
			department = dept[0]["department"]
		else:
			department = ''
	
	if "System Manager" in frappe.get_roles(user):
		return True
	else:
		return doc.owner==user or doc.department==department