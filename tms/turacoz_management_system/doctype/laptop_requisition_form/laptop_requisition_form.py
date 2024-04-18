# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LaptopRequisitionForm(Document):
	pass

@frappe.whitelist(allow_guest=True)
def get_template_detail(userid):
	getData = frappe.db.sql("""select declaration from `tabLaptop Requisition Declaration Template`;""", as_dict = True)
	if getData:
		emp_code = getData[0]['declaration']
	else:
		emp_code = ''	
	return emp_code

