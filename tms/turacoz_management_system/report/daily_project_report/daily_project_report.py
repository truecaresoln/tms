# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
from collections import Counter
from datetime import datetime
from datetime import date
# import datetime
from forex_python.converter import CurrencyRates
import math
from dateutil.relativedelta import relativedelta
# import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data

def get_data(filters):
	
	data = []
	
	data1 = frappe.db.sql("""select tp.name,tp.tms_project_code,tp.bd_name,tp.manager_name,
				tp.customer,tp.contact_person,tp.project_title,tp.project_current_status,tp.expected_start_date,tp.project_title,
				tp.expected_end_date,tp.total_planned_hours,GROUP_CONCAT("'",tpd.name,"'") as delvirable_str from `tabProject` tp
				left join `tabProject Update Data` tpd on tp.name = tpd.parent
				where tp.project_current_status not in ('Completed','Completed Technically','Cancelled') and tp.project_type ='External'
				and tp.customer not in ('Viatris Centre of Excellence','Turacoz Healthcare Solution Pvt Ltd','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd')
				group by tp.name order by project_current_status;""", as_dict = True)
		
	for rec in data1:
		if rec.delvirable_str:
			del_str = rec.delvirable_str
			final_str = " and tpdd.name not in (%s)" %del_str
					
		else:
			del_str = ""
			final_str = ""
		
		dataGetTeam = frappe.db.sql("""select GROUP_CONCAT( DISTINCT allocated_to_full_name) as team from `tabToDo` where project = '{0}' and status ='Open' GROUP by project;""".format(rec.name), as_dict = True)		
		if dataGetTeam:
			team = dataGetTeam[0]['team']
		else:
			team = ''
					
		data2 = frappe.db.sql("""select distinct tpdd.idx,tpdd.name,tpdd.module as  proposed_module,tpdd.deliverable,tpdd.proposed_date,tpud.start_date,tpdd.proposed_end_date,tpud.end_date,
				tpdd.remark,tpud.internal_remarks from `tabProject Proposed Date Data` tpdd
				left join `tabProject Update Data` tpud on tpdd.module=tpud.module and tpdd.deliverable=tpud.deliverable and tpdd.parent=tpud.parent
				where tpdd.parent='{0}' and tpdd.deliverable not in ('General Update') and tpud.end_date is NULL  order by tpdd.idx;""".format(rec.name), as_dict = True)	
		row = {}
		row["project_code"] = rec.name
		row["project_title"] = rec.project_title
		row["project_manager"] = rec.manager_name
		row["client"] = rec.customer
		row["client_poc"] = rec.contact_person
		row["status"] = rec.project_current_status
		row["writer"] = team
		row["expected_completion_time"] = rec.total_planned_hours
		row["project_link"] = "<a href='http://erp.turacoz.com/app/project/'"+rec.name+">http://erp.turacoz.com/app/project/"+rec.name+"</a>"
			
		if data2 != '':
			i = 1
			for deldata in data2:
				if i== 1:
					row["module"] = deldata.proposed_module
					row["document_deliverable"] = deldata.deliverable
					if deldata.proposed_date:
						row["planned_start_date"] = deldata.proposed_date
					if deldata.proposed_end_date:
						row["deadline_date"] = deldata.proposed_end_date
					if deldata.start_date:
						row["start_date"] = deldata.start_date
					if deldata.end_date:
						row["end_date"] = deldata.end_date
					row["remark"] = deldata.remark 
					row["reason_for_delay"] = deldata.internal_remarks
					data.append(row)	
					i+=1
				else:
					row1 = {}
					row1["module"] = deldata.proposed_module
					row1["document_deliverable"] = deldata.deliverable
					if deldata.proposed_date:
						row1["planned_start_date"] = deldata.proposed_date
					if deldata.proposed_end_date:
						row1["deadline_date"] = deldata.proposed_end_date
					if deldata.start_date:
						row1["start_date"] = deldata.start_date
					if deldata.end_date:
						row1["end_date"] = deldata.end_date
					row1["remark"] = deldata.remark
					row1["reason_for_delay"] = deldata.internal_remarks
					data.append(row1)
	
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
				"fieldname": "client",
				"label": _("Client"),
				"fieldtype": "Data",
				"width": "300"
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
				"width": "150"
			},
			{
				"fieldname": "expected_completion_time",
				"label": _("Expected Completion Time"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "module",
				"label": _("Module"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "document_deliverable",
				"label": _("Document/Deliverable"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "planned_start_date",
				"label": _("Planned Start Date"),
				"fieldtype": "Date",
				"width": "200"
			},
			{
				"fieldname": "deadline_date",
				"label": _("Deadline Date"),
				"fieldtype": "Date",
				"width": "200"
			},
			{
				"fieldname": "reason_for_delay",
				"label": _("Reason for Missing Deadline"),
				"fieldtype": "Small Text"
			},
			{
				"fieldname": "project_link",
				"label": _("Project link to ERP"),
				"fieldtype": "Data",
				"width": "300"
			},
		]
	return cols