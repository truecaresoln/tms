# Copyright (c) 2023, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeePerformanceFeedback(Document):
	
	def validate(self):
		self.validate_total_score()
		
	def validate_total_score(self):
		total = 0
		for d in self.get("performance_rating"):
			total += int(d.rating)	
		self.total_score = round(total/6,2)				 			
				
@frappe.whitelist(allow_guest=True)
def get_param(employee):
	data = frappe.db.sql("""select name from `tabEmployee Performance Feedback Parameters` where status = 'Enabled';""", as_dict=True)
	return data

