# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe
from datetime import date
import datetime

def insert_approvals(document,document_name,approver,approver_name,employee,employee_name,workflow_state):
	
	name1 = document+' - '+document_name
	status = 'Draft'
	check_approval = frappe.db.sql("""Select name from `tabApprovals` where name = '{0}';""".format(name1), as_dict=True)
	if check_approval:
		approval_name = check_approval[0]['name']
	else:
		approval_name = ''	

	if approval_name:
		if workflow_state == 'Rejected':
			update_approval = frappe.db.sql("""update `tabApprovals` set status='Rejected' where name='{0}'
					""".format(name1))
		elif workflow_state == 'Approved':
			update_approval = frappe.db.sql("""update `tabApprovals` set status='Approved' where name='{0}'
					""".format(name1))
		elif workflow_state == 'Approved by Reporting Manager':
			update_approval = frappe.db.sql("""update `tabApprovals` set status='Approved' where name='{0}'
					""".format(name1))
		elif workflow_state == 'Approved by Contract Approver':
			update_approval = frappe.db.sql("""update `tabApprovals` set status='Approved' where name='{0}'
					""".format(name1))
		elif workflow_state == 'Approved by Accountant':
			update_approval = frappe.db.sql("""update `tabApprovals` set status='Approved' where name='{0}'
					""".format(name1))
		elif workflow_state == 'Approved by Sales Order Approver':
			update_approval = frappe.db.sql("""update `tabApprovals` set status='Approved' where name='{0}'
					""".format(name1))
	else:
		creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		modified = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		insert_approval = frappe.db.sql("""insert into `tabApprovals`(name,creation,modified,document,document_name,status,owner,owner_name,employee,employee_name) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')
			""".format(name1,creation,modified,document,document_name,status,approver,approver_name,employee,employee_name))
	