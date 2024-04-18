# Copyright (c) 2023, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe
from datetime import date, datetime, timedelta


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	start_date = filters.get("from_date")
	end_date = filters.get("to_date")
	
	today = datetime.today()
	year = today.year
	month = today.month
	
	data = []
	
	getStageData = get_deal_stage()
	
	for rec in getStageData:
		row = {}
		if rec.stage_name != 'Call Scheduled':
			row['activity'] = rec.stage_name
			
			dataBD = frappe.db.sql("""select employee_name,user_id from `tabEmployee` 
				where department in ('Marketing & Sales - THS','Business Development - THS') 
				and status = 'Active';""", as_dict = True)
			
			for recbd in dataBD:
				dealsData = deals_data(recbd.user_id,rec.stage_name)
				
				for recdeals in dealsData:
					row[recbd.employee_name] = recdeals.deal_name
		
		data.append(row)
	
	return data

def get_deal_stage():
	getStageData = frappe.db.sql("""Select stage_name FROM `tabDeal Stage` where status = 'Active';""", as_dict = True)
	
	return getStageData

def deals_data(user_id,stage):
	
	getDealsData = frappe.db.sql("""select deal_name,associated_contact from `tabDeals` where deal_stage = '{1}' and date(close_date) > (NOW() - INTERVAL 30 DAY) and owner = '{0}';""".format(user_id,stage), as_dict = True)
	
	return getDealsData
	
def get_columns(filters):
	cols = []
	cols=[
			{
				"fieldname": "activity",
				"label": _("Activity"),
				"fieldtype": "Data",
				"width": "250"
			},
		]
	
	dataBD = frappe.db.sql("""select employee_name,user_id from `tabEmployee` 
		where department in ('Marketing & Sales - THS','Business Development - THS') 
		and status = 'Active';""", as_dict = True)
	for rec1 in dataBD:
		row = {}
		row["fieldname"] = rec1.employee_name
		row["label"] = rec1.employee_name
		row["fieldtype"] = "Data"
		cols.append(row)
		
	return cols	
