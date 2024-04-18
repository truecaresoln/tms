# -*- coding: utf-8 -*-
# Copyright (c) 2021, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
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

class TeamAlignment(Document):
	
	def validate(self):
		self.insert_todo()
		self.insert_freelancer()
		self.send_welcome_email()
		self.updateProjectStage()
		
	def insert_todo(self):
		
		project = self.project
		reference_type = self.reference_type
		reference_name = self.reference_name
		assigned_by = frappe.session.user
		status = 'Open'
		priority = 'Normal'
		creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		modified = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		
		dms_link = self.dms_project_link
		
		
		for d in self.get("team_detail"):
			
			allocated_to = d.allocated_to
			role = d.role
			start_date= d.start_date
			due_date = d.date
			description = d.description
			working_status = d.is_working
			todo_name = d.todo_name
			allocated_to_full_name = d.allocated_to_full_name
			allocated_hours = d.allocated_hours			
			
			get_todo = frappe.db.sql("""select  count(*) as name_count from `tabToDo` where name = '{0}';""".format(todo_name), as_dict=True)
			todo_ol_name = get_todo[0]['name_count']
			if todo_ol_name == 0:					
				if start_date is None:
					insert_todo = frappe.db.sql("""Insert into `tabToDo`(name,status,priority,date,owner,description,
					reference_type,reference_name,project,role,assigned_by,allocated_to_full_name,hours,creation,modified) 
					Values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}');""".format(todo_name,status,priority,due_date,allocated_to,description,reference_type,reference_name,project,role,assigned_by,allocated_to_full_name,allocated_hours,creation,modified), as_dict=True)
				else:
					insert_todo = frappe.db.sql("""Insert into `tabToDo`(name,status,priority,date,owner,description,
					reference_type,reference_name,project,role,assigned_by,allocated_to_full_name,hours,creation,modified,start_date) 
					Values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}');""".format(todo_name,status,priority,due_date,allocated_to,description,reference_type,reference_name,project,role,assigned_by,allocated_to_full_name,allocated_hours,creation,modified,start_date), as_dict=True)	
			else:
				if working_status:
					update_to_status = frappe.db.sql("""Update `tabToDo` set status='{0}',date='{1}',hours='{2}',role='{3}',modified='{4}',start_date = '{6}' where name = '{5}'""".format(working_status,due_date,allocated_hours,role,todo_name,modified,start_date))
	
	def updateProjectStage(self):
		projectStage = self.project_stage
		if projectStage:
			data = frappe.db.sql("""Update `tabProject Work Process` set is_team_aligned = 1 where name='{0}'""".format(projectStage))
			
			data1 = frappe.db.sql("""Update `tabProject Work Process Log` set is_team_aligned = 1 where process_name='{0}'""".format(projectStage))
	
	def send_welcome_email(self):
		if self.dms_project_link:
			dms_link = self.dms_project_link
		else:
			dms_link = ""	
		url = "http://erp.turacoz.com/app/project/{0}".format(self.project)
		messages = (
			_("You got the new project: {0}".format(self.project)),
			url,
			_("Join")
		)

		content = """
		<p>{0}.</p>
		<p><a href="{1}">{2}</a></p>
		"""

		for user in self.team_detail:
			if user.email_sent == 0:
    # frappe.sendmail(user.allocated_to, subject=_("You got new Project"),
    # 				content=content.format(*messages))
				mylist = user.allocated_to
				frappe.sendmail(recipients=mylist,
					subject=_("You got the new project " + self.project),
					message="<b>Dear User,</b><br><br>You got a new project <b><a href="+url+">"+self.project+"</a></b> to work as <b>"+user.role+"</b>. Please check you ERP ToDo List.</br></br>To Upload the documents, please use this link <a href="+dms_link+">"+dms_link+"</a><br><br>Regards<br>Turacoz ERP",
					header=['New Project', 'green'],
				)
				user.email_sent = 1
	
	def insert_freelancer(self):
		
		project = self.project
		task = self.task
		assigned_by = frappe.session.user
		parenttype = 'Freelancer'
		parentfield = 'project_detail_and_feedback'
		creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		modified = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		
		
		for d in self.get("align_freelancer"):
			
			freelancer = d.freelancer
			role = d.role
			type_of_document = d.type_of_document
			start_date = d.start_date
			close_date = d.close_date
			status = d.status
			freelancer_project_detail_name = d.freelancer_project_detail_name			
			
			get_todo = frappe.db.sql("""select  count(*) as name_count from `tabFreelancer Feedback Project Detail` where name = '{0}';""".format(freelancer_project_detail_name), as_dict=True)
			todo_ol_name = get_todo[0]['name_count']
			if todo_ol_name == 0:					
				insert_todo = frappe.db.sql("""Insert into `tabFreelancer Feedback Project Detail`(name,project,role,type_of_documents,start_date,project_close_date,
				parent,parenttype,parentfield,creation,modified,status) 
				Values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}');""".format(freelancer_project_detail_name,project,role,type_of_document,start_date,close_date,freelancer,parenttype,parentfield,creation,modified,status), as_dict=True)
			else:
				if start_date is None:
					update_to_status = frappe.db.sql("""Update `tabFreelancer Feedback Project Detail` set status='{0}', modified='{1}' where name = '{2}'""".format(status,modified,freelancer_project_detail_name))
				else:
					update_to_status = frappe.db.sql("""Update `tabFreelancer Feedback Project Detail` set status='{0}',modified='{1}' where name = '{2}'""".format(status,modified,freelancer_project_detail_name))
					
	pass

@frappe.whitelist(allow_guest=True)
def getprojectUpdates(project):
# 	project = self.project
# 	frappe.msgprint(project)
	getUpdates = frappe.db.sql("""select * from `tabProject Update Data` where parent='{0}' and deliverable!='General Update';""".format(project), as_dict=True)
	return getUpdates

@frappe.whitelist(allow_guest=True)
def getprojecthours(task,allocated_hours):
# 	project = self.project
	getdata = frappe.db.sql("""select expected_time from `tabTask` where name='{0}'""".format(task),as_dict=True)
	expected_hrs = getdata[0]['expected_time']
	remain = int(expected_hrs) - int(allocated_hours)
	if remain < 0:
		a = 0
	else:
		a = 1
	return a
			
@frappe.whitelist(allow_guest=True)
def getprojectProposed(project):
	getProposedUpdates = frappe.db.sql("""select * from `tabProject Proposed Date Data` where parent='{0}' and deliverable!='General Update';""".format(project), as_dict=True)
	return getProposedUpdates

@frappe.whitelist(allow_guest=True)
def setUser(doctype, txt, searchfield, start, pagelen, filters):
	userid = frappe.session.user
	getReporties = frappe.db.sql("""select name,full_name  from `tabUser` where reporting_manager='{0}' and enabled=1 UNION
	select name,full_name from `tabUser` where name = '{1}' UNION
	select name,full_name from `tabUser` where department = 'Program, Designing and Development - THS' and enabled=1 and name not in ('atul.teotia@turacoz.com');""".format(userid,userid), as_list=1)
	return getReporties
	
@frappe.whitelist(allow_guest=True)
def todo_after_update(self,method=None):
	project = self.project
	reference_type = self.reference_type
	reference_name = self.reference_name
	assigned_by = frappe.session.user
	status = 'Open'
	priority = 'Normal'
	creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	modified = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	
	for d in self.get("team_detail"):
  # start_date = d.start_date
		allocated_to = d.allocated_to
		role = d.role
		
		start_date = d.start_date	
		due_date = d.date
		description = d.description
		working_status = d.is_working
		todo_name = d.todo_name
		allocated_to_full_name = d.allocated_to_full_name
		allocated_hours = d.allocated_hours
		
		if self.dms_project_link:
			dms_link = self.dms_project_link
		else:
			dms_link = ""
		get_todo = frappe.db.sql("""select  count(*) as name_count from `tabToDo` where name = '{0}';""".format(todo_name), as_dict=True)
		todo_ol_name = get_todo[0]['name_count']
		if todo_ol_name == 0:
			if start_date is None:
				insert_todo = frappe.db.sql("""Insert into `tabToDo`(name,status,priority,date,owner,description,
				reference_type,reference_name,project,role,assigned_by,allocated_to_full_name,hours,creation,modified) 
				Values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}');""".format(todo_name,status,priority,due_date,allocated_to,description,reference_type,reference_name,project,role,assigned_by,allocated_to_full_name,allocated_hours,creation,modified), as_dict=True)
			else:
				insert_todo = frappe.db.sql("""Insert into `tabToDo`(name,status,priority,date,owner,description,
				reference_type,reference_name,project,role,assigned_by,allocated_to_full_name,hours,creation,modified,start_date) 
				Values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}');""".format(todo_name,status,priority,due_date,allocated_to,description,reference_type,reference_name,project,role,assigned_by,allocated_to_full_name,allocated_hours,creation,modified,start_date), as_dict=True)	
		else:
			if working_status:
				if start_date is None:
					update_to_status = frappe.db.sql("""Update `tabToDo` set status='{0}',date='{1}',hours='{2}',role='{3}',modified='{4}' where name = '{5}'""".format(working_status,due_date,allocated_hours,role,modified,todo_name))
				else:
					update_to_status = frappe.db.sql("""Update `tabToDo` set status='{0}',date='{1}',hours='{2}',role='{3}',modified='{4}',start_date='{5}' where name = '{6}'""".format(working_status,due_date,allocated_hours,role,modified,start_date,todo_name))
					
		url = "http://erp.turacoz.com/app/Project/{0}".format(self.project)
		messages = (
			_("You got the new project: {0}".format(self.project)),
			url,
			_("Click for Project")
		)
 
		content = """
		<p>{0}.</p>
		<p><a href="{1}">{2}</a></p>
		"""
 			
		for user in self.team_detail:
			if user.email_sent == 0:
				frappe.msgprint(user.email_sent)
    # print(user.allocated_to)
				mylist = user.allocated_to
				frappe.sendmail(recipients=mylist,
			    	subject=_("You got the new project " + self.project),
			    	message="<b>Dear User,</b><br><br>You got a new project <b><a href="+url+">"+self.project+"</a></b> to work as <b>"+user.role+"</b>. Please check you ERP ToDo List.</br></br>To Upload the documents, please use this link <a href="+dms_link+">"+dms_link+"</a><br><br>Regards<br>Turacoz ERP",
			    	header=['New Project', 'green'],
			    )
    # frappe.sendmail(user.allocated_to, subject=_("You got new Project"),
    # 				content=content.format(*messages))
				user.email_sent = 1	

@frappe.whitelist(allow_guest=True)						
def after_update_freelancer(self,method=None):
	project = self.project
	task = self.task
	assigned_by = frappe.session.user
	parenttype = 'Freelancer'
	parentfield = 'project_detail_and_feedback'
		
	for d in self.get("align_freelancer"):
		freelancer = d.freelancer
		role = d.role
		type_of_document = d.type_of_document
		start_date = d.start_date
		close_date = d.close_date
		freelancer_project_detail_name = d.freelancer_project_detail_name
						
		get_todo = frappe.db.sql("""select  count(*) as name_count from `tabFreelancer Feedback Project Detail` where name = '{0}';""".format(freelancer_project_detail_name), as_dict=True)
		todo_ol_name = get_todo[0]['name_count']
		if todo_ol_name == 0:					
			insert_todo = frappe.db.sql("""Insert into `tabFreelancer Feedback Project Detail`(name,project,role,type_of_documents,start_date,project_close_date,
			parent,parenttype,parentfield) 
			Values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');""".format(freelancer_project_detail_name,project,role,type_of_document,start_date,close_date,freelancer,parenttype,parentfield), as_dict=True)
		else:
			update_to_status = frappe.db.sql("""Update `tabFreelancer Feedback Project Detail` set start_date='{0}',project_close_date='{1}' where name = '{2}'""".format(start_date,close_date,freelancer_project_detail_name))
	
		
		
