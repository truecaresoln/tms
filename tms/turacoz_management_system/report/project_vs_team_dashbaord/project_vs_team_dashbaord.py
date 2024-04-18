# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

# import frappe

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
	team = filters.get("team")
	
	if team:
		team = " and viatris_team = '%s'" %team
	else:
		team = ""	
	
	data = []
	
	data1 = frappe.db.sql("""select viatris_team ,count(*) as project_counts from `tabProject` 
		WHERE customer = 'Viatris Centre of Excellence'
		and project_current_status not in ('Cancelled') and viatris_team != ''
		and expected_start_date BETWEEN '{0}' and '{1}' {2}
		GROUP BY viatris_team""".format(from_date, to_date, team), as_dict = True)
		
	for rec1 in data1:
		row = {}
		row['team'] = rec1.viatris_team
		row['project_count'] = rec1.project_counts
	
		data.append(row)
	
	return data

def get_columns(filters):
	cols = [
			{
				"fieldname": "team",
				"label": _("Team"),
				"fieldtype": "Data",
				"width": "400"
			},
			{
				"fieldname": "project_count",
				"label": _("Project Count"),
				"fieldtype": "float",
				"width": "400"
			},
		]
	
	return cols
	