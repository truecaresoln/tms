# Copyright (c) 2013, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	chart = get_chart_data(data,filters)
	
	return columns, data, None, chart

def get_chart_data(data,filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	phase = filters.get("phase")
	company = filters.get("company")
	bd_person = filters.get("bd_person")
	project_manager = filters.get("project_manager")
	new_menu = filters.get("new_menu")
	chart = {}
	label = []
	conditions = ""
	if not data:
		data = []
	datasets1 = []
	datasets2 = []
	datasets3 = []
		
	label1 = frappe.db.sql("""select company_name from `tabCompany` order by 1""",as_dict=True)
	conditions="and `tabProject`.expected_start_date between '%s'" %from_date
	if to_date: conditions += " and '%s'" %to_date
	if company:
		new_company = " and `tabProject`.company = '%s'" %company
		label1 = frappe.db.sql("""select distinct project_current_status  from tabProject tp order by 1""",as_dict=True)
	else:
		new_company = ""
	if bd_person:
		new_bd_person = " and `tabProject`.bd_person = '%s'" %bd_person
	else:
		new_bd_person = ""	
	if project_manager:
		new_project_manager=" and project_manager = '%s'" %project_manager
	else:
		new_project_manager=""
	if new_menu == "All":
		current_menu = ""
	else:
		current_menu = " and `tabProject`.project_current_status = '%s'" %new_menu
	for l in label1:
		if company:
			label.append(l.project_current_status)
			dt = frappe.db.sql("""select count(*) as 'tot' from `tabProject` where project_current_status='{0}' {1} {2} {3} {4} """.format(l.project_current_status,conditions,new_company,new_bd_person,new_project_manager),as_dict=True)
			for d in dt:
				datasets1.append(d.tot)
		else:
			label.append(l.company_name)
			dt = frappe.db.sql("""select count(*) as 'tot' from `tabProject` where `tabProject`.project_current_status not in ('Completed') and company='{0}' {1} {2} {3} 
				""".format(l.company_name,conditions,new_bd_person,new_project_manager, current_menu),as_dict=True)
			for d in dt:
				datasets1.append(d.tot)
	chart = {
			"data": {
				'labels': label,
				'datasets': [{'name': 'Projects','values': datasets1}]
				}
	}
	chart["type"] = "bar"

	return chart

def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	phase = filters.get("phase")
	company = filters.get("company")
	bd_person = filters.get("bd_person")
	project_manager = filters.get("project_manager")
	new_menu = filters.get("new_menu")
	conditions="and `tabProject`.expected_start_date between '%s'" %from_date
	if to_date: conditions += " and '%s'" %to_date
	if company:
		new_company = " and `tabProject`.company = '%s'" %company
	else:
		new_company = ""
	if bd_person:
		new_bd_person = " and `tabProject`.bd_person = '%s'" %bd_person
	else:
		new_bd_person = ""	
	if project_manager:
		new_project_manager=" and project_manager = '%s'" %project_manager
	else:
		new_project_manager=""
	if new_menu == "All":
		current_menu = ""
	else:
		current_menu = " and `tabProject`.project_current_status = '%s'" %new_menu
	data = []
	data1 = frappe.db.sql("""select `tabProject`.name as project_name,`tabProject`.company,`tabProject`.name,
				`tabProject`.tms_project_code,`tabProject`.project_title,
				`tabProject`.project_scope,`tabProject`.customer,`tabProject`.contact_person,
				`tabProject`.project_current_status,`tabProject`.manager_name,`tabProject`.bd_name ,`tabProject`.expected_start_date,
				`tabProject`.expected_end_date,	datediff(`tabProject`.expected_end_date,`tabProject`.expected_start_date) as expected_tat,
				`tabProject`.actual_start_date,`tabProject`.actual_end_date,
				datediff(`tabProject`.actual_end_date,`tabProject`.actual_start_date) as actual_tat,
				`tabProject`.expected_hour,`tabProject`.actual_time,
				`Dr`.drafter,`Rw`.reviewer,`QC`.qc,`Ds`.designer,`tabProject`.services as service,
				`tabProject`.service_type,`tabProject`.number_of_drafts,`tpd`.deliverable as document_deliverable,
				`tpd`.start_date,`tpd`.end_date,`tpd`.client_sent_date,`tpd`.comment_received_date,
				`tpd`.input_from_client,`tpd`.internal_remarks,`tpd`.revision_start_date,
				`tpd`.revision_end_date,`tpd`.journal_resubmission
				from `tabProject` left join (select * from `tabProject New Update`) as `PU` 
				on (`PU`.name=`tabProject`.name)
				left join (select * from `tabProject Update Data` order by parent desc) as `tpd`
				on (tpd.parent=`PU`.name)
				left join (select GROUP_CONCAT(allocated_to_full_name) as drafter,project from `tabToDo` where role='Drafter' group by role,project) as `Dr` 
				on (`Dr`.project=`tabProject`.name)
				left join (select GROUP_CONCAT(allocated_to_full_name) as reviewer,project from `tabToDo` where role='Reviewer' group by role,project) as `Rw` 
				on (`Rw`.project=`tabProject`.name)
				left join (select GROUP_CONCAT(allocated_to_full_name) as qc,project from `tabToDo` where role='QCer' group by role,project) as `QC` 
				on (`QC`.project=`tabProject`.name)
				left join (select GROUP_CONCAT(allocated_to_full_name) as designer,project from `tabToDo` where role='Designer' group by role,project) as `Ds` 
				on (`Ds`.project=`tabProject`.name)
				where `tabProject`.is_active="Yes" and `tabProject`.project_current_status not in ('Completed') {0} {1} {2} {3} {4} group by `tabProject`.name order by `tabProject`.creation desc;""".format(conditions,new_company,new_bd_person,new_project_manager,current_menu),as_dict=True)
	for psr in data1:
		row={}
		project_name = psr["project_name"]
		row["company"] = psr["company"]
		row["name"] = psr["name"]
		row["tms_project_code"] = psr["tms_project_code"]
		row["project_title"] = psr["project_title"]
		row["project_scope"] = psr["project_scope"]
		row["customer"] = psr["customer"]
		row["contact_person"] = psr["contact_person"]
		row["project_current_status"] = psr["project_current_status"]
		row["manager_name"] = psr["manager_name"]
		row["bd_name"] = psr["bd_name"]
		row["expected_start_date"] = psr["expected_start_date"]
		row["expected_end_date"] = psr["expected_end_date"]
		row["expected_tat"] = psr["expected_tat"]
		row["actual_start_date"] = psr["actual_start_date"]
		row["actual_end_date"] = psr["actual_end_date"]
		row["actual_tat"] = psr["actual_tat"]
		row["expected_hour"] = psr["expected_hour"]
		row["actual_time"] = psr["actual_time"]
		row["drafter"] = psr["drafter"]
		row["reviewer"] = psr["reviewer"]
		row["qc"] = psr["qc"]
		row["designer"] = psr["designer"]
		row["service"] = psr["service"]
		row["service_type"] = psr["service_type"]
		row["number_of_drafts"] = psr["number_of_drafts"]
		data2  = []
		data2 = frappe.db.sql("""select * from `tabProject Update Data` where parent = '{0}' order by idx desc limit 1;""".format(project_name),as_dict=True)
		for pd in data2:
			row["document_deliverable"] = pd.deliverable
			row["start_date"] = pd.start_date
			row["end_date"] = pd.end_date
			row["client_sent_date"] = pd.client_sent_date
			row["comment_received_date"] = pd.comment_received_date
			row["input_from_client"] = pd.input_from_client
			row["internal_remarks"] = pd.internal_remarks
			row["revision_start_date"] = pd.revision_start_date
			row["revision_end_date"] = pd.revision_end_date
			row["journal_resubmission"] = pd.journal_resubmission
		data3  = []
		data3 = frappe.db.sql("""select * from `tabFinancial Update Data` where parent = '{0}' order by idx desc limit 1;""".format(project_name),as_dict=True)
		for pd in data3:
			row["financial_deliverable"] = pd.deliverable
			row["shared_with_client"] = pd.shared_with_client
			row["payment_received"] = pd.payment_received
		data.append(row)
			
	return data

def get_menu(filters):
# 	menu = []
# 	menu = frappe.db.sql("""select menu from `tabDashboard Menu where phase='{0}'""".format(filters.phase))
# 	result = list(menu)
	result = filters.phase
	return result
def get_columns(filters):
	return [
				{
					"fieldname": "company",
					"label": ("Company"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "name",
					"label": ("Project Code"),
					"fieldtype": "Data",
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
					"width": "200"
				}, 
				{
					"fieldname": "customer",
					"label": ("Client"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "contact_person",
					"label": ("Client PoC"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "project_current_status",
					"label": ("Project Status"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "manager_name",
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
					"fieldname": "expected_start_date",
					"label": ("Expected Start Date"),
					"fieldtype": "Date",
					"width": "200"
				},
				{
					"fieldname": "expected_end_date",
					"label": ("Expected End Date"),
					"fieldtype": "Date",
					"width": "200"
				},
				{
					"fieldname": "expected_tat",
					"label": ("Expected TAT"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "actual_start_date",
					"label": ("Actual Start Date"),
					"fieldtype": "Date",
					"width": "200"
				},
				{
					"fieldname": "actual_end_date",
					"label": ("Actual End Date"),
					"fieldtype": "Date",
					"width": "200"
				},
				{
					"fieldname": "actual_tat",
					"label": ("Actual TAT"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "expected_hour",
					"label": ("Expected Hour"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "actual_time",
					"label": ("Actual Hour"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "drafter",
					"label": ("Drafter"),
					"fieldtype": "Data",
					"width": "200"
				},		
				{
					"fieldname": "reviewer",
					"label": ("Reviewer"),
					"fieldtype": "Data",
					"width": "200"
				},			
				{
					"fieldname": "qc",
					"label": ("Qcer"),
					"fieldtype": "Data",
					"width": "200"
				},			
				{
					"fieldname": "designer",
					"label": ("Designer"),
					"fieldtype": "Data",
					"width": "200"
				},			
				{
					"fieldname": "service",
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
					"fieldname": "number_of_drafts",
					"label": ("Number of Drafts"),
					"fieldtype": "Data",
					"width": "200"
				},			
				{
					"fieldname": "document_deliverable",
					"label": ("Document Deliverable"),
					"fieldtype": "Data",
					"width": "200"
				},			
				{
					"fieldname": "start_date",
					"label": ("Start Date"),
					"fieldtype": "Data",
					"width": "200"
				},			
				{
					"fieldname": "end_date",
					"label": ("End Date"),
					"fieldtype": "Data",
					"width": "200"
				},			
				{
					"fieldname": "client_sent_date",
					"label": ("Client Sent Date"),
					"fieldtype": "Data",
					"width": "200"
				},			
				{
					"fieldname": "comment_received_date",
					"label": ("Client Review Date"),
					"fieldtype": "Data",
					"width": "200"
				},			
				{
					"fieldname": "input_from_client",
					"label": ("Input From Client"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "internal_remarks",
					"label": ("Remarks"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "revision_start_date",
					"label": ("Revision Start Date"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "revision_end_date",
					"label": ("Revision End Date"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "journal_resubmission",
					"label": ("Journal Re-Submission"),
					"fieldtype": "Data",
					"width": "200"
				},	
				{
					"fieldname": "financial_deliverable",
					"label": ("Financial Deliverable"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "shared_with_client",
					"label": ("Shared With Client"),
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"fieldname": "payment_received",
					"label": ("Payment Received"),
					"fieldtype": "Data",
					"width": "200"
				},
		
		]


