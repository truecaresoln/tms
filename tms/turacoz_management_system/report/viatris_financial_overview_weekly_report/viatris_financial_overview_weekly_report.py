# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
from collections import Counter
from datetime import date
import calendar
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
	firstDateofCurrentMonth = date.today().replace(day=1)
	
	monthlastDay = calendar.monthrange(todays_date.year, todays_date.month)[1]
	
	lastDateofCurrentMonth = date.today().replace(day=monthlastDay)

	year = todays_date.year
	month_name = todays_date.strftime("%B")
	last_month = date.today() - relativedelta(months=1)
	last_month_name = last_month.strftime("%B")
	last_month_year = last_month.year
	
	getIONRequests = frappe.db.sql("""select count(*) number_of_ions, 
		SUM(project_cost) as total_request_cost from `tabION Number` 
		WHERE ion_request_date BETWEEN '{0}' and '{1}';""".format(firstDateofCurrentMonth,lastDateofCurrentMonth), as_dict = True)
	
	if getIONRequests:
		row["particular"] = "Total ION Request Sent of "+ str(month_name) +' '+str(year)
		row["viatris"] = getIONRequests[0]['number_of_ions']
		
		
		data.append(row)
		row1 = {}
		row1["particular"] = "Total Amount of ION Request Sent of "+ str(month_name) +' '+str(year)
		row1["viatris"] = getIONRequests[0]['total_request_cost']
		
		data.append(row1)
	
	return data
	
def get_columns():
	cols = [
			{
				"fieldname": "particular",
				"label": _("Particular"),
				"fieldtype": "Data",
				"width": "400"
			},
			{
				"fieldname": "viatris",
				"label": _("Viatris Centre of Excellence"),
				"fieldtype": "Data",
				"width": "250"
			},
		]
	return cols	
	
	
	
	