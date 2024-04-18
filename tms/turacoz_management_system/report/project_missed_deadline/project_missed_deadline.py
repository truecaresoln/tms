# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
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
	
	getOnHoldData = frappe.db.sql("""select name,customer,manager_name,project_current_status,
		expected_hour,expected_end_date,delayed_reason,on_hold_reason
		from `tabProject` tp 
		WHERE tp.customer not in ('Viatris Centre of Excellence','Turacoz Healthcare Solution Pvt Ltd',
		'Turacoz Solutions LLC','Turacoz Solutions PTE Ltd')
		and tp.project_current_status in ('On Hold')
		and project_type = 'External';""", as_dict = True)
	for rec1 in getOnHoldData:
		row1 = {}
		
		row1["project_code"] = rec1.name
		row1["client"] = rec1.customer
		row1["project_manager"] = rec1.manager_name
		row1["status"] = "<a style='color:red;'>"+ rec1.project_current_status +"</a>"
		row1["expected_time"] = rec1.expected_hour
		row1["deadline_date"] = rec1.expected_end_date
		row1["missing_deadline_reason"] = rec1.on_hold_reason
		row1["project_link"] = "<a style='color:blue;' href='http://erp.turacoz.com/app/project/'"+rec1.name+">http://erp.turacoz.com/app/project/"+rec1.name+"</a>"
		
		dataGetOnHoldTeam = frappe.db.sql("""select GROUP_CONCAT( DISTINCT allocated_to_full_name) as writer from `tabToDo` where project = '{0}' and role='Drafter' and status ='Open' GROUP by project;""".format(rec1.name), as_dict = True)		
		if dataGetOnHoldTeam:
			team_h = dataGetOnHoldTeam[0]['writer']
		else:
			team_h = ''
			
		dataGetOnHoldDeliverable = frappe.db.sql("""select GROUP_CONCAT(tpd.deliverable) as deliverable from `tabProject Deliverable` tpd where tpd.parent = '{0}'""".format(rec1.name), as_dict=True)	
		if dataGetOnHoldDeliverable:
			fn_deliverable_h = dataGetOnHoldDeliverable[0]['deliverable']
		else:
			fn_deliverable_h = ''
			
		row1["writer"] = team_h
		row1["deliverable"] = fn_deliverable_h	
		
		data.append(row1)
	
	getData = frappe.db.sql("""select name,customer,manager_name,project_current_status,expected_hour,expected_end_date,delayed_reason
		from `tabProject` tp WHERE tp.customer not in ('Viatris Centre of Excellence','Turacoz Healthcare Solution Pvt Ltd',
		'Turacoz Solutions LLC','Turacoz Solutions PTE Ltd')
		and tp.project_current_status not in ('Completed', 'Completed Technically', 'Cancelled','On Hold')
		and tp.expected_end_date < NOW() and project_type = 'External';""", as_dict = True)
	for rec in getData:
		row = {}
		
		row["project_code"] = rec.name
		row["client"] = rec.customer
		row["project_manager"] = rec.manager_name
		row["status"] = rec.project_current_status
		row["expected_time"] = rec.expected_hour
		row["deadline_date"] = rec.expected_end_date
		row["missing_deadline_reason"] = rec.delayed_reason
		row["project_link"] = "<a style='color:blue;' href='http://erp.turacoz.com/app/project/'"+rec.name+">http://erp.turacoz.com/app/project/"+rec.name+"</a>"
		
		dataGetTeam = frappe.db.sql("""select GROUP_CONCAT( DISTINCT allocated_to_full_name) as writer from `tabToDo` where project = '{0}' and role='Drafter' and status ='Open' GROUP by project;""".format(rec.name), as_dict = True)		
		if dataGetTeam:
			team = dataGetTeam[0]['writer']
		else:
			team = ''
			
		dataGetDeliverable = frappe.db.sql("""select GROUP_CONCAT(tpd.deliverable) as deliverable from `tabProject Deliverable` tpd where tpd.parent = '{0}'""".format(rec.name), as_dict=True)	
		if dataGetDeliverable:
			fn_deliverable = dataGetDeliverable[0]['deliverable']
		else:
			fn_deliverable = ''
			
		row["writer"] = team
		row["deliverable"] = fn_deliverable	
		
		data.append(row)
		
	return data

def get_columns(filters):
	cols = []
	cols=[
			{
				"fieldname": "project_code",
				"label": _("Project Code"),
				"fieldtype": "Link",
				"options": "Project",
				"width": "150"
			},
			{
				"fieldname": "client",
				"label": _("Client"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "deliverable",
				"label": _("Deliverable"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "project_manager",
				"label": _("Project Manager"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "writer",
				"label": _("Writer"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "status",
				"label": _("Status"),
				"fieldtype": "Data",
				"width": "120"
			},
			{
				"fieldname": "expected_time",
				"label": _("Expected completion time"),
				"fieldtype": "Float",
				"width": "120"
			},
			{
				"fieldname": "deadline_date",
				"label": _("Project completion date (expected)"),
				"fieldtype": "Date",
				"width": "150"
			},
			{
				"fieldname": "missing_deadline_reason",
				"label": _("Reason for missing deadline/On Hold"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "project_link",
				"label": _("Project link to ERP"),
				"fieldtype": "Data",
				"width": "250"
			},
		]
	return cols
	