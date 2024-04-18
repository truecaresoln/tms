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
		combine1=" and date(`tabProject`.creation)>='%s'" %from_date
	else:
		combine1=""
			
	if(to_date):
		combine2=" and date(`tabProject`.creation)<='%s'" %to_date
	else:
		combine2=""
		
	if company:
		comp = " and `tabProject`.company = '%s'" %company
	else:
		comp = ""	
	
		
	data = []	
	data1 = frappe.db.sql("""select distinct tpdt.template_status,`tabProject`.project_detail_template,`tabProject`.company,tpd.deliverable,`tabProject`.turacoz_start_date,`tabProject`.name,`tabProject`.project_title,date(`tabProject`.creation) as creation,
		`tabProject`.tms_project_code,`tabProject`.customer,`tabProject`.contact_person,`tabProject`.bd_name,`tabProject`.project_scope,`tabProject`.expected_end_date,
		`tabProject`.payment_milestones,`tabProject`.manager_name,`tabProject`.project_current_status,'','','','' from `tabProject`
		 left join (select GROUP_CONCAT(deliverable) as deliverable,parent from `tabProject Deliverable` group by parent) tpd on `tabProject`.name = tpd.parent
		 left join `tabContact` as tc on `tabProject`.contact_person=tc.name 
		 left join `tabProject Detail Template` tpdt on `tabProject`.project_detail_template = tpdt.name
		 where project_current_status in ('Ongoing', 'Under Client Review', 'Under Journal Review', 'Under Internal Review', 'Under Internal QC', 'On Hold') and `tabProject`.customer!='Viatris Centre of Excellence' and project_type!='Internal' {0} {1} {2};""".format(
	combine1,combine2,comp),as_dict=True)
	
	for rec in data1:
		
		row = {}
		row["company"] = rec.company
		row["creation"] = rec.creation
		row["turacoz_start_date"] = rec.turacoz_start_date
		row["deliverable"] = rec.deliverable
		row["name"] = rec.name
		row["tms_project_code"] = rec.tms_project_code
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
		row["project_detail_template"] = rec.project_detail_template
		row["template_status"] = rec.template_status
			
		data2 =  frappe.db.sql("""select GROUP_CONCAT(distinct allocated_to_full_name,' ') as technical_team
			 	from `tabToDo` where project='{0}';""".format(rec.name), as_dict = True)
		for rec2 in data2:
			row["technical_team"] = rec2.technical_team
			
		dataPOAmount = frappe.db.sql("""select tso.name,tso.project, sum(tso.net_total) as po_amount,
				tso.currency,ter.rate_in_inr,
				(ter.rate_in_inr*sum(tso.net_total)) as po_amount_inr from `tabSales Order` tso
				left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
				where tso.project='{0}' 
				and tso.status not in('Cancelled') group by tso.project;""".format(rec.name), as_dict=True)	
		
		if dataPOAmount:
			row["po_amount"] = dataPOAmount[0]['po_amount']
			row["po_currency"] = dataPOAmount[0]['currency']
			row["po_amount_inr"] = dataPOAmount[0]['po_amount_inr']
		else:
			row["po_amount"] = ''
			row["po_currency"] = ''
			row["po_amount_inr"] = ''
			
		data.append(row)
			
	return data

def get_columns():
	cols = [
		{
			"fieldname": "project_detail_template",
			"label": ("Project Detail Template"),
			"fieldtype": "Link",
			"options": "Project Detail Template",
			"width": "200"
		},
		{
			"fieldname": "project_status",
			"label": ("Project Status"),
			"fieldtype": "Data",
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
			"fieldname": "project_title",
			"label": ("Project Title"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "technical_team",
			"label": ("Technical Team"),
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
			"fieldname": "deliverable",
			"label": ("Deliverable Type"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "po_amount",
			"label": ("PO Amount"),
			"fieldtype": "Float",
			"width": "150"
		},
		{
			"fieldname": "po_currency",
			"label": ("PO Currency"),
			"fieldtype": "Data",
			"width": "80"
		},
		{
			"fieldname": "po_amount_inr",
			"label": ("PO Amount INR"),
			"fieldtype": "Currency",
			"width": "200"
		},
		{
			"fieldname": "template_status",
			"label": ("Template Status"),
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
	