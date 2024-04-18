# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PublishedArticles(Document):
	pass

@frappe.whitelist(allow_guest=True)						
def after_update_status(self,method=None):
	project = self.project
	record_name = self.name
		
	for d in self.get("publish_log"):
		status = d.status
		
		if status == "Submitted":
			self.status = "In Submission"
			
			f_status = "In Submission"
			data = frappe.db.sql("""UPDATE `tabPublished Articles` set article_status='{0}' where name ='{1}';""".format(f_status,record_name))
		elif status == "Accepted":
			self.article_status = "In Acceptance"
			
			f_status = "In Acceptance"
			data = frappe.db.sql("""UPDATE `tabPublished Articles` set article_status='{0}' where name ='{1}';""".format(f_status,record_name))
		elif status == "Published":
			self.article_status = "Published"
			
			f_status = "Published"
			data = frappe.db.sql("""UPDATE `tabPublished Articles` set article_status='{0}' where name ='{1}';""".format(f_status,record_name))
		elif status == "Rejected":
			self.article_status = "Rejected"
			
			f_status = "Rejected"
			data = frappe.db.sql("""UPDATE `tabPublished Articles` set article_status='{0}' where name ='{1}';""".format(f_status,record_name))			
