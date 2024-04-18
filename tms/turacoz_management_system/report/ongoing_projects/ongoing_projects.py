# Copyright (c) 2013, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
from forex_python.converter import CurrencyRates
import math

def execute(filters=None):
	return get_columns(), get_data(filters)

def get_data(filters):
	from_date=filters.get("from_date")
	to_date=filters.get("to_date")
	company=filters.get("company")
	viatris=filters.get("viatris")
	
	if(from_date):
		combine1=" and date(expected_start_date)>='%s'" %from_date
	else:
		combine1=""
			
	if(to_date):
		combine2=" and date(expected_start_date)<='%s'" %to_date
	else:
		combine2=""
		
	if company:
		comp = " and `tabProject`.company = '%s'" %company
	else:
		comp = ""	
	
		
	data = []	
	
	if viatris == 1:
		data1 = frappe.db.sql("""select distinct `tabProject`.company,tpd.deliverable,`tabProject`.turacoz_start_date,`tabProject`.name,`tabProject`.project_title,
			`tabProject`.tms_project_code,`tabProject`.customer,`tabProject`.contact_person,`tabProject`.bd_name,`tabProject`.project_scope,`tabProject`.expected_end_date,
			`tabProject`.payment_milestones,`tabProject`.manager_name,`tabProject`.project_current_status,'','','','' from `tabProject`
			 left join (select GROUP_CONCAT(deliverable) as deliverable,parent from `tabProject Deliverable` group by parent) tpd on `tabProject`.name = tpd.parent
			 left join `tabContact` as tc on `tabProject`.contact_person=tc.name 
			 where project_current_status in ('Ongoing', 'Under Client Review', 'Under Journal Review', 'Under Internal Review', 'Under Internal QC', 'On Hold') and customer='Viatris Centre of Excellence' and project_type!='Internal' {0} {1} {2};""".format(
			combine1,combine2,comp),as_dict=True)
	else:
		data1 = frappe.db.sql("""select distinct `tabProject`.company,tpd.deliverable,`tabProject`.turacoz_start_date,`tabProject`.name,`tabProject`.project_title,
			`tabProject`.tms_project_code,`tabProject`.customer,`tabProject`.contact_person,`tabProject`.bd_name,`tabProject`.project_scope,`tabProject`.expected_end_date,
			`tabProject`.payment_milestones,`tabProject`.manager_name,`tabProject`.project_current_status,'','','','' from `tabProject`
			 left join (select GROUP_CONCAT(deliverable) as deliverable,parent from `tabProject Deliverable` group by parent) tpd on `tabProject`.name = tpd.parent
			 left join `tabContact` as tc on `tabProject`.contact_person=tc.name 
			 where project_current_status in ('Ongoing', 'Under Client Review', 'Under Journal Review', 'Under Internal Review', 'Under Internal QC', 'On Hold') and customer!='Viatris Centre of Excellence' and project_type!='Internal' {0} {1} {2};""".format(
		combine1,combine2,comp),as_dict=True)
	
	for rec in data1:
		
		row = {}
		row["company"] = rec.company
		row["turacoz_start_date"] = rec.turacoz_start_date
		row["name"] = rec.name
		row["tms_project_code"] = rec.tms_project_code
		row["deliverable"] = rec.deliverable
		row["project_title"] = rec.project_title
		row["customer"] = rec.customer
		row["contact_person"] = rec.contact_person
		row["project_status"] = rec.project_current_status	
		row["services"] = rec.services
		row["service_type"] = rec.service_type
		row["project_scope"] = rec.project_scope
		row["bd_name"] = rec.bd_name
		row["pm_name"] = rec.manager_name
		row["project_timeline"] = rec.expected_end_date
		row["payment_milestones"] = rec.payment_milestones
			
		data2 =  frappe.db.sql("""select type_of_challenge,description_of_challenge,solutions
			 	from `tabChallenges and Commitments` where project='{0}';""".format(rec.name), as_dict = True)
		for rec2 in data2:
			row["typeofchallenge"] = rec2.type_of_challenge
			row["description_of_challenge"] = rec2.description_of_challenge
			row["solution_of_challenge"] = rec2.solutions
			
		data5 = frappe.db.sql("""select name,project, sum(net_total) as po_amount,currency from `tabSales Order` tso where project='{0}' and status not in('Cancelled') group by project;""".format(rec.name), as_dict=True)
		
		to_currency = "INR"
		final_total_amount_inr = float()
		for rec5 in data5:
			from_currency = rec5.currency
			c = CurrencyRates()
			currenyrate = c.get_rate(from_currency, to_currency)
			currenyrate = round(currenyrate, 2)
			final_total_amount_inr = float(rec5.po_amount) * currenyrate
			final_total_amount_inr = round(final_total_amount_inr, 2)
			if rec5.po_amount:
				row["po_amount"] = str(rec5.po_amount)+' '+rec5.currency
				row["po_amount_inr"] = final_total_amount_inr
			else:
				row["po_amount"] = "Sales Order not generated"
				row["po_amount_inr"] = "Sales Order not generated"
				
			data7 = frappe.db.sql("""select tsi.project, sum(tps.payment_amount) as total_amount,tsi.currency from `tabSales Invoice` tsi
					left join `tabPayment Schedule` tps on tsi.name  = tps.parent 
					where tsi.sales_order='{0}' and tps.invoice_status ='Unraised' and tsi.status not in ('Paid','Draft','Cancelled') group by tsi.project """.format(rec5.name), as_dict = True)
			if data7:
				to_currency1 = "INR"
				final_total_amount_inr1 = float()	
				for rec7 in data7:
					from_currency1 = rec7.currency
					c = CurrencyRates()
					currenyrate1 = c.get_rate(from_currency1, to_currency1)
					currenyrate1 = round(currenyrate1, 2)
					final_total_amount_inr1 = float(rec7.total_amount) * currenyrate1
					final_total_amount_inr1 = round(final_total_amount_inr1, 2)
					row["pending_unraised"] = str(rec7.total_amount)+' '+rec7.currency
					row["pending_unraised_inr"]	= final_total_amount_inr1
			else:
				row["pending_unraised"]	= '0.00'
				row["pending_unraised_inr"]	= '0.00'
		
		data6 = frappe.db.sql("""select project, sum(net_total) as total_amount,invoice_currency from `tabPayment Request` where project='{0}' and payment_status in ('Unpaid','Overdue') group by project """.format(rec.name), as_dict = True)											
		if data6:
			to_currency3 = "INR"
			final_total_amount_inr3 = float()	
			for rec6 in data6:
				from_currency3 = rec6.invoice_currency
				c = CurrencyRates()
				currenyrate3 = c.get_rate(from_currency3, to_currency3)
				currenyrate3 = round(currenyrate3, 2)
				final_total_amount_inr3 = float(rec6.total_amount) * currenyrate3
				final_total_amount_inr3 = round(final_total_amount_inr3, 2)
				row["pending_raised"] = str(rec6.total_amount)+' '+rec6.invoice_currency
				row["pending_raised_inr"] = final_total_amount_inr3
		else:
			row["pending_raised"] = '0.00'
			row["pending_raised_inr"] = '0.00'
			
		data8 = frappe.db.sql("""select project, sum(net_total) as total_amount,invoice_currency from `tabPayment Request` where project='{0}' and payment_status in ('Paid') group by project """.format(rec.name), as_dict = True)											
		if data8:
			to_currency2 = "INR"
			final_total_amount_inr2 = float()	
			for rec8 in data8:
				from_currency2 = rec8.invoice_currency
				c = CurrencyRates()
				currenyrate2 = c.get_rate(from_currency2, to_currency2)
				currenyrate2 = round(currenyrate2, 2)
				final_total_amount_inr2 = float(rec8.total_amount) * currenyrate2
				final_total_amount_inr2 = round(final_total_amount_inr2, 2)	
				row["received_amount"] = str(rec8.total_amount)+' '+rec8.invoice_currency
				row["received_amount_inr"] = final_total_amount_inr2
		else:
			row["received_amount"] = '0.00'
			row["received_amount_inr"]	= '0.00'	
		data.append(row)
			
	return data

def get_columns():
	cols = [
		{
			"fieldname": "company",
			"label": ("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"width": "200"
		},
		{
			"fieldname": "turacoz_start_date",
			"label": ("Date of Initiation"),
			"fieldtype": "Date",
			"width": "200"
		},
		{
			"fieldname": "name",
			"label": ("Project Code"),
			"fieldtype": "Link",
			"options": "Project",
			"width": "200"
		},
		{
			"fieldname": "tms_project_code",
			"label": ("TMS Project Code"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "project_title",
			"label": ("Project Title"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "project_scope",
			"label": ("Project Scope"),
			"fieldtype": "Data",
			"width": "300"
		},
		{
			"fieldname": "deliverable",
			"label": ("Deliverable Type"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "customer",
			"label": ("Client"),
			"fieldtype": "Data",
			"width": "250"
		},
		{
			"fieldname": "contact_person",
			"label": ("Client POC"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "project_status",
			"label": ("Project Status"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "bd_name",
			"label": ("BD Person"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "pm_name",
			"label": ("Project Manager"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "po_amount",
			"label": ("PO Amount"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "po_amount_inr",
			"label": ("PO Amount (INR)"),
			"fieldtype": "Float",
			"width": "200"
		},
		{
			"fieldname": "received_amount",
			"label": ("Received Amount"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "received_amount_inr",
			"label": ("Received Amount (INR)"),
			"fieldtype": "Float",
			"width": "200"
		},
		{
			"fieldname": "pending_unraised",
			"label": ("Pending Unraised Amount"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "pending_unraised_inr",
			"label": ("Pending Unraised Amount (INR)"),
			"fieldtype": "Float",
			"width": "200"
		},
		{
			"fieldname": "pending_raised",
			"label": ("Pending Raised Amount"),
			"fieldtype": "Float",
			"width": "200"
		},
		{
			"fieldname": "pending_raised_inr",
			"label": ("Pending Raised (INR)"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "project_timeline",
			"label": ("Projected Timeline"),
			"fieldtype": "Date",
			"width": "200"
		},
		{
			"fieldname": "payment_milestones",
			"label": ("Payment Milestone"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "typeofchallenge",
			"label": ("Challenges"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "description_of_challenge",
			"label": ("Description of Challenge"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "solution_of_challenge",
			"label": ("Solutions"),
			"fieldtype": "Data",
			"width": "200"
		},

	]
	
	return cols
	