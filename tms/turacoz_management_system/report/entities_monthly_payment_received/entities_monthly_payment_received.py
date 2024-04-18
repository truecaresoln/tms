# Copyright (c) 2024, RSA and contributors
# For license information, please see license.txt

import frappe
import calendar
from datetime import datetime, timedelta

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data

def get_data(filters):
	start_date = filters.get('from_date')
	end_date = filters.get('to_date')
	startDate = datetime.strptime(start_date, "%Y-%m-%d")
	endDate = datetime.strptime(end_date, "%Y-%m-%d")
	
	data = []
	addDays = timedelta(days=31)
	while startDate <= endDate:
		row = {}
		months = startDate.month
		years = startDate.year
		months_name = calendar.month_name[months]
		
		row['months'] = months_name+'-'+str(years)
		row['ths_payment_received'] = get_ths_payment_received(months,years)
		row['tspl_payment_received'] = get_tspl_payment_received(months,years)
		row['tbv_payment_received'] = get_tbv_payment_received(months,years)
		
		startDate += addDays
		
		data.append(row)
	return data	
	
def get_columns(filters):	
	cols =[
			{
				"fieldname": "months",
				"label": ("Months"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "ths_payment_received",
				"label": ("THS Payment Received"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "tspl_payment_received",
				"label": ("TSPL Payment Received"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "tbv_payment_received",
				"label": ("TBV Payment Received"),
				"fieldtype": "Data",
				"width": "250"
			},
		]
	
	return cols

def get_ths_payment_received(month,year):
	
	ths_data = frappe.db.sql("""SELECT sum(ROUND((tpr.grand_total*tcer.rate_in_inr),2)) as amount_in_inr from `tabPayment Request` tpr
		left join `tabCurrency Exchange Rate` tcer on tpr.currency = tcer.name
		WHERE tpr.company = 'Turacoz Healthcare Solutions Pvt Ltd' 
		and YEAR(tpr.payment_date) = '{1}' 
		AND MONTH(tpr.payment_date) = '{0}';""".format(month,year), as_dict = True)
	
	if ths_data[0]['amount_in_inr']:
		ths_total_month_amount = ths_data[0]['amount_in_inr']
	else:
		ths_total_month_amount = 0	
	
	return ths_total_month_amount

def get_tspl_payment_received(month,year):
	
	tspl_data = frappe.db.sql("""SELECT sum(ROUND((tpr.grand_total*tcer.rate_in_inr),2)) as amount_in_inr from `tabPayment Request` tpr
		left join `tabCurrency Exchange Rate` tcer on tpr.currency = tcer.name
		WHERE tpr.company = 'Turacoz Solutions PTE Ltd.' 
		and YEAR(tpr.payment_date) = '{1}' 
		AND MONTH(tpr.payment_date) = '{0}';""".format(month,year), as_dict = True)
	if tspl_data[0]['amount_in_inr']:
		tspl_total_month_amount = tspl_data[0]['amount_in_inr']
	else:
		tspl_total_month_amount = 0	
	
	return tspl_total_month_amount

def get_tbv_payment_received(month,year):
	
	tbv_data = frappe.db.sql("""SELECT sum(ROUND((tpr.grand_total*tcer.rate_in_inr),2)) as amount_in_inr from `tabPayment Request` tpr
		left join `tabCurrency Exchange Rate` tcer on tpr.currency = tcer.name
		WHERE tpr.company = 'Turacoz B.V.' 
		and YEAR(tpr.payment_date) = '{1}' 
		AND MONTH(tpr.payment_date) = '{0}';""".format(month,year), as_dict = True)
	if tbv_data[0]['amount_in_inr']:
		tbv_total_month_amount = tbv_data[0]['amount_in_inr']
	else:
		tbv_total_month_amount = 0	
	
	return tbv_total_month_amount
	
	

	
