# -*- coding: utf-8 -*-
# Copyright (c) 2021, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ProjectNewUpdate(Document):
	pass

@frappe.whitelist(allow_guest=True)				
def wrap_up_call_alert(self,method=None):
	is_wrap_up_call = self.is_wrap_up_call_fixed
	if is_wrap_up_call == "Yes":
		name = self.name
		wrap_call_date = self.wrap_call_date
		time = self.time
		final_draft_link = self.final_draft_link
		any_issue = self.remark
				
		getProjectData = frappe.db.sql("""SELECT  name,customer,contact_person,project_title, 
				project_scope, expected_hour, total_planned_hours, 
				actual_time, manager_name from `tabProject` WHERE name = '{0}'""".format(name), as_dict = True)
		if getProjectData:
			
			project_code = getProjectData[0]['name']
			
			if getProjectData[0]['customer']:
				customer = getProjectData[0]['customer']
			else:
				customer = ''
				
			if getProjectData[0]['contact_person']:
				contact_person = getProjectData[0]['contact_person']
			else:
				contact_person = ''
				
			if getProjectData[0]['project_title']:
				project_title = getProjectData[0]['project_title']
			else:
				project_title = ''
				
			if getProjectData[0]['project_scope']:
				project_scope = getProjectData[0]['project_scope']
			else:
				project_scope = ''
				
			if getProjectData[0]['expected_hour']:
				expected_hour = float(getProjectData[0]['expected_hour'])
			else:
				expected_hour = 0.0
			
			if getProjectData[0]['total_planned_hours']:
				total_planned_hours = float(getProjectData[0]['total_planned_hours'])
			else:
				total_planned_hours = 0.0
															
			if getProjectData[0]['actual_time']:
				actual_time = float(getProjectData[0]['actual_time'])
			else:
				actual_time = 0.0
				
			if getProjectData[0]['manager_name']:
				manager_name = getProjectData[0]['manager_name']
			else:
				manager_name = ''		
				
			if expected_hour == actual_time:
				profitability = "No Loss No Profit"
			elif expected_hour > actual_time:
				profitability = "PROFIT"
			elif expected_hour < actual_time:
				profitability = "LOSS"
			
			getDrfater = frappe.db.sql("""select GROUP_CONCAT( distinct allocated_to_full_name) as drafter 
				from `tabToDo` where project = '{0}' 
				and `role` = 'Drafter' and status  not in ('Cancelled')""".format(getProjectData[0]['name']), as_dict = True)
			if getDrfater:
				if getDrfater[0]['drafter'] is None:
					drafter = ''
				else:
					drafter = getDrfater[0]['drafter']
			else:
				drafter = ''
			
			getQcer = frappe.db.sql("""select GROUP_CONCAT( distinct allocated_to_full_name) as qcer 
				from `tabToDo` where project = '{0}' 
				and `role` = 'QCer' and status  not in ('Cancelled')""".format(getProjectData[0]['name']), as_dict = True)
			if getQcer:
				if getQcer[0]['qcer'] is None:
					qcer = ''
				else:
					qcer = getQcer[0]['qcer']
			else:
				qcer = ''
				
			getReviewer = frappe.db.sql("""select GROUP_CONCAT( distinct allocated_to_full_name) as reviewer 
				from `tabToDo` where project = '{0}' 
				and `role` = 'Reviewer' and status  not in ('Cancelled')""".format(getProjectData[0]['name']), as_dict = True)
			if getReviewer:
				if getReviewer[0]['reviewer'] is None:
					reviewer = ''
				else:
					reviewer = getReviewer[0]['reviewer']
			else:
				reviewer = ''						
							
		recepent = ['atul.teotia@turacoz.com','namrata@turacoz.com']
		frappe.sendmail(recipients=recepent,
				subject = (project_code + " Wrap up call with Client"),
				message = "Dear All, <br><br> Wrap call has been scheduled with client. Kindly check given below detail: <br><br><li><b>Wrap up call Date: </b>"+ wrap_call_date +"</li><br><li><b>Wrap Call Time: </b>"+ time +"</li><br><li><b>Project Code: </b>"+ getProjectData[0]['name'] +"</li><br><li><b>Client: </b>"+ customer +"</li><br><li><b>Client PoC: </b>"+ contact_person +"</li><br><li><b>Project Title: </b>"+ project_title +"</li><br><li><b>Project Scope: </b>"+ project_scope +"</li><br><li><b>Drafter: </b>"+ drafter +"</li><br><li><b>Reviewer: </b>"+ reviewer +"</li><br><li><b>Qcer: </b>"+ qcer +"</li><br><li><b>Project Manager: </b>"+ manager_name +"</li><br><li><b>Final Draft: </b>"+ final_draft_link +"</li><br><li><b>Any Issue: </b>"+ any_issue +"</li><br><li><b>Budgetted hours: </b>"+ str(expected_hour) +"</li><br><li><b>Proposed Effort Hours: </b>"+ str(total_planned_hours) +"</li><br><li><b>Actual Effort Hours: </b>"+ str(actual_time) +"</li><br><li><b>Profitability: </b>"+ profitability +"</li>.<br><br>Regards<br>Turacoz ERP",
			)
		
		
