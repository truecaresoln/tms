# Copyright (c) 2022, RSA and contributors
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
	month_name = today.strftime("%B")
	
	
	if start_date:
		first_date = start_date
	else:
		first_date = get_first_date_of_current_month(year,month)
		
	if end_date:
		last_date = end_date
	else:
		last_date = get_last_date_of_month(year, month)	
	
	data = []
	
	getBD = getBDPersons()
	for rec1 in getBD:
		total_business = 0
		userid = rec1.user_id
		empid = rec1.name
		employee_name = rec1.employee_name
		
		getTargetBusiness = getTargetedBusiness(empid,month_name,year)
		
		for rec in getTargetBusiness:
			row = {}
			row['bd_person'] = rec.bd_person_name
			row['month'] = rec.month
			row['year'] = rec.year
			row['total_business_in_inr'] = rec.total_business_in_inr
			row['monthly_target'] = rec.targeted_amount
			row['remaining_target'] = rec.targeted_amount-rec.total_business_in_inr
			
			data.append(row)	
	
	return data

def get_last_date_of_month(year, month):
	if month == 12:
		last_date = datetime(year, month, 31)
	else:
		last_date = datetime(year, month + 1, 1) + timedelta(days=-1)
	
	return last_date.strftime("%Y-%m-%d")

def get_first_date_of_current_month(year, month):
	first_date = datetime(year, month, 1)
	return first_date.strftime("%Y-%m-%d")

def getBDPersons():
	
	dataEmployee  = frappe.db.sql("""select name,user_id,employee_name from `tabEmployee` te 
	where te.status = 'Active' and te.department in ('Business Development - THS','Marketing & Sales - THS');""", as_dict = True)
	
	return dataEmployee

def getTargetedBusiness(empid,month,year):	
	dataTargetedBusiness = frappe.db.sql("""select tbmb.name,tbmb.bd_person_name,
		tbmb.total_business_in_inr,tbmb.`month`,tbmb.year,tbmb.targeted_amount,
		tbmb.pending_target
		from `tabBD Monthly Business` tbmb 
		left join `tabMonthly Distribution` tmd on tbmb.bd_person = tmd.employee
		where tbmb.`month` = '{1}' 
		and tbmb.year='{2}' and tbmb.bd_person = '{0}';""".format(empid,month,year),as_dict = True)
			
	return dataTargetedBusiness

def get_columns(filters):
	cols = [
			{
				"fieldname": "bd_person",
				"label": _("BD Person Name"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "month",
				"label": _("Month"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "year",
				"label": _("Year"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "total_business_in_inr",
				"label": _("Current Month Target Achieve Till Date"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "monthly_target",
				"label": _("Current Month Target"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "remaining_target",
				"label": _("Current Month Remaining Target"),
				"fieldtype": "Data",
				"width": "200"
			},				
		]
	return cols	
