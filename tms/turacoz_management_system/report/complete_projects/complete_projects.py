# Copyright (c) 2013, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
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
	
	if viatris==1:
		data1 = frappe.db.sql("""select distinct `tabProject`.company,tpd.deliverable,`tabProject`.turacoz_end_date,`tabProject`.turacoz_start_date,`tabProject`.name,`tabProject`.project_title,
			`tabProject`.tms_project_code,`tabProject`.customer,`tabProject`.contact_person,`tabProject`.bd_name,`tabProject`.manager_name,`tabProject`.project_current_status,
			`tabProject`.services,`tabProject`.service_type,`tabProject`.total_planned_hours,		
			`tabProject`.project_scope,if(`tabSales Invoice`.project=`tabProject`.name,"Raised","Not Raised") as 'status',`tabProject`.expected_hour as 'expected_tat',`tabProject`.actual_time as 'actual_tat','','','','','','','','','','','' from `tabProject`
	 	    left join (select GROUP_CONCAT(deliverable) as deliverable,parent from `tabProject Deliverable` group by parent) tpd on `tabProject`.name = tpd.parent
			left join `tabSales Invoice` on (
					`tabSales Invoice`.project=`tabProject`.name
				)
			 where `tabProject`.project_type='External' and `tabProject`.project_current_status in ('Completed','Completed Technically') and `tabProject`.customer='Viatris Centre of Excellence' {0} {1} {2};""".format(combine1,combine2,comp),as_dict=True)
	else:
		data1 = frappe.db.sql("""select distinct `tabProject`.company,tpd.deliverable,`tabProject`.turacoz_end_date,`tabProject`.turacoz_start_date,`tabProject`.name,`tabProject`.project_title,
			`tabProject`.tms_project_code,`tabProject`.customer,`tabProject`.contact_person,`tabProject`.bd_name,`tabProject`.manager_name,`tabProject`.project_current_status,
			`tabProject`.services,`tabProject`.service_type,`tabProject`.total_planned_hours,		
			`tabProject`.project_scope,if(`tabSales Invoice`.project=`tabProject`.name,"Raised","Not Raised") as 'status',`tabProject`.expected_hour as 'expected_tat',`tabProject`.actual_time as 'actual_tat','','','','','','','','','','','' from `tabProject`
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
		if rec.total_planned_hours:
			row["expected_tat"] = rec.total_planned_hours
		else:
			row["expected_tat"] = rec.expected_tat	
		row["actual_tat"] = rec.actual_tat
		
		data2 = frappe.db.sql("""SELECT * from `tabProject Closure Checklist` where name='{0}'""".format(rec.name), as_dict = True)
		
		if data2: 
			for rec1 in data2:
				if rec1.final_draft_delivered_to_client == 1:
					row["technical_closure"] = "Yes"
				elif rec1.final_draft_delivered_to_client == 0:
					row["technical_closure"] = "No"	
				else:
					row["technical_closure"] = "Not Exists"	
					
				if rec1.payment_received_of_the_all_the_invoices_raised == 1:
					row["financial_closure"] = "Yes"
				elif rec1.payment_received_of_the_all_the_invoices_raised == 0:
					row["financial_closure"] = "No"	
				else:
					row["financial_closure"] = "Not Exists"
				if rec1.sample_documents_updated == 1:
					row["casestudy"] = "Yes"
					row["bdfolder"] = "Yes"
					row["bdmaster_sheet"] = "Yes"
				elif rec1.sample_documents_updated == 0:
					row["casestudy"] = "No"
					row["bdfolder"] = "No"
					row["bdmaster_sheet"] = "No"
				else:
					row["casestudy"] = "Not Exists"
					row["bdfolder"] = "Not Exists"
					row["bdmaster_sheet"] = "Not Exists"	
				if rec1.client_folder_updated == 1:
					row["experience_folder"] = "Yes"
				elif rec1.client_folder_updated ==0:
					row["experience_folder"] = "No"	
				else:
					row["experience_folder"] = "Not Exists"	
			row["closure_checklist_updated"] = "Yes"								
		else:
			row["technical_closure"] = "Not Exists"
			row["financial_closure"] = "Not Exists"	
			row["casestudy"] = "Not Exists"	
			row["experience_folder"] = "Not Exists"
			row["bdfolder"] = "Not Exists"
			row["bdmaster_sheet"] = "Not Exists"
			row["closure_checklist_updated"] = "No"	
			
		data3 = frappe.db.sql("""select * from `tabClient Feedback` where name = '{0}'""".format(rec.name), as_dict = True)
		if data3:
			sum = 0
			final_rating = 0
			for rec2 in data3:
				if rec2.quality_of_the_document:
					if rec2.quality_of_the_document:
						qotd = rec2.quality_of_the_document
					else:
						qotd = ""
					if rec2.communication:
						comm = rec2.communication
					else:
						comm = ""
					if rec2.project_management:
						pm = rec2.project_management
					else:
						pm = ""	
					if rec2.meeting_timeline_expectations:
						mte = rec2.meeting_timeline_expectations
					else:
						mte = ""
					if rec2.understanding_implementing_review_comments:
						uirc = rec2.understanding_implementing_review_comments
					else:
						uirc = ""	  			  				
					sum = qotd + comm + pm + mte + uirc
					final_rating = sum/5
				if rec2.client_feedback_sent_on:
					row["client_feedback"] = rec2.client_feedback_sent_on
				else:
					row["client_feedback"] = "Date Not Exists"
				if rec2.response_received_on:
					row["client_feedback_response_on"] = rec2.response_received_on
				else:
					row["client_feedback_response_on"] = "Date Not Exists"
				if rec2.exprience:
					row["remarks"] = rec2.exprience
				else:
					row["remarks"] = "Remark Not Exists"
				row["score"] = final_rating		 				
		else:
			row["client_feedback"] = "Feedback Not Sent"
			row["client_feedback_response_on"] = "Feedback Not Sent"
			row["remarks"] = "Feedback Not Sent"
			row["score"] = "Feedback Not Sent"		
					
		data4 = frappe.db.sql("""select * from `tabInternal Project Feedback` where project = ''""".format(rec.name), as_dict = True)
		if data4:
			row["internal_team_feedback"] = "Yes"
		else:
			row["internal_team_feedback"] = "No"
			
		data5 = frappe.db.sql("""select tso.name,tso.project, sum(tso.net_total) as po_amount,(sum(tso.net_total)*tcer.rate_in_inr) as po_amount_inr,tso.currency 
		from `tabSales Order` tso 
		left join `tabCurrency Exchange Rate` tcer on tso.currency = tcer.name
		where tso.project='{0}' 
		and tso.status not in('Cancelled') group by tso.project;""".format(rec.name), as_dict=True)
		
		to_currency = "INR"
		final_total_amount_inr = float()
		for rec5 in data5:
   # from_currency = rec5.currency
   # c = CurrencyRates()
   # currenyrate = c.get_rate(from_currency, to_currency)
   # currenyrate = round(currenyrate, 2)
			final_total_amount_inr = float(rec5.po_amount_inr)
			final_total_amount_inr = round(final_total_amount_inr, 2)
			if rec5.po_amount:
				row["po_amount"] = str(rec5.po_amount)+' '+rec5.currency
				row["po_amount_inr"] = final_total_amount_inr
			else:
				row["po_amount"] = "Sales Order not generated"
				row["po_amount_inr"] = "Sales Order not generated"
				
			data7 = frappe.db.sql("""select tsi.project, sum(tps.payment_amount) as total_amount,(sum(tps.payment_amount)*tcer.rate_in_inr) as total_amount_inr,tsi.currency from `tabSales Invoice` tsi
					left join `tabPayment Schedule` tps on tsi.name  = tps.parent
					left join `tabCurrency Exchange Rate` tcer on tsi.currency = tcer.name  
					where tsi.sales_order='{0}' and tps.invoice_status ='Unraised' and tsi.status not in ('Paid','Draft','Cancelled') group by tsi.project """.format(rec5.name), as_dict = True)
			if data7:
				to_currency1 = "INR"
				final_total_amount_inr1 = float()	
				for rec7 in data7:
     # from_currency1 = rec7.currency
     # c = CurrencyRates()
     # currenyrate1 = c.get_rate(from_currency1, to_currency1)
     # currenyrate1 = round(currenyrate1, 2)
					final_total_amount_inr1 = float(rec7.total_amount_inr)
					final_total_amount_inr1 = round(final_total_amount_inr1, 2)
					row["pending_unraised"] = str(rec7.total_amount)+' '+rec7.currency
					row["pending_unraised_inr"]	= final_total_amount_inr1
			else:
				row["pending_unraised"]	= '0.00'
				row["pending_unraised_inr"]	= '0.00'
		
		data6 = frappe.db.sql("""select tpr.project, sum(tpr.net_total) as total_amount,
		(sum(tpr.net_total)*tcer.rate_in_inr) as total_amount_inr,tpr.invoice_currency 
		from `tabPayment Request` tpr
		left join `tabCurrency Exchange Rate` tcer on tpr.invoice_currency = tcer.name
		where tpr.project='{0}'
		and tpr.payment_status in ('Unpaid','Overdue') group by tpr.project """.format(rec.name), as_dict = True)											
		if data6:
			to_currency3 = "INR"
			final_total_amount_inr3 = float()	
			for rec6 in data6:
    # from_currency3 = rec6.invoice_currency
    # c = CurrencyRates()
    # currenyrate3 = c.get_rate(from_currency3, to_currency3)
    # currenyrate3 = round(currenyrate3, 2)
				final_total_amount_inr3 = float(rec6.total_amount_inr)
				final_total_amount_inr3 = round(final_total_amount_inr3, 2)
				row["pending_raised"] = str(rec6.total_amount)+' '+rec6.invoice_currency
				row["pending_raised_inr"] = final_total_amount_inr3
		else:
			row["pending_raised"] = '0.00'
			row["pending_raised_inr"] = '0.00'
			
		data8 = frappe.db.sql("""select tpr.project, sum(tpr.net_total) as total_amount,
		(sum(tpr.net_total)*tcer.rate_in_inr) as total_amount_inr,tpr.invoice_currency 
		from `tabPayment Request` tpr
		left join `tabCurrency Exchange Rate` tcer on tpr.invoice_currency = tcer.name
		where tpr.project='{0}'
		and tpr.payment_status in ('Paid') group by tpr.project""".format(rec.name), as_dict = True)											
		if data8:
			to_currency2 = "INR"
			final_total_amount_inr2 = float()	
			for rec8 in data8:
    # from_currency2 = rec8.invoice_currency
    # c = CurrencyRates()
    # currenyrate2 = c.get_rate(from_currency2, to_currency2)
    # currenyrate2 = round(currenyrate2, 2)
				final_total_amount_inr2 = float(rec8.total_amount_inr)
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
			"fieldname": "services",
			"label": ("Service"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "service_type",
			"label": ("Service Type"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "status",
			"label": ("Invoice Status"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "expected_tat",
			"label": ("Expected TAT"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "actual_tat",
			"label": ("Actual TAT"),
			"fieldtype": "Data",
			"width": "200"
		},

		{
			"fieldname": "technical_closure",
			"label": ("Technical Closure"),
			"fieldtype": "Select",
			"options":['Yes','No'],
			"width": "200"
		},
		{
			"fieldname": "financial_closure",
			"label": ("Financial Closure"),
			"fieldtype": "Select",
			"options":['Yes','No'],
			"width": "200"
		},
		{
			"fieldname": "client_feedback",
			"label": ("Client Feedback Sent On"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "client_feedback_response_on",
			"label": ("Response Received On"),
			"fieldtype": "Select",
			"options":['Sent','Not Sent'],
			"width": "200"
		},
		{
			"fieldname": "score",
			"label": ("Score of Client Feedback"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "remarks",
			"label": ("Remarks"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "casestudy",
			"label": ("Case Study Uploaded"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "experience_folder",
			"label": ("Turacoz Experience Folder Updated"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "bdfolder",
			"label": ("BD Folder Updated"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "bdmaster_sheet",
			"label": ("Master BD Sheet Updated"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "closure_checklist_updated",
			"label": ("Project Closure Checklist Updated"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "internal_team_feedback",
			"label": ("Internal Team Feedback Documented in ERP"),
			"fieldtype": "Data",
			"width": "200"
		},

	]
	return cols