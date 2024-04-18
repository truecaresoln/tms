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
	chart = get_chart_data(data,filters)
	
	return columns, data, None, chart

def get_chart_data(data,filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	
	chart = {}
	label = []
	datasets1 = []
	
	if not data:
		data = []
		
	dt = frappe.db.sql("""select 'ION Requested' as particular,sum(tin.project_cost) as cost FROM `tabION Number` tin 
		where tin.ion_request_date BETWEEN '{0}' and '{1}'
		UNION 
		select 'ION Received' as particular,sum(tinn.project_cost) as cost FROM `tabION Number` tinn 
		where tinn.ion_number is NOT NULL and tinn.ion_request_date BETWEEN '{0}' and '{1}';""".format(from_date,to_date), as_dict=True)
		
	for d in dt:
		label.append(d.particular)
		datasets1.append(d.cost)
			
	chart = {
			"data": {
				'labels': label,
				'datasets': [{'name': 'Total Cost','values': datasets1}]
				}
	}
	chart["type"] = "bar"
	chart["colors"] = ["#3c005a"]
	return chart		

def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	
	data = []
	
	data1 = frappe.db.sql("""select 'ION Requested' as particular,sum(tin.project_cost) as requested_cost FROM `tabION Number` tin 
		where tin.ion_request_date BETWEEN '{0}' and '{1}'
		UNION 
		select 'ION Received' as particular,sum(tinn.project_cost) as ion_received FROM `tabION Number` tinn 
		where tinn.ion_number is NOT NULL and tinn.ion_request_date BETWEEN '{0}' and '{1}';""".format(from_date,to_date), as_dict=True)
	
	for rec in data1:
		row = {}
		row['particular'] = rec.particular
		row['amount'] = rec.requested_cost
		
  # if rec.particular == 'ION Requested':
  # 	row['ion_requested'] = rec.requested_cost
  # 	row['ion_received'] = 0.0
  # elif rec.particular == 'ION Received':
  # 	row['ion_requested'] = 0.0
  # 	row['ion_received'] = rec.requested_cost	
		
		data.append(row)
	data	
	return data	

def get_columns(filters):
	cols = [
			{
				"fieldname": "particular",
				"label": _("particular"),
				"fieldtype": "Data",
				"width": "400"
			},
			{
				"fieldname": "amount",
				"label": _("Amount"),
				"fieldtype": "Float",
				"default": "0.0",
				"width": "400"
			},
   # {
   # 	"fieldname": "ion_requested",
   # 	"label": _("ION Requested"),
   # 	"fieldtype": "Float",
   # 	"default": "0.0",
   # 	"width": "300"
   # },
   # {
   # 	"fieldname": "ion_received",
   # 	"label": _("ION Received"),
   # 	"fieldtype": "Float",
   # 	"default": "0.0",
   # 	"width": "300"
   # },
			
		]
	return cols
		
		
