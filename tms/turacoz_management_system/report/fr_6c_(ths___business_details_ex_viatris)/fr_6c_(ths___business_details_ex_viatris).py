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
	company = 'Turacoz Healthcare Solutions Pvt Ltd'
	data=[]
	if company == "Turacoz Healthcare Solution Pvt Ltd":
		data1 = frappe.db.sql("""SELECT  tpr.name,tpr.invoice_date,tpr.status,tpr.customer_name,tpr.contact_person,tpr.project,tpr.currency,tpr.grand_total,tpr.grand_total*ter.rate_in_inr as 'grand_amount',tpr.payment_status,tpr.due_date,pe.reference_no,pe.reference_date,tp.manager_name 
			FROM `tabPayment Request` tpr
			left join `tabProject` tp on tpr.project = tp.name 
			left join `tabCurrency Exchange Rate` ter on tpr.currency=ter.name
			left join `tabPayment Entry` pe on tpr.name = pe.payment_request 
			where tpr.company='{2}' and tpr.customer_name not in ('Turacoz B.V.','Turacoz Healthcare Solution Pvt Ltd','Turacoz Solutions PTE Ltd','Turacoz Solutions LLC ','Viatris Centre of Excellence','Mylan Centre of Excellence')
			and tpr.invoice_date between '{0}' and '{1}' and tpr.payment_status not in ('Cancelled') and tpr.status not in ('Cancelled') group by tpr.name order by tpr.invoice_date
			""".format(start_date,end_date,company),as_dict=True)
	else:
		data1 = frappe.db.sql("""SELECT  tpr.name,tpr.invoice_date,tpr.status,tpr.customer_name,tpr.contact_person,tpr.project,tpr.currency,tpr.grand_total,tpr.grand_total*conversion_rate as 'grand_amount',tpr.payment_status,tpr.due_date,pe.reference_no,pe.reference_date,tp.manager_name 
			FROM `tabPayment Request` tpr
			left join `tabProject` tp on tpr.project = tp.name 
			left join `tabPayment Entry` pe on tpr.name = pe.payment_request 
			where tpr.company='{2}' and tpr.customer_name not in ('Turacoz B.V.','Turacoz Healthcare Solution Pvt Ltd','Turacoz Solutions PTE Ltd','Turacoz Solutions LLC ','Viatris Centre of Excellence','Mylan Centre of Excellence')
			and tpr.invoice_date between '{0}' and '{1}' and tpr.payment_status not in ('Cancelled') and tpr.status not in ('Cancelled') group by tpr.name order by tpr.invoice_date
			""".format(start_date,end_date,company),as_dict=True)
	row={}
	row["name"] = "<div><span><center><b>Invoices Raised</b></center></span></div>"
	data.append(row)
	for rec in data1:
		row={}
		row["name"] = rec.name
		row["invoice_date"] = rec.invoice_date
		row["project"] = rec.project
		row["customer_name"] = rec.customer_name
		row["contact_person"] = rec.contact_person
		row["currency"] = rec.currency
		row["due_date"] = rec.due_date
		row["grand_total"] = round(rec.grand_total,2)
		if company == "Turacoz Healthcare Solutions Pvt Ltd":
			row["grand_amount"] = str(round(rec.grand_amount,2))+" INR"
		elif company == "Turacoz B.V.":
			row["grand_amount"] = str(round(rec.grand_amount,2))+" EUR"
		else:
			row["grand_amount"] = str(round(rec.grand_amount,2))+" USD"
		row["payment_status"] = rec.payment_status
		row["reference_no"] = rec.reference_no
		row["reference_date"] = rec.reference_date
		row["manager_name"] = rec.manager_name
		data.append(row)
	
	if company == "Turacoz Healthcare Solution Pvt Ltd":
		data2 = frappe.db.sql("""SELECT  tpr.name,tpr.invoice_date,tpr.status,tpr.customer_name,tpr.contact_person,tpr.project,tpr.currency,tpr.grand_total,tpr.grand_total*ter.rate_in_inr as 'grand_amount',tpr.payment_status,tpr.due_date,pe.reference_no,pe.reference_date,tp.manager_name 
			FROM `tabPayment Request` tpr
			left join `tabProject` tp on tpr.project = tp.name 
			left join `tabPayment Entry` pe on tpr.name = pe.payment_request 
			left join `tabCurrency Exchange Rate` ter on tpr.currency=ter.name
			where tpr.company='{2}' and tpr.customer_name not in ('Turacoz B.V.','Turacoz Healthcare Solution Pvt Ltd','Turacoz Solutions PTE Ltd','Turacoz Solutions LLC ','Viatris Centre of Excellence','Mylan Centre of Excellence')
			and tpr.payment_date between '{0}' and '{1}' and tpr.payment_status not in ('Cancelled') and tpr.status not in ('Cancelled') group by tpr.name order by tpr.payment_date
			""".format(start_date,end_date,company),as_dict=True)
	else:
		data2 = frappe.db.sql("""SELECT  tpr.name,tpr.invoice_date,tpr.status,tpr.customer_name,tpr.contact_person,tpr.project,tpr.currency,tpr.grand_total,tpr.grand_total*conversion_rate as 'grand_amount',tpr.payment_status,tpr.due_date,pe.reference_no,pe.reference_date,tp.manager_name 
			FROM `tabPayment Request` tpr
			left join `tabProject` tp on tpr.project = tp.name 
			left join `tabPayment Entry` pe on tpr.name = pe.payment_request 
			where tpr.company='{2}' and tpr.customer_name not in ('Turacoz B.V.','Turacoz Healthcare Solution Pvt Ltd','Turacoz Solutions PTE Ltd','Turacoz Solutions LLC ','Viatris Centre of Excellence','Mylan Centre of Excellence')
			and tpr.payment_date between '{0}' and '{1}' and tpr.payment_status not in ('Cancelled') and tpr.status not in ('Cancelled') group by tpr.name order by tpr.payment_date
			""".format(start_date,end_date,company),as_dict=True)
	row={}
	row["name"] = "<div><span><center><b>Payments Received</b></center></span></div>"
	data.append(row)
	for rec in data2:
		row={}
		row["name"] = rec.name
		row["invoice_date"] = rec.invoice_date
		row["project"] = rec.project
		row["customer_name"] = rec.customer_name
		row["contact_person"] = rec.contact_person
		row["currency"] = rec.currency
		row["due_date"] = rec.due_date
		row["grand_total"] = round(rec.grand_total,2)
		if company == "Turacoz Healthcare Solutions Pvt Ltd":
			row["grand_amount"] = str(round(rec.grand_amount,2))+" INR"
		elif company == "Turacoz B.V.":
			row["grand_amount"] = str(round(rec.grand_amount,2))+" EUR"
		else:
			row["grand_amount"] = str(round(rec.grand_amount,2))+" USD"
		row["payment_status"] = rec.payment_status
		row["reference_no"] = rec.reference_no
		row["reference_date"] = rec.reference_date
		row["manager_name"] = rec.manager_name
		data.append(row)
	
	data3 = frappe.db.sql("""select deals.owner,users.full_name,close_date,deal_stage,deal_type,associated_company,associated_contact,service_type,therapeutic_areas,amount,currency,turacoz_entity 
					from `tabDeals` deals
					left join `tabUser` users on deals.owner=users.name
					where turacoz_entity='{2}' and close_date between '{0}' and '{1}' and deal_stage = 'Closed Won'
			""".format(start_date,end_date,company),as_dict=True)
	
	row={}
	row["name"]="<div><span><center><b>Deals (New Projects - Hubspots)</b></center></span></div>"
	data.append(row)
	row={}
	row['name'] = "<div><span><center><b>Project Owner/Deal Owner</b></center></span></div>"
	row['invoice_date'] = "<div><span><center><b>Close Date</b></center></span></div>"
	row['project'] = "<div><span><center><b>Associated Company</b></center></span></div>"
	row['customer_name'] = "<div><span><center><b>Associated Contact</b></center></span></div>"
	row['contact_person'] = "<div><span><center><b>Service Type</b></center></span></div>"
	row['currency'] = "<div><span><center><b>Therapeutic Area</b></center></span></div>"
	row['due_date'] = "<div><span><center><b>Amount</b></center></span></div>"
	row['grand_total'] = "<div><span><center><b>Turacoz Entity</b></center></span></div>"
	row['grand_amount'] = "<div><span><center><b>Deal Type</b></center></span></div>"
	data.append(row)

	for rec in data3:
		row={}
		row["name"] = rec.full_name
		row["invoice_date"] = rec.close_date
		row["project"] = rec.associated_company
		row["customer_name"] = rec.associated_contact
		row["contact_person"] = rec.service_type
		row["currency"] = rec.therapeutic_areas
		row["due_date"] = rec.amount
		row["grand_total"] = rec.turacoz_entity
		row["grand_amount"] = rec.deal_type
		data.append(row)
		
	return data
def get_columns(filters):
			cols=[
			{
				"fieldname": "name",
				"label": _("Invoice No"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "invoice_date",
				"label": _("Invoice Date"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "project",
				"label": _("Project"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "customer_name",
				"label": _("Customer"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "contact_person",
				"label": _("Client PoC"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "currency",
				"label": _("Currency"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "due_date",
				"label": _("Due Date"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "grand_total",
				"label": _("Amount"),
				"fieldtype": "Data",
				"width": "200"
			},			
			{
				"fieldname": "grand_amount",
				"label": _("Amount in Bank Currency"),
				"fieldtype": "Data",
				"width": "200"
			},	
			{
				"fieldname": "payment_status",
				"label": _("Status"),
				"fieldtype": "Data",
				"width": "200"
			},			
			{
				"fieldname": "reference_no",
				"label": _("Transaction No"),
				"fieldtype": "Data",
				"width": "200"
			},			
			{
				"fieldname": "reference_date",
				"label": _("Payment Date"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "manager_name",
				"label": _("Project Manager"),
				"fieldtype": "Data",
				"width": "200"
			},
		]
			return cols
