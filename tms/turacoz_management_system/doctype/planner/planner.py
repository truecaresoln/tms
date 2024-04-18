# -*- coding: utf-8 -*-
# Copyright (c) 2021, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Planner(Document):
	pass


@frappe.whitelist()
def fetch_details_department(userid):
	if userid:
		data = frappe.db.sql("""Select department from `tabEmployee` where company_email='{0}' limit 1;""".format(userid), as_dict = True)
		if data:
			department = data[0]["department"]
		else:
			department = ''	
	else:
		department = ''	
	return department

@frappe.whitelist()
def fetch_details_designation(userid):
	if userid:
		data = frappe.db.sql("""Select designation from `tabEmployee` where company_email='{0}' limit 1;""".format(userid), as_dict = True)
		if data:
			designation = data[0]["designation"]
		else:
			designation = ''	
	else:
		designation = ''	
	return designation