# Copyright (c) 2023, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProjectLogs(Document):
	
	def validate(self):
		self.send_log_email()



	def send_log_email(self):
		project = self.project_code
		
		for d in self.get("during_project_duration"):
			email_sent = d.email_sent
			if d.title:
				title = d.title
			else:
				title = ''
			
			if d.date:
				date = d.date
			else:			
				date  = ''
			
			if d.user:	
				user = d.user
			else:
				user = ''
				
			if d.client_poc:		
				client_poc = d.client_poc
			else:
				client_poc = ''	
				
			if d.description:
				description = d.description
			else:
				description = ''	
			
			if email_sent == 0:
								
				recepent = ['rakeshtripathi@turacoz.com']	
				frappe.sendmail(recipients=recepent,
					subject= (project + " New log entered"),
					message = "<b>Dear Sir/Ma'am,</b><br><br> New log inserted for project (<b>"+project+")</b>. Kindly take a look.<br><br><li><b>Title: </b>"+title+"</li><li><b>Date: </b>"+str(date)+"</li><li><b>User: </b>"+user+"</li><li><b>Client PoC: </b>"+client_poc+"</li><li><b>Description: </b>"+description+"</li><br><br>Regards<br>Turacoz ERP",
				)
				
				d.email_sent = 1
