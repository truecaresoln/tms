# -*- coding: utf-8 -*-
# Copyright (c) 2021, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.model.document import Document
from tms.utils.approvals import insert_approvals

class ProjectContractDocument(Document):
	def update_approval(self):
		document = "Project Contract Document"
		approver = frappe.db.sql("""select thr.parent,tu.full_name from `tabHas Role` thr
				left join `tabUser` tu on thr.parent=tu.name
				where thr.role='PCD Approver' limit 1""",as_dict = True)
		reporting_manager_id = approver[0]['parent']
		full_name = approver[0]['full_name']
		employee_name = frappe.db.sql("""select full_name from `tabUser` where name='{0}'""".format(frappe.session.user),as_dict = True)
		insert_approvals(document,self.name,reporting_manager_id,full_name,frappe.session.user,employee_name[0]['full_name'],self.workflow_state)	

	def validate(self):
 		self.update_approval()
	

	# def update_approval(self):
	# 	name1 = "Project Contract Document - %s" %self.name
	# 	approver = frappe.db.sql("""select thr.parent,tu.full_name from `tabHas Role` thr
	# 					left join `tabUser` tu on thr.parent=tu.name
	# 					where thr.role='PCD Approver' limit 1""",as_dict = True)
	# 	employee = frappe.db.sql("""select full_name from `tabUser` where name='{0}'""".format(frappe.session.user),as_dict = True)
		 
	# 	check_approval = frappe.get_value('Approvals',name1,'name')
	# 	if (check_approval):
	# 		if self.workflow_state == 'Rejected':
	# 			update_approval = frappe.db.sql("""update `tabApprovals` set status='Rejected' where name='{0}'
	# 				""".format(name1))
	# 		else:
	# 			update_approval = frappe.db.sql("""update `tabApprovals` set status='Approved' where name='{0}'
	# 				""".format(name1))
	# 	else:
	# 		creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	# 		modified = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	# 		insert_approval = frappe.db.sql("""insert into `tabApprovals`(name,creation,modified,document,document_name,status,owner,owner_name,employee,employee_name) values('{0}','{6}','{7}','Project Contract Document','{1}','Draft','{2}','{3}','{4}','{5}')
	# 		""".format(name1,self.name,approver[0]['parent'],approver[0]['full_name'],frappe.session.user,employee[0]['full_name'],creation,modified))
	
	
	pass
