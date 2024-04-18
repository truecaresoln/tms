# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
from collections import Counter
from datetime import datetime
from datetime import date
from forex_python.converter import CurrencyRates
import math
from dateutil.relativedelta import relativedelta

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data

def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	
	data = []
	
	data1 = frappe.db.sql("""select name,employee_name,status,relieving_date from `tabEmployee`;""", as_dict = True)
	
	for rec1 in data1:
		row = {}
		row['emp_id'] = rec1.name
		row['emp_name'] = rec1.employee_name
		row['status'] = rec1.status
		row['relieving_date'] = rec1.relieving_date
		
		dataCasualLeave = frappe.db.sql("""select employee,employee_name ,leave_type,
		sum(leaves) as leaves from `tabLeave Ledger Entry` where transaction_type ='Leave Application' 
		and employee = '{0}' and from_date between '{1}' 
		and '{2}' GROUP BY employee,leave_type order by 1,2""".format(rec1.name,from_date,to_date), as_dict = True)
		for rec2 in dataCasualLeave:
			if rec2.leave_type == 'Casual Leave':
				row['cl_taken'] = abs(rec2.leaves)
				
			elif rec2.leave_type == 'Sick Leave':
				row['sl_taken']	= abs(rec2.leaves)
				
			elif rec2.leave_type == 'Earned Leave':
				row['el_taken']	= abs(rec2.leaves)
				
			elif rec2.leave_type == 'Contractual':
				row['contractual_taken'] = abs(rec2.leaves)
				
			elif rec2.leave_type == 'Probation':
				row['probation_taken'] = abs(rec2.leaves)
				
			elif rec2.leave_type == 'Compensatory off':
				row['compoff_taken'] = abs(rec2.leaves)
				
			elif rec2.leave_type == 'Leave Without Pay':
				row['lwp_taken']	= abs(rec2.leaves)					
		
		data.append(row)
		
	return data

def get_columns(filters):
	cols = [
			{
				"fieldname": "emp_id",
				"label": _("EMP ID"),
				"fieldtype": "Data",
				"width": "100"
			},
			{
				"fieldname": "emp_name",
				"label": _("Employee Name"),
				"fieldtype": "Data",
				"width": "300"
			},
			{
				"fieldname": "status",
				"label": _("Status"),
				"fieldtype": "Data",
				"width": "80"
			},
			{
				"fieldname": "relieving_date",
				"label": _("Relieving Date"),
				"fieldtype": "Date",
				"width": "80"
			},
			{
				"fieldname": "cl_taken",
				"label": _("CL Taken"),
				"fieldtype": "float",
				"width": "80"
			},
			{
				"fieldname": "sl_taken",
				"label": _("SL Taken"),
				"fieldtype": "float",
				"width": "80"
			},
			{
				"fieldname": "el_taken",
				"label": _("EL Taken"),
				"fieldtype": "float",
				"width": "80"
			},
			{
				"fieldname": "compoff_taken",
				"label": _("Comp Off Taken"),
				"fieldtype": "float",
				"width": "80"
			},
			{
				"fieldname": "contractual_taken",
				"label": _("Contractual Taken"),
				"fieldtype": "float",
				"width": "80"
			},
			{
				"fieldname": "probation_taken",
				"label": _("Probation Taken"),
				"fieldtype": "float",
				"width": "80"
			},
			{
				"fieldname": "lwp_taken",
				"label": _("LWP Taken"),
				"fieldtype": "float",
				"width": "80"
			},
		]
	
	return cols	
		
		
