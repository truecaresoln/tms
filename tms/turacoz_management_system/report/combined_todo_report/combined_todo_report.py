# Copyright (c) 2024, RSA and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	department = filters.get('department')
	owner = filters.get('allocate_to')
	status = filters.get('status')
	
	new_department=''
	new_owner=''
	new_status=''
	
	if department:
		new_department = "and tu.department='%s'" %department
	
	if owner:
		new_owner = "and tu.name='%s'" %owner
	
	if status:
		new_status = "ttd.status in ('%s')" %status
	else:
		new_status = "ttd.status in ('Open','Overdue')"
		
	data = frappe.db.sql("""select tu.department,ttd.name,ttd.description,ttd.reference_name,ttd.allocated_to,ttd.allocated_to_full_name,ttd.start_date,ttd.`date` as 'due_date',ttd.status 
			from tabToDo ttd 
			left join tabUser tu on ttd.allocated_to = tu.name 
			where {0} {1} {2} and ttd.allocated_to not in ('') and ttd.description not in ('Calls and Co-ordinations','Medical Services - Calls','Medical Services - Training & Development','Medical Services - Trainings','Calls','Business Development - Others','Business Development - ERP training','Business Development - Internal calls or discussion',
'Project Management - Other Tasks','Project Management - ERP management','Project Management - Internal Calls and Coordination',
'Project Management - Client communication and coordination','Project Management - Database Management','Project Management - Project Planning & Resourcing',
'Project Management - Client Coordination','Project Management - Training related','Business Development - Mailing','Project Management - Invoicing and PFR related',
'Project Management - Project delivery','Project Management - Internal Documents Review','Administration--ERP Update','Administration--HubSpot Update')
order by ttd.allocated_to_full_name,ttd.`date` 
 """.format(new_status,new_department,new_owner),as_dict=True)
	
	return data

def get_columns(filters):
			cols=[
			{
				"fieldname": "name",
				"label": _("ToDO"),
				"fieldtype": "Link",
				"options": "ToDo",
				"width": "200"
			},
			{
				"fieldname": "description",
				"label": _("Description"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "department",
				"label": _("Department"),
				"fieldtype": "Data",
				"width": "100"
			},
			{
				"fieldname": "reference_name",
				"label": _("DMS Alert Name"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "allocated_to_full_name",
				"label": _("Employee Name"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "start_date",
				"label": _("Start Date"),
				"fieldtype": "Date",
				"width": "100"
			},
			{
				"fieldname": "due_date",
				"label": _("Due Date"),
				"fieldtype": "Date",
				"width": "100"
			},
			{
				"fieldname": "status",
				"label": _("Status"),
				"fieldtype": "Data",
				"width": "80"
			}

		]
			return cols
