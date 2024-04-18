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
	
	data1 = frappe.db.sql("""select distinct `tabProject`.company,tpd.deliverable,`tabProject`.number_of_drafts,`tabProject`.turacoz_start_date,`tabProject`.name,`tabProject`.project_title,
			`tabProject`.tms_project_code,`tabProject`.customer,`tabProject`.contact_person,`tabProject`.bd_name,`tabProject`.project_scope,`tabProject`.expected_end_date,
			`tabProject`.payment_milestones,`tabProject`.project_delayed_on_track,`tabProject`.delayed_reason,`tabProject`.manager_name,`tabProject`.project_current_status,'','','','' from `tabProject`
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
		row["delayed"] = rec.project_delayed_on_track
		row["delayed_reason"] = rec.delayed_reason
			
		data2 =  frappe.db.sql("""select type_of_challenge,description_of_challenge,solutions
			 	from `tabChallenges and Commitments` where project='{0}';""".format(rec.name), as_dict = True)
		for rec2 in data2:
			row["typeofchallenge"] = rec2.type_of_challenge
			row["description_of_challenge"] = rec2.description_of_challenge
			row["solution_of_challenge"] = rec2.solutions
			
		dataPOStatus = frappe.db.sql("""select count(*) as sales_order_count from 
				`tabSales Order` where project='{0}' 
				and status  not in ('Cancelled')""".format(rec.name), as_dict = True)
		salesOrderCount = dataPOStatus[0]['sales_order_count']
		if salesOrderCount > 0:
			row["po_status"] = "Received"
		else:
			row["po_status"] = "Not Received"
			
		dataInvoiceMilestone= frappe.db.sql("""select count(*) as payment_milestone 
			from `tabSales Invoice` tsi
			left join `tabPayment Schedule` tps on tsi.name  = tps.parent 
			WHERE tsi.project = '{0}' and tsi.status not in ('Cancelled')""".format(rec.name), as_dict = True)		
		invoiceMilestone = 	dataInvoiceMilestone[0]['payment_milestone']
		
		if invoiceMilestone > 0:
			row["payment_milestone"] = invoiceMilestone
		else:
			row["payment_milestone"] = "Sales Invoice Not Created"
			
		dataInvoiceStatus = frappe.db.sql("""select GROUP_CONCAT(round(tps.invoice_portion,2),' ',tps.payment_term, ' (',tps.invoice_status,')') as invoice_raise 
			from `tabSales Invoice` tsi 
			left join `tabPayment Schedule` tps on tsi.name = tps.parent
			where tsi.project = '{0}' 
			and tsi.status not in ('Cancelled')""".format(rec.name), as_dict = True)
				
		if dataInvoiceStatus:
			row["invoice_status"] = dataInvoiceStatus[0]['invoice_raise']	
		else:
			row["invoice_status"] = "Invoice Not Created"
			
		dataPaymentReceived = frappe.db.sql("""select count(*) as payment_received_count 
			from `tabPayment Request` where project = '{0}' 
			and payment_status in ('Paid')""".format(rec.name), as_dict = True)
		paymentReceivedCount = 	dataPaymentReceived[0]["payment_received_count"]	
		
		if paymentReceivedCount > 0:
			row["payment_status"] = "Payment Received of "+str(paymentReceivedCount)
		else:
			row["payment_status"] = "No Payment Received"
			
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
			"fieldname": "name",
			"label": ("Project Code"),
			"fieldtype": "Link",
			"options": "Project",
			"width": "200"
		},
		{
			"fieldname": "contact_person",
			"label": ("Client POC"),
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
			"fieldname": "project_status",
			"label": ("Project Status"),
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
			"fieldname": "bd_name",
			"label": ("BD Person"),
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
			"fieldname": "delayed",
			"label": ("Delayed/On Track"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "delayed_reason",
			"label": ("Delayed Reason"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "po_status",
			"label": ("PO Status"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "payment_milestone",
			"label": ("Payment Milestone"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "invoice_status",
			"label": ("Invoice Status in %"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "payment_status",
			"label": ("Payment Status"),
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
		{
			"fieldname": "company",
			"label": ("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"width": "200"
		},
	]
	
	return cols
	