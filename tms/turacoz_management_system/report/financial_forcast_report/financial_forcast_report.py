# Copyright (c) 2024, RSA and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data

def get_data(filters):
	data = []
	total = 0.0
	forcastData = frappe.db.sql("""SELECT tpr.name,tpr.invoice_date,tpr.due_date,tpr.customer_name,
		tpr.contact_person as client_poc,tp.manager_name,tpr.company,
		tpr.invoice_currency,tpr.net_total,
		(tcer.rate_in_inr * tpr.net_total) as net_total_in_inr,tpr.total_taxes,tpr.grand_total,
		(tcer.rate_in_inr * tpr.grand_total) as grand_total_in_inr
		FROM `tabPayment Request` tpr
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` tcer on tpr.invoice_currency = tcer.name
		WHERE tpr.payment_status in ('Unpaid','Overdue') AND  DATE(tpr.due_date)> DATE_SUB(NOW(), INTERVAL 7 DAY) order by tpr.due_date;""", as_dict = True)
	
	for invoicesData in forcastData:
		row = {}
		row1 ={}
		row['invoice_number'] = invoicesData.name
		row['invoice_date'] = invoicesData.invoice_date
		row['due_date'] = invoicesData.due_date

		dt = invoicesData.due_date
		# given_date = datetime.strptime(dt, '%Y-%m-%d')

		# sevenDayAgo = given_date - timedelta(days=7)
		# sevenDayAgo1 = sevenDayAgo.strftime('%Y-%m-%d')

		# sevenDayAgo = given_date - timedelta(days=7)
		# sevenDayAgo1 = sevenDayAgo.strftime('%Y-%m-%d')

		dtnew = dt.strftime('%d-%m-%Y')
		given_date = datetime.strptime(dtnew,'%d-%m-%Y').date()
		sevenDayAgo = given_date - timedelta(days=7)
		sevenDayAgo1 = sevenDayAgo.strftime('%Y-%m-%d')

		sevenDayAfter = given_date + timedelta(days=7)
		sevenDayAfter1 = sevenDayAfter.strftime('%Y-%m-%d')

		row['ex_from_date'] = sevenDayAgo1
		row['ex_to_date'] = sevenDayAfter1
		row['customer'] = invoicesData.customer_name
		row['client_poc'] = invoicesData.client_poc
		row['project_manager'] = invoicesData.manager_name
		row['invoice_currency'] = invoicesData.invoice_currency
		# row['actual_net_total'] = invoicesData.net_total
		# row['inr_net_total'] = invoicesData.net_total_in_inr
		# row['total_taxes'] = invoicesData.total_taxes
		row['actual_grand_total'] = invoicesData.grand_total
		row['inr_grand_total'] = invoicesData.grand_total_in_inr
		row['turacoz_entity'] = invoicesData.company

		total += invoicesData.grand_total_in_inr


		data.append(row)

	row1['invoice_number'] = 'Total'
	row1['inr_grand_total'] = total
	data.append(row1)

	return data

def get_columns(filters):
	cols = []
	cols = [
		{
			"fieldname": "invoice_number",
			"label": ("Invoice No"),
			"fieldtype": "Link",
			"options": "Payment Request",
			"width": "150"
		},
		{
			"fieldname": "invoice_date",
			"label": ("Raised Date"),
			"fieldtype": "Date",
			"width": "150"
		},
		{
			"fieldname": "due_date",
			"label": ("Due Date"),
			"fieldtype": "Date",
			"width": "150"
		},
		{
			"fieldname": "ex_from_date",
			"label": ("Ex From Date"),
			"fieldtype": "Date",
			"width": "150"
		},
		{
			"fieldname": "ex_to_date",
			"label": ("Ex To Date"),
			"fieldtype": "Date",
			"width": "150"
		},
		{
			"fieldname": "customer",
			"label": ("Client"),
			"fieldtype": "Data",
			"width": "150"
		},
		{
			"fieldname": "client_poc",
			"label": ("Client PoC"),
			"fieldtype": "Data",
			"width": "150"
		},
		{
			"fieldname": "project_manager",
			"label": ("Project Manager"),
			"fieldtype": "Data",
			"width": "150"
		},
		{
			"fieldname": "invoice_currency",
			"label": ("Currency"),
			"fieldtype": "Data",
			"width": "100"
		},
		{
			"fieldname": "actual_grand_total",
			"label": ("Grand Total (in actual currency)"),
			"fieldtype": "Currency",
			"options": "invoice_currency",
			"width": "100"
		},
		{
			"fieldname": "inr_grand_total",
			"label": ("Grand Total (in INR)"),
			"fieldtype": "Currency",
			"width": "100"
		},
		{
			"fieldname": "turacoz_entity",
			"label": ("Turacoz Entity"),
			"fieldtype": "Data",
			"width": "100"
		},
	]

	return cols		
