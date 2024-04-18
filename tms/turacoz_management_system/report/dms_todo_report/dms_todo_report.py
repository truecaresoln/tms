# Copyright (c) 2024, RSA and contributors
# For license information, please see license.txt

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
	owner = filters.get('owner')
	status = filters.get('status')
	
	new_department=''
	new_owner=''
	new_status=''
	
	if department:
		new_department = "and tdas.department='%s'" %department
	
	if owner:
		new_owner = "and ttd.owner='%s'" %owner
	
	if status:
		new_status = "and ttd.status='%s'" %status
	else:
		new_status = "and ttd.status in ('Open','Overdue')"
		
	data = frappe.db.sql("""select tdas.department,ttd.name,ttd.description,ttd.reference_name,ttd.owner,ttd.allocated_to_full_name,ttd.start_date,ttd.`date` as 'due_date',ttd.status 
				from tabToDo ttd 
				left join `tabDMS ALERT SYSTEM` tdas on ttd.reference_name = tdas.name 
				where ttd.reference_type ='DMS ALERT SYSTEM' {0} {1} {2}""".format(new_department,new_owner,new_status),as_dict=True)
	
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
