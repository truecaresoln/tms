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
	project_category = filters.get("project_category")
	team = filters.get("team")
	
	if project_category:
		proj_cat = " and viatris_project_category = '%s'" %project_category
	else:
		proj_cat = ""
		
	if team:
		teams = " and viatris_team = '%s'" %team
	else:
		teams = ""			
	
	chart = {}
	label = []
	datasets1 = []
	
	if not data:
		data = []
	
	dt = frappe.db.sql("""select viatris_project_category ,count(*) as project_counts from `tabProject` 
			WHERE customer = 'Viatris Centre of Excellence'
			and project_current_status not in ('Cancelled') and viatris_team != '' 
			and expected_start_date BETWEEN '{1}' and '{2}' {0} {3}
			GROUP BY viatris_project_category""".format(proj_cat,from_date,to_date,teams), as_dict=True)
	
	for d in dt:
		if d.viatris_project_category:
			label.append(d.viatris_project_category)
		else:
			a = "Category not defined"
			label.append(a)	
		datasets1.append(d.project_counts)
			
	chart = {
			"data": {
				'labels': label,
				'datasets': [{'name': 'Total Projects','values': datasets1}]
				}
	}
	chart["type"] = "bar"
	chart["colors"] = ["#87CEEB"]
	return chart	

def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	project_category = filters.get("project_category")
	team = filters.get("team")
	
	if project_category:
		proj_cat = " and viatris_project_category = '%s'" %project_category
	else:
		proj_cat = ""
		
	if team:
		teams = " and viatris_team = '%s'" %team
	else:
		teams = ""				
	
	data = []
	
	data1 = frappe.db.sql("""select viatris_project_category ,count(*) as project_counts from `tabProject` 
			WHERE customer = 'Viatris Centre of Excellence'
			and project_current_status not in ('Cancelled') and viatris_team != '' 
			and expected_start_date BETWEEN '{1}' and '{2}' {0} {3}
			GROUP BY viatris_project_category""".format(proj_cat,from_date,to_date,teams), as_dict=True)
	
	for rec1 in data1:
		row={}
		
		if rec1.viatris_project_category:
			row['viatris_project_category'] = rec1.viatris_project_category
		else:
			row['viatris_project_category'] = 'Category not defined'	
		row['project_count'] = rec1.project_counts
		data.append(row)
	
	return data

def get_columns(filters):
	cols = [
			{
				"fieldname": "viatris_project_category",
				"label": _("Project Category"),
				"fieldtype": "Data",
				"width": "400"
			},
			{
				"fieldname": "project_count",
				"label": _("Project Count"),
				"fieldtype": "Float",
				"width": "300"
			},
	]
	
	return cols
	
