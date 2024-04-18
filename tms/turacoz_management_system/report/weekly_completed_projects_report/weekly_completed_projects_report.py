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
		combine1=" and date(turacoz_end_date)>='%s'" %from_date
	else:
		combine1=""
			
	if(to_date):
		combine2=" and date(turacoz_end_date)<='%s'" %to_date
	else:
		combine2=""
		
	if company:
		comp = " and `tabProject`.company = '%s'" %company
	else:
		comp = ""	
	data = []	
	
	data1 = frappe.db.sql("""select distinct `tabProject`.company,tpd.deliverable,`tabProject`.turacoz_end_date,`tabProject`.turacoz_start_date,`tabProject`.name,`tabProject`.project_title,
		`tabProject`.tms_project_code,`tabProject`.customer,`tabProject`.contact_person,`tabProject`.bd_name,`tabProject`.manager_name,`tabProject`.project_current_status,
		`tabProject`.services,`tabProject`.service_type,		
		`tabProject`.project_scope,if(`tabSales Invoice`.project=`tabProject`.name,"Raised","Not Raised") as 'status',datediff(`tabProject`.expected_end_date,`tabProject`.expected_start_date) as 'expected_tat',datediff(`tabProject`.turacoz_end_date,`tabProject`.turacoz_start_date) as 'actual_tat','','','','','','','','','','','' from `tabProject`
	 	left join (select GROUP_CONCAT(deliverable) as deliverable,parent from `tabProject Deliverable` group by parent) tpd on `tabProject`.name = tpd.parent
		left join `tabSales Invoice` on (
					`tabSales Invoice`.project=`tabProject`.name
				)
		where `tabProject`.project_type='External' and `tabProject`.project_current_status in ('Completed','Completed Technically') and `tabProject`.customer!='Viatris Centre of Excellence' {0} {1} {2};""".format(combine1,combine2,comp),as_dict=True)

	for rec in data1:
		row = {}
		row["company"] = rec.company
		row["turacoz_start_date"] = rec.turacoz_start_date
		row["turacoz_end_date"] = rec.turacoz_end_date
		row["name"] = rec.name
		row["tms_project_code"] = rec.tms_project_code
		row["project_title"] = rec.project_title
		row["customer"] = rec.customer
		row["contact_person"] = rec.contact_person
		if rec.project_current_status == "Completed":
			row["project_status"] = 'Completed Technically and Financially'
		else:
			row["project_status"] = rec.project_current_status	
		row["services"] = rec.services
		row["service_type"] = rec.service_type
		row["deliverable"] = rec.deliverable
		row["project_scope"] = rec.project_scope
		row["bd_name"] = rec.bd_name
		row["pm_name"] = rec.manager_name
		row["status"] = rec.status
		row["expected_tat"] = rec.expected_tat
		row["actual_tat"] = rec.actual_tat
		
		data2 = frappe.db.sql("""Select description from `tabWrap Up Calls` where parent = '{0}' ORDER by idx desc LIMIT 1""".format(rec.name), as_dict=True)
		
		for rec2 in data2:
			row["wrap_up_calls"] = rec2.description
		
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
			
		dataTechnicalTeam = frappe.db.sql("""select GROUP_CONCAT( DISTINCT allocated_to_full_name,' ') as tec_team 
		from `tabToDo` where project = '{0}' GROUP by project;""".format(rec.name), as_dict = True)	
		if dataTechnicalTeam:
			row["techical_team_inhouse"] = dataTechnicalTeam[0]['tec_team']
		else:
			row["techical_team_inhouse"] = ''
			
		dataFreelanceTeam = frappe.db.sql("""select GROUP_CONCAT(DISTINCT  tf.freelancer_name,' ') as freelacer_team 
			from `tabFreelancer Feedback Project Detail` tff
			left join `tabFreelancer` tf on tff.parent = tf.name
			where project = '{0}';""".format(rec.name), as_dict = True)
		if dataFreelanceTeam:
			row["freelancer_team"] = dataFreelanceTeam[0]['freelacer_team']
		else:
			row["freelancer_team"] = ''		
				
		data.append(row)		
			
	return data

def get_columns():
	cols = [
		{
			"fieldname": "customer",
			"label": ("Client"),
			"fieldtype": "Data",
			"width": "250"
		},
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
			"fieldname": "turacoz_end_date",
			"label": ("Date of Completion"),
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
			"fieldname": "techical_team_inhouse",
			"label": ("Technical Team Inhouse"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "freelancer_team",
			"label": ("Freelancer Team"),
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
			"fieldname": "wrap_up_calls",
			"label": ("Wrap up call status"),
			"fieldtype": "Data",
			"width": "200"
		},

	]
	return cols