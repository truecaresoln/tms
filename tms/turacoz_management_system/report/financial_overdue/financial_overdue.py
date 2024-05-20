# Copyright (c) 2024, RSA and contributors
# For license information, please see license.txt

import frappe
import datetime
from datetime import datetime


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data

def get_data(filters):
	data = []
	forcastData = frappe.db.sql("""SELECT tpr.name,tpr.invoice_date,tpr.due_date,tpr.customer_name,
		tpr.contact_person as client_poc,tp.manager_name,
		tpr.invoice_currency,tpr.net_total,
		(tcer.rate_in_inr * tpr.net_total) as net_total_in_inr,tpr.total_taxes,tpr.grand_total,
		(tcer.rate_in_inr * tpr.grand_total) as grand_total_in_inr
		FROM `tabPayment Request` tpr
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` tcer on tpr.invoice_currency = tcer.name
		WHERE tpr.due_date < DATE_SUB(NOW(), INTERVAL 7 DAY) and tpr.payment_status in ('Overdue') order by tpr.due_date DESC""", as_dict = True)
	
	for invoicesData in forcastData:
		row = {}
		row['invoice_number'] = invoicesData.name
		row['invoice_date'] = invoicesData.invoice_date
		row['due_date'] = invoicesData.due_date

		today = datetime.now().strftime('%d-%m-%Y')
		dtnew = invoicesData.due_date.strftime('%d-%m-%Y')
		dt1 = datetime.strptime(today,'%d-%m-%Y').date()
		dt2 = datetime.strptime(dtnew,'%d-%m-%Y').date()
		delta = (dt1 - dt2).days

		row['overdue_in_days'] = str(delta)+" Days"
		row['customer'] = invoicesData.customer_name
		row['client_poc'] = invoicesData.client_poc
		row['project_manager'] = invoicesData.manager_name
		row['invoice_currency'] = invoicesData.invoice_currency
		# row['actual_net_total'] = invoicesData.net_total
		# row['inr_net_total'] = invoicesData.net_total_in_inr
		# row['total_taxes'] = invoicesData.total_taxes
		row['actual_grand_total'] = invoicesData.grand_total
		row['inr_grand_total'] = invoicesData.grand_total_in_inr

		data.append(row)

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
			"fieldname": "overdue_in_days",
			"label": ("Overdue in Days"),
			"fieldtype": "Data",
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
	]

	return cols		
