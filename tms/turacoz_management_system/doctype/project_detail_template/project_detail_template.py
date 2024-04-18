# -*- coding: utf-8 -*-
# Copyright (c) 2021, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint
from importlib import reload

class ProjectDetailTemplate(Document):
	def validate(self):
		self.set_project_coordinators()
		self.update_approval()
	
	def update_approval(self):
		name1 = "Project Detail Template - %s" %self.name
		approver = frappe.db.sql("""select thr.parent,thr.role,tu.full_name from `tabHas Role` thr
					left join `tabUser` tu on thr.parent=tu.name
					where thr.role='Technical Project Head'""",as_dict = True)
		employee = frappe.db.sql("""select full_name from `tabUser` where name='{0}'""".format(frappe.session.user),as_dict = True)
		 
		check_approval = frappe.get_value('Approvals',name1,'name')
		if (check_approval):
			if self.workflow_state == 'Rejected':
				update_approval = frappe.db.sql("""update `tabApprovals` set status='Rejected' where name='{0}'
					""".format(name1), as_dict = True)
			else:
				update_approval = frappe.db.sql("""update `tabApprovals` set status='Approved' where name='{0}'
					""".format(name1), as_dict = True)
		else:
			insert_approval = frappe.db.sql("""insert into `tabApprovals`(name,document,document_name,status,owner,owner_name,employee,employee_name) values('{0}','Project Detail Template','{1}','Draft','{2}','{3}','{4}','{5}')
			""".format(name1,self.name,approver[0]['parent'],approver[0]['full_name'],frappe.session.user,employee[0]['full_name']), as_dict = True)
	
	def set_project_coordinators(self):
		record_name = self.name
		project_manager = self.project_manager
		team_lead_medical_writer = self.team_lead_medical_writer
		if(project_manager):
			check_coordinators = frappe.db.get_value('Project Coordinators', record_name, 'name')
			if(check_coordinators):
# 				print('welcome')
# 				doc = frappe.get_doc("Project Coordinators", record_name)
# 				doc.project_manager = project_manager
# 				doc.team_leader = team_lead_medical_writer
# 				doc.save()
				update_coordinators = frappe.db.sql("""Update `tabProject Coordinators` set project_manager='{0}',
				team_leader='{1}' where name='{2}'""".format(project_manager,team_lead_medical_writer,record_name), as_dict = True)
 				
			else:	
 				
				insert_coordinators = frappe.db.sql("""insert into `tabProject Coordinators` (name,project_detail_template,
				project_manager,team_leader) 
				values('{0}','{1}','{2}','{3}')""".format(record_name,record_name,project_manager,team_lead_medical_writer), as_dict = True)	
	
	pass 


@frappe.whitelist(allow_guest=True)
def update_project_coordinators(self,method=None):
	 record_name = self.name
	 project_manager = self.project_manager
	 team_lead_medical_writer = self.team_lead_medical_writer
	 if(project_manager):
			check_coordinators = frappe.db.get_value('Project Coordinators', record_name, 'name')
			if(check_coordinators):
# 				print('welcome')
# 				doc = frappe.get_doc("Project Coordinators", record_name)
# 				doc.project_manager = project_manager
# 				doc.team_leader = team_lead_medical_writer
# 				doc.save()
				update_coordinators = frappe.db.sql("""Update `tabProject Coordinators` set project_manager='{0}',
				team_leader='{1}' where name='{2}'""".format(project_manager,team_lead_medical_writer,record_name), as_dict = True)
 				
			else:	
 				
				insert_coordinators = frappe.db.sql("""insert into `tabProject Coordinators` (name,project_detail_template,
				project_manager,team_leader) 
				values('{0}','{1}','{2}','{3}')""".format(record_name,record_name,project_manager,team_lead_medical_writer), as_dict = True)
	 frappe.msgprint(record_name)

@frappe.whitelist(allow_guest=True)
def setUser(doctype, txt, searchfield, start, pagelen, filters):
	department = 'Business Development - THS'
	getReporties = frappe.db.sql("""select DISTINCT name from `tabUser` where department='{0}'""".format(department), as_list=1)
	return getReporties

# 		
	
# 		self.get_project()
# 		a = on_submit()
# 		a.save()
# 	@frappe.whitelist()
# 	def on_update(self):
# 		record_name = self.name
# 		project_manager = self.project_manager
# 		return {"record":record_name, "project_manager": project_manager}
# # 		print("on update wwwwwwww")
# # 		msgprint("helloooooooooooooooooooooooooooooooooooooooooooooooooooo")			
# 
# 	@frappe.whitelist()
# 	def callme(salary):
# 		salary = 3
# 		return salary

# 	@frappe.whitelist()
# 	def get_prod_type():
# 		value = "metal"
# 		return value
# 
#  	
# # 	def on_submit(self):	
# # 		set_project_coordinators()
# # 		get_project()
# 		

# 	
# 
@frappe.whitelist(allow_guest=True)	
def update_coordinators_in_project(self,method=None):
 	 record_name = self.name
 	 project_manager = self.project_manager
 	 team_lead_medical_writer = self.team_lead_medical_writer
 	 if(record_name):
 	 	check_project = frappe.db.sql("""select project from `tabProject Coordinators` where name='{0}';""".format(record_name),as_dict=True)
 	 	if check_project:
 	 		for rec in check_project:
 	 			project=rec.project
 	 			if project:
 	 				update_coordinators = frappe.db.sql("""Update `tabProject` set project_manager='{0}',
 	 				team_leader_medical_writer='{1}' where name='{2}'""".format(project_manager,team_lead_medical_writer,project), as_dict = True)

@frappe.whitelist(allow_guest=True)	
def get_pms_detail(userid):
	
	getPMData = frappe.db.sql("""select te.employee_name, count(tp.name) as projects_count from `tabEmployee` te
		left join `tabProject` tp on te.user_id = tp.project_manager
		where te.status  = 'Active' and te.department = 'Project Management - THS' 
		and tp.project_current_status in ('Ongoing') group by te.employee_name order by te.employee_name;""", as_dict = True)
	
	if getPMData:
		data = getPMData
	else:
		data = ''
	
	return data									
					
					
					
					