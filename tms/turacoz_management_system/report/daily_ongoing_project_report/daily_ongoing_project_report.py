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
	
	data1 = frappe.db.sql("""select tp.name,tp.customer,tp.manager_name,
			tp.project_current_status,tp.total_planned_hours,tp.actual_time,
			tp.expected_end_date from `tabProject` tp 
			where tp.project_current_status in ('Ongoing','Yet to Start','On Hold','Under Client Review','Under Journal Review') 
			and tp.customer not in ('Viatris Centre of Excellence','Turacoz Healthcare Solution Pvt Ltd','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd') and tp.project_type ='External' ORDER BY tp.project_current_status DESC,tp.expected_end_date;;""", as_dict = True)
	
	for rec in data1:
		row = {}
		
		dataGetTeam = frappe.db.sql("""select GROUP_CONCAT( DISTINCT allocated_to_full_name) as team from `tabToDo` where project = '{0}'  and `role` = 'Drafter' GROUP by project;""".format(rec.name), as_dict = True)		
		if dataGetTeam:
			team = dataGetTeam[0]['team']
		else:
			team = ''
			
		dataGetDeliverable = frappe.db.sql("""select GROUP_CONCAT(tpd.deliverable) as deliverable from `tabProject Deliverable` tpd where tpd.parent = '{0}'""".format(rec.name), as_dict=True)	
		if dataGetDeliverable:
			fn_deliverable = dataGetDeliverable[0]['deliverable']
		else:
			fn_deliverable = ''
			
		dataGetTodayTimeConsumed = frappe.db.sql("""select if(SUM(ttd.hours),SUM(ttd.hours),0) as today_consumed_hours from `tabTimesheet` tt
			left join `tabTimesheet Detail` ttd on tt.name=ttd.parent 
			where tt.start_date = DATE_SUB(CURDATE(),INTERVAL 1 DAY) 
			and ttd.project='{0}';""".format(rec.name), as_dict = True)
		if dataGetTodayTimeConsumed[0]['today_consumed_hours'] == 0:
			fn_today_hours = 0.0
		else:
			fn_today_hours = dataGetTodayTimeConsumed[0]['today_consumed_hours']	
		
		row["project_code"] = rec.name
		row["client"] = rec.customer
		row["writer"] = team
		row["project_manager"] = rec.manager_name
		row["deliverable"] = fn_deliverable
		row["status"] = rec.project_current_status
		row["expected_completion_time"] = rec.total_planned_hours
		row["time_consumed"] = rec.actual_time
		row["today_time_consumed"] = fn_today_hours
		row["deadlline_date"] = rec.expected_end_date
		row["project_link"] = "<a href='http://erp.turacoz.com/app/project/'"+rec.name+">http://erp.turacoz.com/app/project/"+rec.name+"</a>"
			
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
				"fieldname": "client",
				"label": _("Client"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "deliverable",
				"label": _("Deliverable Type"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "project_manager",
				"label": _("Project Manager"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "writer",
				"label": _("Writer"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "status",
				"label": _("Status"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "expected_completion_time",
				"label": _("Expected completion Time"),
				"fieldtype": "Float",
				"width": "200"
			},
			{
				"fieldname": "time_consumed",
				"label": _("Time consumed"),
				"fieldtype": "Float",
				"width": "200"
			},
			{
				"fieldname": "today_time_consumed",
				"label": _("Today Time consumed"),
				"fieldtype": "Float",
				"width": "200"
			},
			{
				"fieldname": "deadlline_date",
				"label": _("Deadline Date"),
				"fieldtype": "Date",
				"width": "150"
			},
			{
				"fieldname": "project_link",
				"label": _("Project link to ERP"),
				"fieldtype": "Data",
				"width": "300"
			},
		]
	
	return cols