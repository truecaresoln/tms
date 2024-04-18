# Copyright (c) 2023, RSA and contributors
# For license information, please see license.txt

from frappe import _
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	
	data = []
	
	userid = frappe.session.user
	
	if userid:
		if userid != 'Administrator':
			getUserName = frappe.db.sql("""Select employee_name from `tabEmployee` where user_id='{0}';""".format(userid),as_dict=True)
			user_name = getUserName[0]['employee_name']
		else:
			user_name = 'Administrator'	
		
		pending_approval = getPendingApproval(userid)
		overdue_task = getOverDueTask(userid)
		
		row = {}
		row['name'] = user_name
		row['pending_approval'] = pending_approval[0]['pending_approvals']
		row['overdue_task'] = overdue_task[0]['overdue_tasks']
		
		data.append(row)
		
	return data

def getPendingApproval(userid):
	getPendingApprovals = frappe.db.sql("""select count(*) as pending_approvals from `tabApprovals` where owner = '{0}' and status = 'Draft';""".format(userid), as_dict = True)
	return getPendingApprovals

def getOverDueTask(userid):
	getOverTask = frappe.db.sql("""select count(*) as overdue_tasks from `tabMy Task Allocation` where owner = '{0}' and status = 'Overdue';""".format(userid), as_dict=True)
	return getOverTask

def get_columns(filters):
	cols = [
			{
				"fieldname": "name",
				"label": _("Name"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "pending_approval",
				"label": _("Pending Approvals"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "overdue_task",
				"label": _("Total Overdue Task"),
				"fieldtype": "Data",
				"width": "200"
			},
		]
	return cols
	
