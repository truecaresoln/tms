# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe
import datetime

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data

def get_data(filters):
	
	data = []
	
	getProjectsData = frappe.db.sql("""select tp.name,tp.customer,tp.project_current_status,tp.manager_name,
		tp.bd_name,tp.contact_person,tp.project_scope,tp.turacoz_end_date,tc.first_name,tc.middle_name,tc.last_name from `tabProject` tp
		left join `tabContact` tc on tp.contact_person = tc.name
		left join `tabSales Invoice` tsi on tp.name = tsi.project
		where tp.project_current_status in ('Completed Technically')
		and tp.customer not in ('Turacoz Healthcare Solution Pvt Ltd','Turacoz Solutions LLC',
		'Turacoz Solutions PTE Ltd','Viatris Centre of Excellence') and tp.project_type = 'External';""", as_dict = True)
	
	for rec in getProjectsData:
		
		if rec.first_name:
			first_name = rec.first_name
		else:
			first_name = ''
			
		if rec.middle_name:
			middle_name = rec.middle_name
		else:
			middle_name = ''
			
		if rec.last_name:
			last_name = rec.last_name
		else:
			last_name = ''
			
		final_contact_person_name = first_name+' '+middle_name+' '+last_name						
		row = {}
		
		row["project_code"] = rec.name
		row["status"] = "Financially Not Closed"
		row["client"] = rec.customer
		row["client_poc"] = final_contact_person_name
		row["project_scope"] = rec.project_scope
		row["completed_date"] = rec.turacoz_end_date
		row["project_manager"] = rec.manager_name
		
		financeData = frappe.db.sql("""select name,currency,outstanding_amount from `tabSales Invoice` 
			where project = '{0}' and status not in ('Cancelled','Paid')""".format(rec.name), as_dict = True)
		for rec1 in financeData:
			row["outstanding_amount"] = rec1.outstanding_amount
			row["currency"] = rec1.currency
		
		data.append(row)
		
	return data

def get_columns(filters):	
	cols =[
			{
				"fieldname": "project_code",
				"label": _("Project Code"),
				"fieldtype": "Link",
				"options": "Project",
				"width": "150"
			},
			{
				"fieldname": "status",
				"label": _("Status"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "client",
				"label": _("Client"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "client_poc",
				"label": _("Client PoC"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "project_scope",
				"label": _("Scope of Project"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "completed_date",
				"label": _("Technically Completed Date"),
				"fieldtype": "Date",
				"width": "200"
			},
			{
				"fieldname": "project_manager",
				"label": _("Project Manager"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "outstanding_amount",
				"label": _("Outstanding Amount"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "currency",
				"label": _("Currency"),
				"fieldtype": "Data",
				"width": "80"
			},
		]
	
	return cols