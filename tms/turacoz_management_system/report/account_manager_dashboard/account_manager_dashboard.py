# Copyright (c) 2023, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe
from datetime import datetime, timedelta

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data


def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	type = filters.get("type")
	account_managers = filters.get("account")
	current_date = datetime.today()
	prev_date = datetime.today() - timedelta(days=7)
	if from_date and to_date:
		print(from_date)
	else:
		from_date = prev_date
		to_date = current_date
	data = []
	if type=='Ongoing Projects':
		if from_date and to_date:
			data1 = frappe.db.sql("""select name,status,project_current_status,project_type,expected_end_date,customer,contact_person,bd_person,bd_name,project_manager,manager_name
	,team_leader_name,team_leader_medical_writer,account_manager_name,company,turacoz_end_date,is_active,percent_complete,project_name
	from `tabProject` where project_current_status not in ('Completed','Completed Technically','Cancelled') and account_manager_name='{0}' and expected_start_date between '{1}' and '{2}';""".format(account_managers,from_date,to_date),as_dict=True)
		else:
			data1 = frappe.db.sql("""select name,status,project_current_status,project_type,expected_end_date,customer,contact_person,bd_person,bd_name,project_manager,manager_name
	,team_leader_name,team_leader_medical_writer,account_manager_name,company,turacoz_end_date,is_active,percent_complete,project_name
	from `tabProject` where project_current_status not in ('Completed','Completed Technically','Cancelled') and account_manager_name='{0}';""".format(account_managers),as_dict=True)	
		for rec in data1:
			rows ={}
			rows['name'] = rec.name
			rows['status'] = rec.status
			rows['project_current_status'] = rec.project_current_status
			rows['project_type'] = rec.project_type
			rows['expected_end_date'] = rec.expected_end_date
			rows['customer'] = rec.customer
			rows['contact_person'] = rec.contact_person
			rows['bd_name'] = rec.bd_name
			rows['manager_name'] = rec.manager_name
			rows['team_leader_medical_writer'] = rec.team_leader_medical_writer
			rows['account_manager_name'] = rec.account_manager_name
			rows['company'] = rec.company
			rows['turacoz_end_date'] = rec.turacoz_end_date
			rows['is_active'] = rec.is_active
			rows['percent_complete'] = rec.percent_complete
			rows['project_name'] = rec.project_name
			data.append(rows)
	elif type=='Finance':
		data6 = frappe.db.sql("""select name from `tabProject` where project_current_status not in ('Cancelled') and project_type = 'External' and account_manager_name='{0}' and expected_start_date between '{1}' and '{2}'""".format(account_managers,from_date,to_date),as_dict=True)
		EUR_total = 0
		USD_total = 0
		INR_total = 0
		SGD_total = 0
		EUR_unraised = 0
		USD_unraised = 0
		INR_unraised = 0
		SGD_unraised = 0
		EUR_raised = 0
		USD_raised = 0
		INR_raised = 0
		SGD_raised = 0
		EUR_received = 0
		USD_received = 0
		INR_received = 0
		SGD_received = 0
		EUR_convert_rate = 0.0
		USD_convert_rate = 0.0
		SGD_convert_rate = 0.0
		INR_total_convert = 0.0
		
		convertdata = frappe.db.sql("""SELECT currency,rate_in_inr from `tabCurrency Exchange Rate` tcer""",as_dict=True)
		for rec111 in convertdata:
			if rec111.currency == 'USD':
				USD_convert_rate = rec111.rate_in_inr
			elif rec111.currency == 'EUR':
				EUR_convert_rate = rec111.rate_in_inr
			elif rec111.currency == 'SGD':
				SGD_convert_rate = rec111.rate_in_inr
			
		for rec6 in data6:
			data7 = frappe.db.sql("""select name from `tabPayment Request` where project='{0}'""".format(rec6.name),as_dict=True)
			if data7:
				data1 = frappe.db.sql("""select so.*,tsi.name as invoice_no,tsi.status as invoice_status,
				date(tsi.modified) as invoice_date,tsi.net_total as invoice_total,
				tsi.total_taxes_and_charges as invoice_taxes,tsi.grand_total as invoice_grand_total,
				tsi.outstanding_amount as invoice_outstanding_amount,tsi.conversion_rate,
				tp.bd_name,tp.manager_name,tp.project_current_status,
				tp.project_title,tp.tms_project_code,tp.region,sum(tpr.grand_total) as main_invoice_total,tp.services
				from `tabSales Order` as so 
				left join `tabSales Invoice` as tsi on so.name=tsi.sales_order
				left join `tabPayment Request` as tpr on tsi.name=tpr.sales_invoice
				left join `tabProject` as tp on so.project=tp.name 
				where tp.name = '{0}' and tp.project_current_status not in ('Cancelled') and tsi.status in ('Unpaid','Overdue','Partly Paid') and tpr.status not in ('Cancelled') group by so.name;""".format(rec6.name),as_dict=True)
			else:
				data1 = frappe.db.sql("""select so.*,tsi.name as invoice_no,tsi.status as invoice_status,
				date(tsi.modified) as invoice_date,tsi.net_total as invoice_total,
				tsi.total_taxes_and_charges as invoice_taxes,tsi.grand_total as invoice_grand_total,
				tsi.outstanding_amount as invoice_outstanding_amount,tsi.conversion_rate,
				tp.bd_name,tp.manager_name,tp.project_current_status,
				tp.project_title,tp.tms_project_code,tp.region,'0.0' as main_invoice_total,tp.services
				from `tabSales Order` as so 
				left join `tabSales Invoice` as tsi on so.name=tsi.sales_order
				left join `tabProject` as tp on so.project=tp.name 
				where tp.name = '{0}' and tp.project_current_status not in ('Cancelled') and tsi.status in ('Unpaid','Overdue','Partly Paid') group by so.name;""".format(rec6.name),as_dict=True)
					
			
			for rec in data1:
					
				row={}
				if rec.invoice_date:
					invoice_dt = rec.invoice_date
				else:
					invoice_dt = 'Unraised' 
				if rec.invoice_no:
					invoice_n = rec.invoice_no
				else:
					invoice_n = "Unraised"
				if rec.invoice_status: 
					invoice_s = rec.invoice_status
				else:
					invoice_s = "Unraised"  
									
				outstanding = rec.invoice_outstanding_amount
				conversion = rec.conversion_rate
				if outstanding is None:
					outstanding=0
				if conversion is None:
					conversion=1
				final_outstanding = outstanding/conversion
				final_outstanding = round(final_outstanding,2)
					
				invoice_tot=float(rec.main_invoice_total)
				invoice_grand=rec.invoice_grand_total
				if invoice_tot is None:
					invoice_tot=0
				if invoice_grand is None:
					invoice_grand=0
				invoice_unraised = invoice_grand-invoice_tot
						
				a = rec.invoice_grand_total
				b = final_outstanding
				if a is None:
					a = 0
				if b is None:
					b = 0	
				received_amt =  a-b	 
				
				row["customer"]=rec.customer
				row["contact_display"]=rec.contact_display
				row["currency"]=rec.currency
				row["project"]=rec.project
				row["project_status"]=rec.project_current_status
				row["project_title"]=rec.project_title
				row["invoice_no"]=invoice_n
				row["status"]=invoice_s
				row["invoice_date"]=invoice_dt
				if(rec.currency=="EUR"):
					row["po_amount"]="€{0}".format(round(rec.net_total,2))
					row["po_amount_inr"]="₹{0}".format(round(round(rec.net_total,2)*EUR_convert_rate),2)
					row["invoice_amount"]="€{0}".format(round(rec.invoice_total,2))
					row["total_taxes"]="€{0}".format(round(rec.invoice_taxes,2))
					row["grand_total"]="€{0}".format(round(rec.invoice_grand_total,2))
					row["outstanding"]="€{0}".format(round(final_outstanding,2))
					row["invoice_total"]="€{0}".format(round(invoice_tot,2))
					row["received_amount"]="€{0}".format(round(received_amt,2))
					row["invoice_unraised_total"]="€{0}".format(round(invoice_unraised,2))
					EUR_total += final_outstanding
					EUR_raised += invoice_tot
					EUR_unraised += invoice_unraised
					EUR_received += received_amt
				elif(rec.currency=="USD"):
					row["po_amount"]="${0}".format(round(rec.net_total,2))
					row["po_amount_inr"]="₹{0}".format(round(round(rec.net_total,2)*USD_convert_rate),2)
					row["invoice_amount"]="${0}".format(round(rec.invoice_total,2))
					row["total_taxes"]="${0}".format(round(rec.invoice_taxes,2))
					row["grand_total"]="${0}".format(round(rec.invoice_grand_total,2))
					row["outstanding"]="${0}".format(round(final_outstanding,2))
					row["invoice_total"]="${0}".format(round(invoice_tot,2))
					row["invoice_unraised_total"]="${0}".format(round(invoice_unraised,2))
					row["received_amount"]="${0}".format(round(received_amt,2))
					USD_total += final_outstanding
					USD_raised += invoice_tot
					USD_unraised += invoice_unraised
					USD_received += received_amt
				elif(rec.currency=="SGD"):
					row["po_amount"]="S${0}".format(round(rec.net_total,2))
					row["po_amount_inr"]="₹{0}".format(round(round(rec.net_total,2)*SGD_convert_rate),2)
					row["invoice_amount"]="S${0}".format(round(rec.invoice_total,2))
					row["total_taxes"]="S${0}".format(round(rec.invoice_taxes,2))
					row["grand_total"]="S${0}".format(round(rec.invoice_grand_total,2))
					row["outstanding"]="S${0}".format(round(final_outstanding,2))
					row["invoice_total"]="S${0}".format(round(invoice_tot,2))
					row["invoice_unraised_total"]="S${0}".format(round(invoice_unraised,2))
					row["received_amount"]="S${0}".format(round(received_amt,2))
					SGD_total += final_outstanding
					SGD_raised += invoice_tot
					SGD_unraised += invoice_unraised
					SGD_received += received_amt	
				else:
					row["po_amount"]="₹{0}".format(round(rec.net_total,2))
					row["po_amount_inr"]="₹{0}".format(round(rec.net_total,2))
					row["invoice_amount"]="₹{0}".format(round(rec.invoice_total,2))
					row["total_taxes"]="₹{0}".format(round(rec.invoice_taxes,2))
					row["grand_total"]="₹{0}".format(round(rec.invoice_grand_total,2))
					row["outstanding"]="₹{0}".format(round(final_outstanding,2))
					row["invoice_total"]="₹{0}".format(round(invoice_tot,2))
					row["invoice_unraised_total"]="₹{0}".format(round(invoice_unraised,2))
					row["received_amount"]="₹{0}".format(round(received_amt,2))
					INR_total += final_outstanding
					INR_raised += invoice_tot
					INR_unraised += invoice_unraised
					INR_received += received_amt
						
				row["company"] = rec.company
				data.append(row)
		INR_raised_total = 0.0
		INR_unraised_total = 0.0
		INR_total_total = 0.0
		INR_received_total = 0.0
		
		row = {}
		row["grand_total"] = "Total (INR)"
		row["invoice_total"] = "₹{0}".format(round(INR_raised,2))
		INR_raised_total = INR_raised_total + round(INR_raised,2)
		row["invoice_unraised_total"] = "₹{0}".format(round(INR_unraised,2))
		INR_unraised_total = INR_unraised_total + round(INR_unraised,2)
		row["outstanding"] =  "₹{0}".format(round(INR_total,2))
		INR_total_total = INR_total_total + round(INR_total,2)
		row["received_amount"] = "₹{0}".format(round(INR_received,2))
		INR_received_total = INR_received_total + round(INR_received,2)
		data.append(row)
		row = {}
		row["grand_total"] = "Total (USD)"
		row["invoice_total"] = "${0}".format(USD_raised)
		print("usd:"+str(round(USD_raised,2)*USD_convert_rate))
		INR_raised_total = INR_raised_total + (round(USD_raised,2)*USD_convert_rate)
		row["invoice_unraised_total"] = "${0}".format(USD_unraised)
		INR_unraised_total = INR_unraised_total + (round(USD_unraised,2)*USD_convert_rate)
		row["outstanding"] =  "${0}".format(round(USD_total,2))
		INR_total_total = INR_total_total + (round(USD_total,2)*USD_convert_rate)
		row["received_amount"] = "${0}".format(round(USD_received,2))
		INR_received_total = INR_received_total + (round(USD_received,2)*USD_convert_rate)
		data.append(row)
		row = {}
		row["grand_total"] = "Total (EUR)"
		row["invoice_total"] = "€{0}".format(EUR_raised)
		INR_raised_total = INR_raised_total + (round(EUR_raised,2)*EUR_convert_rate)
		print("eur:"+str(round(EUR_raised,2)*EUR_convert_rate))
		row["invoice_unraised_total"] = "€{0}".format(EUR_unraised)
		INR_unraised_total = INR_unraised_total + (round(EUR_unraised,2)*EUR_convert_rate)
		row["outstanding"] =  "€{0}".format(round(EUR_total,2))
		INR_total_total = INR_total_total + (round(EUR_total,2)*EUR_convert_rate)
		row["received_amount"] = "€{0}".format(round(EUR_received,2))
		INR_received_total = INR_received_total + (round(EUR_received,2)*EUR_convert_rate)
		data.append(row)
		row = {}
		row["grand_total"] = "Total (SGD)"
		row["invoice_total"] = "S${0}".format(SGD_raised)
		INR_raised_total = INR_raised_total + (round(SGD_raised,2)*SGD_convert_rate)
		print("sgd:"+str(round(SGD_raised,2)*SGD_convert_rate))
		row["invoice_unraised_total"] = "S${0}".format(SGD_unraised)
		INR_unraised_total = INR_unraised_total + (round(SGD_unraised,2)*SGD_convert_rate)
		row["outstanding"] =  "S${0}".format(round(SGD_total,2))
		INR_total_total = INR_total_total + (round(SGD_total,2)*SGD_convert_rate)
		row["received_amount"] = "S${0}".format(round(SGD_received,2))
		INR_received_total = INR_received_total + (round(SGD_received,2)*SGD_convert_rate)
		data.append(row)
		row = {}
		row["grand_total"] = "Grand Total (in INR)"
		row["invoice_total"] = "₹{0}".format(round(INR_raised_total,2))
		row["invoice_unraised_total"] = "₹{0}".format(round(INR_unraised_total,2))
		row["outstanding"] =  "₹{0}".format(round(INR_total_total,2))
		row["received_amount"] = "₹{0}".format(round(INR_received_total,2))
		data.append(row)		
	elif type=='Contacts':
		datacontact=frappe.db.sql("""select tp.name,customer,add1.country,contact_person,contact.first_name,contact.last_name,contact.email_id,contact.department,contact.designation,contact.phone,contact.mobile_no,contact.linkedin  from `tabProject` tp
		left join `tabCustomer` cust on tp.customer=cust.name
		left join `tabContact` contact on tp.contact_person = contact.name
		left join `tabDynamic Link` tdl on cust.name = tdl.link_name  
		left join `tabAddress` add1 on tdl.parent=add1.name 
		where account_manager_name='{0}' group by tp.name""".format(account_managers),as_dict=True)
		
		for rec in datacontact:
			row={}
			row['name']=rec.name
			row['first_name']=rec.first_name
			row['last_name']=rec.last_name
			row['company']=rec.customer
			row['country']=rec.country
			row['department']=rec.department
			row['designation']=rec.designation
			row['email_id']=rec.email_id
			row['phone']=rec.phone
			row['mobile_no']=rec.mobile_no
			row['linkedin']=rec.linkedin
			data.append(row)
	elif type=='Agreements':
		dataagreement=frappe.db.sql("""select contract_document_type,signed_on,end_date,tc.party_name,add1.country,tc.turacoz_legal_entity  from tabContract tc 
		left join `tabCustomer` cust on tc.party_name=cust.name
		left join `tabDynamic Link` tdl on cust.name = tdl.link_name  
		left join `tabAddress` add1 on tdl.parent=add1.name 
		where status='Active' and party_name in (select customer from `tabProject` where account_manager_name='{0}')
		group by party_name,contract_document_type 
		order by start_date DESC""".format(account_managers),as_dict=True)
		
		for rec in dataagreement:
			row={}
			row['contract_document_type']=rec.contract_document_type
			row['signed_on']=rec.signed_on
			row['end_date']=rec.end_date
			row['party_name']=rec.party_name
			row['country']=rec.country
			row['turacoz_legal_entity']=rec.turacoz_legal_entity
			data.append(row)
	elif type=='Marketing Data':
		data8 = frappe.db.sql("""select user_id,employee_name from `tabEmployee` where employee_name = '{0}'""".format(account_managers),as_dict=True)
		account_managers1=data8[0]['user_id']
		row={}
		row['deal_name'] = '<b>Meeting Scheduled</b>'
		data.append(row)
		print(current_date)
		print(prev_date)

			
		data2 = frappe.db.sql("""select deal_name,country,region,currency,service_type,therapeutic_areas,
				turacoz_entity,deal_stage,amount,deal_type,associated_contact,associated_company 
				from `tabDeals` 
				where deal_stage='Meeting Scheduled' and owner = '{0}' and create_date between '{1}' and '{2}'""".format(account_managers1,from_date,to_date),as_dict=True)
		for rec in data2:
			row={}
			row['deal_name'] = rec.deal_name
			row['country'] = rec.country
			row['region'] = rec.region
			row['currency'] = rec.currency
			row['service_type']	= rec.service_type
			row['therapeutic_areas'] = rec.therapeutic_areas
			row['turacoz_entity'] = rec.turacoz_entity
			row['deal_stage'] = rec.deal_stage
			row['amount'] = rec.amount
			row['deal_type'] = rec.deal_type
			row['associated_contact'] = rec.associated_contact
			data.append(row)

		row={}
		row['deal_name'] = '<b>New Contact</b>'
		data.append(row)
		data3 = frappe.db.sql("""select deal_name,country,region,currency,service_type,therapeutic_areas,
				turacoz_entity,deal_stage,amount,deal_type,associated_contact,associated_company 
				from `tabDeals` 
				where deal_type='New Business' and owner = '{0}' and create_date between '{1}' and '{2}'""".format(account_managers1,from_date,to_date),as_dict=True)
		for rec in data3:
			row={}
			row['deal_name'] = rec.deal_name
			row['country'] = rec.country
			row['region'] = rec.region
			row['currency'] = rec.currency
			row['service_type']	= rec.service_type
			row['therapeutic_areas'] = rec.therapeutic_areas
			row['turacoz_entity'] = rec.turacoz_entity
			row['deal_stage'] = rec.deal_stage
			row['amount'] = rec.amount
			row['deal_type'] = rec.deal_type
			row['associated_contact'] = rec.associated_contact
			data.append(row)

		row={}
		row['deal_name'] = '<b>New Requirement Received</b>'
		data.append(row)
		data4 = frappe.db.sql("""select deal_name,country,region,currency,service_type,therapeutic_areas,
				turacoz_entity,deal_stage,amount,deal_type,associated_contact,associated_company 
				from `tabDeals` 
				where deal_stage in ('Request for Proposal','Request for Information') and owner = '{0}' and create_date between '{1}' and '{2}'""".format(account_managers1,from_date,to_date),as_dict=True)
		for rec in data4:
			row={}
			row['deal_name'] = rec.deal_name
			row['country'] = rec.country
			row['region'] = rec.region
			row['currency'] = rec.currency
			row['service_type']	= rec.service_type
			row['therapeutic_areas'] = rec.therapeutic_areas
			row['turacoz_entity'] = rec.turacoz_entity
			row['deal_stage'] = rec.deal_stage
			row['amount'] = rec.amount
			row['deal_type'] = rec.deal_type
			row['associated_contact'] = rec.associated_contact
			data.append(row)

		row={}
		row['deal_name'] = '<b>New Projects</b>'
		data.append(row)
		data5 = frappe.db.sql("""select deal_name,country,region,currency,service_type,therapeutic_areas,
				turacoz_entity,deal_stage,amount,deal_type,associated_contact,associated_company 
				from `tabDeals` 
				where deal_stage='Closed Won' and owner = '{0}' and create_date between '{1}' and '{2}'""".format(account_managers1,from_date,to_date),as_dict=True)
		for rec in data5:
			row={}
			row['deal_name'] = rec.deal_name
			row['country'] = rec.country
			row['region'] = rec.region
			row['currency'] = rec.currency
			row['service_type']	= rec.service_type
			row['therapeutic_areas'] = rec.therapeutic_areas
			row['turacoz_entity'] = rec.turacoz_entity
			row['deal_stage'] = rec.deal_stage
			row['amount'] = rec.amount
			row['deal_type'] = rec.deal_type
			row['associated_contact'] = rec.associated_contact
			data.append(row)			

	return data

def get_columns(filters):
	account_managers = filters.get("account")
	type = filters.get("type")
	cols = []
	if type=='Ongoing Projects':
		cols = [
			{
				"fieldname": "name",
				"label": _("Project Code"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "project_current_status",
				"label": _("Project Current Status"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "project_type",
				"label": _("Project Type"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "expected_end_date",
				"label": _("Expected End Date"),
				"fieldtype": "Date",
				"width": "150"
			},
			{
				"fieldname": "customer",
				"label": _("Client"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "contact_person",
				"label": _("Client PoC"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "bd_name",
				"label": _("BD PoC"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "manager_name",
				"label": _("Project Manager"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "team_leader_medical_writer",
				"label": _("Team Leader"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "account_manager_name",
				"label": _("Account Manager"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "company",
				"label": _("Company"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "turacoz_end_date",
				"label": _("Turacoz End Date"),
				"fieldtype": "Date",
				"width": "150"
			},
			{
				"fieldname": "is_active",
				"label": _("Is Active"),
				"fieldtype": "Data",
				"width": "50"
			},
			{
				"fieldname": "percent_complete",
				"label": _("%Complete"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "project_name",
				"label": _("Project Name"),
				"fieldtype": "Data",
				"width": "150"
			},
		]
	elif type=='Finance':
		cols=[
			{
			    "fieldname": "project",
			    "label": _("Project"),
				"fieldtype": "Link",
				"options": "Project",
			    "width": "200"
			},
			{
			    "fieldname": "customer",
			    "label": _("Client"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
			    "fieldname": "contact_display",
			    "label": _("Financial PoC"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
			    "fieldname": "project_status",
			    "label": _("Project Status"),
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
			    "fieldname": "po_amount",
			    "label": _("PO Amount"),
			    "fieldtype": "Data",
		        "option": "currency",
			    "width": "200"
			},	  		
			{
			    "fieldname": "po_amount_inr",
			    "label": _("PO Amount(in INR)"),
			    "fieldtype": "Data",
		        "option": "currency",
			    "width": "200"
			},	  		
			{
			    "fieldname": "grand_total",
			    "label": _("PI Grand Total"),
			    "fieldtype": "Data",
			    "width": "200"
			},
		    {
		        "fieldname": "invoice_total",
		        "label": _("Invoices Raised Amount"),
		        "fieldtype": "Data",
		        "width": "200"
		    },
			{
		        "fieldname": "invoice_unraised_total",
		        "label": _("Invoice Unraised Amount"),
		        "fieldtype": "Data",
		        "width": "200"
		    },
			{
			    "fieldname": "received_amount",
			    "label": _("Total Received Amount"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
			    "fieldname": "outstanding",
			    "label": _("Total Outstanding"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
				"fieldname": "company",
			    "label": _("Company"),
			    "fieldtype": "Data",
			    "width": "200"
		    },		
			]
	elif type=='Contacts':
		cols=[
			{
				"fieldname": "name",
				"label": _("Project Code"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
			    "fieldname": "first_name",
			    "label": _("First Name"),
				"fieldtype": "Data",
			    "width": "200"
			},
			{
			    "fieldname": "last_name",
			    "label": _("Last Name"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
			    "fieldname": "company",
			    "label": _("Company"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
			    "fieldname": "country",
			    "label": _("Country"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
		        "fieldname": "department",
		        "label": _("Department"),
		        "fieldtype": "Data",
		        "width": "200"
		    },
			{
			    "fieldname": "designation",
			    "label": _("Designation"),
			    "fieldtype": "Data",
			    "width": "200"
			},	  		
			{
			    "fieldname": "email_id",
			    "label": _("Email"),
			    "fieldtype": "Data",
			    "width": "200"
			},	  		
			{
			    "fieldname": "linkedin",
			    "label": _("LinkedIn"),
			    "fieldtype": "Data",
			    "width": "200"
			},
		    {
		        "fieldname": "phone",
		        "label": _("Phone"),
		        "fieldtype": "Data",
		        "width": "200"
		    },
			{
		        "fieldname": "mobile_no",
		        "label": _("Mobile No"),
		        "fieldtype": "Data",
		        "width": "200"
		    },
			]
	elif type=='Agreements':
		cols=[
			{
				"fieldname": "contract_document_type",
				"label": _("Type of Document"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
			    "fieldname": "signed_on",
			    "label": _("Signed On"),
				"fieldtype": "Data",
			    "width": "200"
			},
			{
			    "fieldname": "end_date",
			    "label": _("Expiring On"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
			    "fieldname": "party_name",
			    "label": _("Client Entity"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
			    "fieldname": "country",
			    "label": _("Country"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
		        "fieldname": "turacoz_legal_entity",
		        "label": _("Turacoz Entity"),
		        "fieldtype": "Data",
		        "width": "200"
		    },
			]
	elif type=='Marketing Data':
		cols=[
			{
				"fieldname": "deal_name",
				"label": _("Deal"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
			    "fieldname": "associated_contact",
			    "label": _("PoC"),
				"fieldtype": "Data",
			    "width": "200"
			},
			{
			    "fieldname": "country",
			    "label": _("Country"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
			    "fieldname": "region",
			    "label": _("Region"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
			    "fieldname": "deal_stage",
			    "label": _("Deat Stage"),
			    "fieldtype": "Data",
			    "width": "200"
			},
			{
		        "fieldname": "deal_type",
		        "label": _("Deal Type"),
		        "fieldtype": "Data",
		        "width": "200"
		    },
			{
		        "fieldname": "service_type",
		        "label": _("Service Type"),
		        "fieldtype": "Data",
		        "width": "200"
		    },			
			{
		        "fieldname": "therapeutic_areas",
		        "label": _("Therapeutic Areas"),
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
		        "fieldname": "amount",
		        "label": _("Amount"),
		        "fieldtype": "Data",
		        "width": "200"
		    },
			{
		        "fieldname": "turacoz_entity",
		        "label": _("Turacoz Entity"),
		        "fieldtype": "Data",
		        "width": "200"
		    },
			]

	return cols

