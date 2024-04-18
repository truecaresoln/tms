# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	start_date = filters.get("from_date")
	end_date = filters.get("to_date")
	
	data = frappe.db.sql("""select tpr.name, tpr.invoice_date, tpr.payment_status as 'Payment Status', tpr.project,tip.ion, ROUND(tpr.net_total,2) as 'net_total',ROUND(tpr.total_taxes,2) as 'total_taxes',ROUND((tpr.net_total*0.1),2) as 'tds', ROUND(tpr.grand_total,2) as 'grand_total',ROUND((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.1)) as 'receivable',tpr.due_date
			from `tabPayment Request` tpr
			left join `tabInvoice Particulars` tip on tpr.name = tip.parent 
			where tpr.customer_name = 'Viatris Centre of Excellence' and tpr.payment_status not in ('Paid','Cancelled') and tpr.status not in ('Cancelled') and tpr.invoice_date between '{0}' and '{1}' group by tpr.name""".format(start_date,end_date),as_dict=True)
	
	return data

def get_columns(filters):
			cols=[
			{
				"fieldname": "name",
				"label": _("Invoice Number"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "invoice_date",
				"label": _("Invoice Date"),
				"fieldtype": "Date",
				"width": "200"
			},
			{
				"fieldname": "project",
				"label": _("Project Code"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "ion",
				"label": _("ION Number"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "net_total",
				"label": _("Basic Amount (A)"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "total_taxes",
				"label": _("GST (B = 18% of A)"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "tds",
				"label": _("TDS (C = 10% of A)"),
				"fieldtype": "Data",
				"width": "200"
			},			
			{
				"fieldname": "grand_total",
				"label": _("Invoice Raised (D=A+B)"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "receivable",
				"label": _("Amount Receivable After Deducting TDS (E = D-C)"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "due_date",
				"label": _("Transaction Number"),
				"fieldtype": "Data",
				"width": "200"
			}
		]
			return cols