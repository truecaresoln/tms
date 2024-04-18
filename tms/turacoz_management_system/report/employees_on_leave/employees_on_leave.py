# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe
from collections import Counter

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data

def get_data(filters):
	data =[]
	
	data1 = frappe.db.sql("""select tla.employee_name,te.designation,tla.half_day,tla.first_half_or_second_half,
			tla.from_date,tla.to_date,datediff(tla.to_date,tla.from_date) +1 as leave_days
			from `tabLeave Application` tla
			left join `tabEmployee` te on tla.employee = te.name           
			where tla.workflow_state not in ('Rejected') and CURDATE() BETWEEN tla.from_date and tla.to_date
			order by tla.from_date;""", as_dict = True)
	print(data1)	
	for rec in data1:
		row = {}
		row["employee_name"] = rec.employee_name
		row["designation"] = rec.designation
		if rec.half_day == 0:
			row["half_day_full_day"] = "Full Day"
		else:
			row["half_day_full_day"] = rec.first_half_or_second_half	
		
		data.append(row)
	
	return data	
	
def get_columns(filters):
	cols=[
			{
				"fieldname": "employee_name",
				"label": _("Employee Name"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "designation",
				"label": _("Designation"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "half_day_full_day",
				"label": _("Full Day/Half Day"),
				"fieldtype": "Data",
				"width": "200"
			},
		]
	return cols	
