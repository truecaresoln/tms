# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import datetime
import datetime
from frappe.utils import add_days, flt, get_datetime, get_time, get_url, nowtime, today
from frappe import _

from frappe.model.document import Document
from tms.utils.approvals import insert_approvals

class Challenges(Document):
	def validate(self):
		self.update_approval()
		self.insert_todo()
	
	def update_approval(self):
		document = "Challenges"
		employee_name = frappe.db.sql("""select full_name from `tabUser` where name='{0}'""".format(frappe.session.user),as_dict=True)
		approver = frappe.db.sql("""Select full_name from `tabUser` where name='{0}'""".format(self.approver),as_dict = True)
		if approver:
			reporting_manager_id = self.approver
			full_name = approver[0]['full_name']
		insert_approvals(document,self.name,reporting_manager_id,full_name,frappe.session.user,employee_name[0]["full_name"],self.workflow_state)	

	# def update_approval(self):
	# 	name1 = "Challenges and Commitments - %s" %self.name
	# 	checkUser = frappe.session.user
	# 	employee_name = frappe.db.sql("""select full_name from `tabUser` where name='{0}'""".format(checkUser),as_dict=True)
 		
	# 	check_approval = frappe.get_value('Approvals',name1,'name')
	# 	if (check_approval):
	# 		if self.workflow_state == 'Rejected':
	# 			update_approval = frappe.db.sql("""update `tabApprovals` set status='Rejected' where name='{0}'
	# 				""".format(name1))
	# 		else:
	# 			update_approval = frappe.db.sql("""update `tabApprovals` set status='Approved' where name='{0}'
	# 				""".format(name1))
	# 	else:
	# 		if checkUser != 'Administrator':
	# 			approver = frappe.db.sql("""Select full_name from `tabUser` where name='{0}'""".format(self.approver),as_dict = True)
	# 			if approver:
	# 				reporting_manager_id = self.approver
	# 				full_name = approver[0]['full_name']
	# 				creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	# 				frappe.msgprint(creation)
	# 				modified = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	# 				insert_approval = frappe.db.sql("""insert into `tabApprovals`(name,creation,modified,document,document_name,status,owner,owner_name,employee,employee_name) 
	# 								values('{0}','{6}','{7}','Challenges and Commitments','{1}','Draft','{2}','{3}','{4}','{5}')
	# 								""".format(name1,self.name,reporting_manager_id,full_name,frappe.session.user,employee_name[0]["full_name"],creation,modified))

	def insert_todo(self):
		name = self.name
		allocated_by = frappe.session.user
		allocated_to = self.task_owner
		allocated_to_name = self.task_owner_name
		status = 'Open'
		priority = 'High'
		start_date = self.date
		end_date = self.committed_date
		reference_type = 'Challenges and Commitments'
		reference_name = self.name
		task_description = self.description_of_challenge
		create_todo = self.create_todo
		
		hours = 0
		
		creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		modified = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		
		if create_todo == "Yes":
			data = frappe.db.sql("""select count(*) as cnt from `tabToDo` where name = '{0}';""".format(name), as_dict = True)
			cnt = data[0]['cnt']
			if cnt == 0:
				data1 = frappe.db.sql("""insert into `tabToDo`(name,creation,modified,
					modified_by,owner,status,
					priority,start_date,`date`,
					description,reference_type,
					reference_name,assigned_by,
					allocated_to_full_name,hours) values('{0}','{1}','{2}','{3}','{4}','{5}',
					'{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}');""".format(name,creation,modified,
					allocated_by,allocated_to,status,priority,start_date,end_date,
					task_description,reference_type,reference_name,allocated_by,allocated_to_name,hours))

@frappe.whitelist(allow_guest=True)			
def getapprover(company_email):
	user_id = company_email
	if user_id:
		data = frappe.db.sql("""select tee.user_id from `tabEmployee` te
				left join `tabEmployee` tee on te.reports_to = tee.name
				WHERE te.user_id = '{0}';""".format(user_id), as_dict = True)
		if data:
			reporting_manager = data[0]['user_id']
		else:
			reporting_manager = ''	
	else:
		reporting_manager = ''
		
	return reporting_manager	
		

def get_permission_query_conditions(user):
	if not user: user = frappe.session.user

	if "System Manager" in frappe.get_roles(user) or "Project Dashboard" in frappe.get_roles(user):
		return None
	else:
		return """(`tabChallenges`.owner = {user} or `tabChallenges`.approver = {user})"""\
			.format(user=frappe.db.escape(user))

def has_permission(doc, user):
	if "System Manager" in frappe.get_roles(user) or "Project Dashboard" in frappe.get_roles(user):
		return True
	else:
		return doc.owner==user or doc.approver==user
