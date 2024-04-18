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
	data=[]
	data1 = frappe.db.sql("""select tpr.name, tpr.invoice_date, tpr.payment_status as 'Payment Status', tpr.project,tip.ion, ROUND(tpr.net_total,2) as 'net_total',ROUND(tpr.total_taxes,2) as 'total_taxes',ROUND((tpr.net_total*0.1),2) as 'tds', ROUND(tpr.grand_total,2) as 'grand_total',ROUND((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.1)) as 'receivable',tpr.due_date
			from `tabPayment Request` tpr
			left join `tabInvoice Particulars` tip on tpr.name = tip.parent 
			where tpr.customer_name = 'Viatris Centre of Excellence' and tpr.payment_status not in ('Paid','Cancelled') and tpr.status not in ('Cancelled') and tpr.invoice_date between '{0}' and '{1}' group by tpr.name""".format(start_date,end_date),as_dict=True)
	total_net=0.0
	total_taxes=0.0
	total_tds=0.0
	total_grand=0.0
	total_receive=0.0
	row={}
	row["name"] = "<div><span><b>Viatris Pending Invoices From " + str(start_date) + " To " + str(end_date)+"</b></span></div>"
	data.append(row)
	for rec in data1:
		row={}
		row["name"] = rec.name
		row["invoice_date"] = rec.invoice_date
		row["payment_status"] = rec.payment_status
		row["project"] = rec.project
		row["ion"] = rec.ion
		row["net_total"] = round(rec.net_total,2)
		row["total_taxes"] = round(rec.total_taxes,2)
		row["tds"] = round(rec.tds,2)
		row["grand_total"] = round(rec.grand_total,2)
		row["receivable"] = round(rec.receivable,2)
		row["due_date"] = rec.due_date
		total_net = total_net + round(rec.net_total,2)
		total_taxes = total_taxes + round(rec.total_taxes,2)
		total_tds = total_tds + round(rec.tds,2)
		total_grand = total_grand + round(rec.grand_total,2)
		total_receive = total_receive + round(rec.receivable,2)
		data.append(row)
	row={}
	row['net_total'] = "<div><span><b>%s</b></span></div>" %round(total_net,2)
	row['total_taxes'] = "<div><span><b>%s</b></span></div>" %round(total_taxes,2)
	row['tds'] = "<div><span><b>%s</b></span></div>" %round(total_tds,2)
	row['grand_total'] = "<div><span><b>%s</b></span></div>" %round(total_grand,2)
	row['receivable'] = "<div><span><b>%s</b></span></div>" %round(total_receive,2)
	data.append(row)
		
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
				"label": _("Due Date"),
				"fieldtype": "Data",
				"width": "200"
			}
		]
			return cols