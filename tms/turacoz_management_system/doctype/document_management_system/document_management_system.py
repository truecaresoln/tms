# Copyright (c) 2023, RSA and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
import frappe
from datetime import datetime
import datetime
import os
import shutil
from frappe.utils import add_days, flt, get_datetime, get_time, get_url, nowtime, today
from frappe import _
from frappe.model.document import Document
from tms.utils.approvals import insert_approvals

class DocumentManagementSystem(Document):
	def validate(self):
		if self.is_new():
			self.versioning()
			self.directories()
		self.update_approval()		
	
	def update_approval(self):
		document = "Document Management System"
		employee_name = frappe.db.sql("""select full_name from `tabUser` where name='{0}'""".format(frappe.session.user),as_dict=True)
		approver = frappe.db.sql("""select thr.parent,usr.full_name from `tabHas Role` thr 
				left join `tabUser` usr on thr.parent=usr.name
				where `role` ='DMS Approver' and full_name is not null order by 1 desc limit 1""",as_dict = True)
		reporting_manager_id = approver[0]['parent']
		full_name = approver[0]['full_name']
		insert_approvals(document,self.name,reporting_manager_id,full_name,frappe.session.user,employee_name[0]["full_name"],self.workflow_state)	

	def versioning(self):
		document_title = self.document_title
		document_type = self.document_type
		file_type = self.file_type
		
		dataDuplicate = frappe.db.sql("""select count(*) 'total' from `tabDocument Management System`
							where document_title='{0}' and document_type='{1}' and file_type='{2}'""".format(document_title,document_type,file_type),as_dict=True)
		
		self.version = dataDuplicate[0]['total']
	
	def directories(self):
		path = '/home/azureuser/frappe-bench/sites/erp.turacoz.com/public/files/'
		new_path = self.department
		if self.category:
			dataCategory = frappe.db.sql("""select category from `tabDMS Category` where name='{0}'""".format(self.category),as_dict=True)
			category = dataCategory[0]['category']
			new_path = new_path + '/'+ category
		else:
			category = ''
			
		if self.sub_category:
			dataSubCategory = frappe.db.sql("""select sub_category from `tabDMS Sub Category` where name='{0}'""".format(self.sub_category),as_dict=True)
			sub_category = dataSubCategory[0]['sub_category']
			new_path = new_path + '/' + sub_category
		else:
			sub_category = ''

		mode = 0o777
		if self.department=='Medical Services':
			new_path = new_path + '/' + self.project_code
		
		path = path + new_path	
		if not os.path.exists(path):
			os.makedirs(path,mode)
		os.chmod(path,mode)
		source = '/home/azureuser/frappe-bench/sites/erp.turacoz.com/public' + self.document_attachment
		path = path + '/' + self.document_title + '_' + self.document_type +'_'+ str(self.version) + '.' + self.file_type 
  # shutil.copy2(source,path)
		shutil.move(source,path)
		filename = os.path.basename(path).split('/')[-1]
		basename = filename.split('.')[0]

		file1 = 'https://erp.turacoz.com/files/' + new_path + '/' + filename
		self.file_link = "<a href='{0}'>{0}</a>".format(file1)
		self.document_attachment = self.file_link
		self.sharable_link_hidden = file1


def get_permission_query_conditions(user):
	if not user: 
		user = frappe.session.user

	if "System Manager" in frappe.get_roles(user):
		return None
	else:
		dept = frappe.db.sql("""select department from `tabUser` where name='{0}'""".format(user),as_dict=True)
		return """(`tabDocument Management System`.owner = {user} or `tabDocument Management System`.department_name = {dept})"""\
			.format(user=frappe.db.escape(user),dept=frappe.db.escape(dept[0]['department']))

def has_permission(doc, user):
	if "System Manager" in frappe.get_roles(user):
		return True
	else:
		dept = frappe.db.sql("""select department from `tabUser` where name='{0}'""".format(user),as_dict=True)
		return doc.owner==user or doc.department_name==dept[0]['department']
			
@frappe.whitelist(allow_guest=True)
def update_todo_status(self,method=None):
	todo_name = self.task_allocated
	if todo_name and self.document_attachment:
		modified_by = frappe.session.user
		data1 = frappe.db.sql("""Update `tabToDo` set status='Closed',modified_by='{1}' where name='{0}' and status in ('Open','Overdue');""".format(todo_name,modified_by))

@frappe.whitelist(allow_guest=True)		
def getroles(user):
	return frappe.get_roles(user)


