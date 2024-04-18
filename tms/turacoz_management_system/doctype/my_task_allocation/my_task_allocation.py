# -*- coding: utf-8 -*-
# Copyright (c) 2021, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from six import iteritems
from email_reply_parser import EmailReplyParser
from frappe.utils import (flt, getdate, get_url, now,
	nowtime, get_time, today, get_datetime, add_days)
from erpnext.controllers.queries import get_filters_cond
from frappe.desk.reportview import get_match_cond
from erpnext.hr.doctype.daily_work_summary.daily_work_summary import get_users_email
from erpnext.hr.doctype.holiday_list.holiday_list import is_holiday
from frappe.model.document import Document
import datetime
import calendar

class MyTaskAllocation(Document):
	
	def validate(self):
		self.insert_todo()		
	
	def insert_todo(self):
		name = self.name
		allocated_by = self.allocated_by
		allocated_to = self.owner
		allocated_by_name = self.allocated_by_name
		allocated_to_name = self.allocated_to_name
		priority = self.priority
		type = self.type
		start_date = self.start_date
		end_date = self.end_date
		task_description = self.task_description
		status = self.status
		reference_type = 'My Task Allocation'
		reference_name = self.name
		hours = 0
		
		if status != 'Information':
			creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
			modified = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
			
			data = frappe.db.sql("""select count(*) as cnt from `tabToDo` where name = '{0}';""".format(name), as_dict = True)
			cnt = data[0]['cnt']
			
			if cnt == 0:
				if start_date:
					if end_date:
						data1 = frappe.db.sql("""insert into `tabToDo`(name,creation,modified,
								modified_by,owner,status,
								priority,start_date,`date`,
								description,reference_type,
								reference_name,assigned_by,
								assigned_by_full_name,
								allocated_to_full_name,hours) values('{0}','{1}','{2}',
								'{3}','{4}','{5}','{6}','{7}','{8}',
								'{9}','{10}','{11}','{12}','{13}','{14}',
								'{15}');""".format(name,creation,modified,allocated_by,allocated_to,status,
												priority,start_date,end_date,task_description,
												reference_type,reference_name,allocated_by,allocated_by_name,
												allocated_to_name,hours))
					else:
						data1 = frappe.db.sql("""insert into `tabToDo`(name,creation,modified,
								modified_by,owner,status,
								priority,start_date,
								description,reference_type,
								reference_name,assigned_by,
								assigned_by_full_name,
								allocated_to_full_name,hours) values('{0}','{1}','{2}',
								'{3}','{4}','{5}','{6}','{7}','{8}',
								'{9}','{10}','{11}','{12}','{13}','{14}');""".format(name,creation,modified,allocated_by,allocated_to,status,
												priority,start_date,task_description,
												reference_type,reference_name,allocated_by,allocated_by_name,
												allocated_to_name,hours))	
				else:	
					data1 = frappe.db.sql("""insert into `tabToDo`(name,creation,modified,
							modified_by,owner,status,priority,
							description,reference_type,
							reference_name,assigned_by,
							assigned_by_full_name,
							allocated_to_full_name,hours) values('{0}','{1}','{2}',
							'{3}','{4}','{5}','{6}','{7}','{8}',
							'{9}','{10}','{11}','{12}','{13}');""".format(name,creation,modified,allocated_by,allocated_to,status,
											priority,task_description,
											reference_type,reference_name,allocated_by,allocated_by_name,
											allocated_to_name,hours))
			else:
				modified_by = frappe.session.user
				data1 = frappe.db.sql("""Update `tabToDo` set status='{1}',modified_by='{2}' where name='{0}';""".format(name,status,modified_by))
	
				
def get_permission_query_conditions(user):
	if not user: user = frappe.session.user

	if "System Manager" in frappe.get_roles(user):
		return None
	else:
		return """(`tabMy Task Allocation`.owner = {user} or `tabMy Task Allocation`.allocated_by = {user})"""\
			.format(user=frappe.db.escape(user))

def has_permission(doc, user):
	if "System Manager" in frappe.get_roles(user):
		return True
	else:
		return doc.owner==user or doc.allocated_by==user

@frappe.whitelist()
def get_contact_detail(contact_detail):
	if contact_detail:
		data = frappe.db.sql("""Select * from `tabTask Contact Detail` where name='{0}';""".format(contact_detail), as_dict = True)
		company_name = data[0]["company_name"]
		poc_name = data[0]["poc_name"]
		phone = data[0]["phone"]
		email = data[0]["email"]
		url = data[0]["url"]
		address = data[0]["address"]
		if company_name:
			new_company_name = '<b>Company Name:</b> '+company_name
		else:
			new_company_name = ''
		if poc_name:
			new_poc_name = ', </br><b>PoC Name:</b> '+poc_name
		else:
			new_poc_name = ''
		if phone:
			new_phone = ', </br><b>Phone:</b> '+phone
		else:
			new_phone = ''
		if email:
			new_email = ', </br><b>Email:</b> '+email
		else:
			new_email = ''
		if url:
			new_url = ', </br><b>Url:</b> '+url
		else:
			new_url = ''
		if address:
			new_address = ', </br><b>Address:</b> '+address
		else:
			new_address = ''
		final_contact_detail = new_company_name+new_poc_name+new_phone+new_email+new_url+new_address
		frappe.msgprint(final_contact_detail)								
	return final_contact_detail

@frappe.whitelist(allow_guest=True)				
def update_todo_status(self,method=None):
	task_name = self.name
	status = self.status
	f_status = "Open"
	
	if status == 'Open':
		f_status = "Open"
	elif status == 'On Hold':
		f_status = "On Hold"
	elif status == 'Close':
		f_status = "Closed"
	elif status == 'Cancelled':
		f_status = "Cancelled"
			
	if f_status:
		data = frappe.db.sql("""Update `tabToDo` set status='{0}' where name='{1}'""".format(f_status,task_name))
	
def status_overdue_alert():	
	import datetime
	today_date = today()
	data = frappe.db.sql("""SELECT tmta.name, tmta.allocated_to_name, tmta.start_date,
			tmta.end_date,tmta.task_description,tmta.status,tmta.owner,tmta.allocated_by,
			tu.reporting_manager from `tabMy Task Allocation` tmta
			left join `tabUser` tu on tmta.owner = tu.name 
			where tmta.end_date = '{0}'
			and tmta.status in ('Open','Ongoing') 
			and tu.enabled = 1 and tu.reporting_manager != '';""".format(today_date),as_dict = True)
	if data:
		for rec in data:
			reporting_manager = rec.reporting_manager
			
			if reporting_manager == 'dpsingh@turacoz.com':
				subject_fn = rec.name+" Overdue"
				recipients = ["rakeshtripathi@turacoz.com",rec.owner]
				if recipients:
					message = "<table><tr><td><p><i><b>Dear "+rec.allocated_to_name+",</b></i></p></td></tr><tr><td>Your task <b>"+rec.name+"</b> has been overdue. Please take a action ASAP.</td></tr><tr><td><p><b>Thanks & Regards,</b></p></td></tr><tr><td><b>Turacoz Group</b></td></tr></table>"
					frappe.sendmail(recipients=recipients,
					subject=_(subject_fn),
					message = message,
					)
					
			elif reporting_manager == 'namrata@turacoz.com':
				subject_fn = rec.name+" Overdue"
				recipients = ["ashima.jawa@turacoz.com",rec.owner]
				if recipients:
					message = "<table><tr><td><p><i><b>Dear "+rec.allocated_to_name+",</b></i></p></td></tr><tr><td>Your task <b>"+rec.name+"</b> has been overdue. Please take a action ASAP.</td></tr><tr><td><p><b>Thanks & Regards,</b></p></td></tr><tr><td><b>Turacoz Group</b></td></tr></table>"
					frappe.sendmail(recipients=recipients,
					subject=_(subject_fn),
					message = message,
					)
			else:
				subject_fn = rec.name+" Overdue"
				recipients = [rec.allocated_by,rec.owner]
				if recipients:
					message = "<table><tr><td><p><i><b>Dear "+rec.allocated_to_name+",</b></i></p></td></tr><tr><td>Your task <b>"+rec.name+"</b> has been overdue. Please take a action ASAP.</td></tr><tr><td><p><b>Thanks & Regards,</b></p></td></tr><tr><td><b>Turacoz Group</b></td></tr></table>"
					frappe.sendmail(recipients=recipients,
					subject=_(subject_fn),
					message = message,
					)		
				 	
	
	

		