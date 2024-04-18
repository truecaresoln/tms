# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
from collections import Counter
from datetime import date
# import datetime
from forex_python.converter import CurrencyRates
import math
from dateutil.relativedelta import relativedelta

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data()
	return columns, data

def get_data():
	data = []
	row = {}
	
	todays_date = date.today()
	three_months_date = todays_date + relativedelta(months=+3)
		
	data1 = frappe.db.sql("""SELECT name,status,start_date,end_date,
			contract_document_type,party_name,party_user 
			from `tabContract` where status in ('Active') 
			and end_date is not NULL and end_date BETWEEN '{0}' and '{1}'""".format(todays_date,three_months_date), as_dict = True)
	for rec in data1:
		row = {}
		row["customer"] = rec.party_name
		row["status"] = rec.status
		row["contract_type"] = rec.contract_document_type
		row["start_date"] = rec.start_date
		row["end_date"] = rec.end_date
		row["party_user"] = rec.party_user
		
		data.append(row)
		
	return data
	
def get_columns():
	cols = [
			{
				"fieldname": "customer",
				"label": _("Client"),
				"fieldtype": "Data",
				"width": "300"
			},
			{
				"fieldname": "status",
				"label": _("Current Status"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "contract_type",
				"label": _("Contract Type"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "start_date",
				"label": _("Start Date"),
				"fieldtype": "Date",
				"width": "150"
			},
			{
				"fieldname": "end_date",
				"label": _("End Date"),
				"fieldtype": "Date",
				"width": "150"
			},
			{
				"fieldname": "party_user",
				"label": _("Client User"),
				"fieldtype": "Data",
				"width": "250"
			},
		]
	
	return cols	
