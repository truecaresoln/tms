# Copyright (c) 2023, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe

# import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	search_string = filters.get("search_string")
	session = filters.get("session")
	company = filters.get("company")
	dtype = filters.get("dtype")
	department = filters.get("department")
	category = filters.get("category")
	sub_category = filters.get("sub_category")
	project_code = filters.get("project_code")
	
	data=[]
	new_search_string=''
	new_session=''
	new_company=''
	new_dtype=''
	new_department=''
	new_category=''
	new_sub_category=''
	new_project_code=''
	
	if search_string:
		new_search_string = "and document_title like '%%%s%%'" %search_string
	else:
		new_search_string = ''
		

	if company:
		new_company = " and company='%s'" %company
	else:
		new_company=''
		
	if dtype:
		new_dtype = " and dtype='%s'" %dtype
	else:
		new_dtype=''
		
	if department:
		new_department = " and tdms.department='%s'" %department
	else:
		new_department=''
		
	if category:
		new_category = " and tdms.category='%s'" %category
	else:
		new_category=''
		
	if sub_category:
		new_sub_category = " and tdms.sub_category='%s'" %sub_category
	else:
		new_sub_category=''
		
	if project_code:
		new_project_code = " and project_code='%s'" %project_code
	else:
		new_project_code=''
		
	if department == 'Medical Services':
		data2 = frappe.db.sql("""select tdms.name,tdms.`session`,tdms.company,tdms.document_title,tdms.document_type,tdms.version,tdms.classification,tdms.department
					,tdc.category,tsdc.sub_category,tdms.file_link,project_code,services,region,therapeutic_area,customer,client_poc,project_manager,bd_poc,viatris_region,project_category,project_brands 
					from `tabDocument Management System` tdms 
					left join `tabDMS Category` tdc on tdms.category = tdc.name 
					left join `tabDMS Sub Category` tsdc on tdms.sub_category = tsdc.name  where session='{0}' {1} {2} {3} {4} {5} {6} {7}""".format(session,new_search_string,new_company,new_dtype,new_department,new_category,new_sub_category,new_project_code),as_dict=True)
		
		for ds1 in data2:
			row={}
			row['name'] = ds1.name
			row['session'] = ds1.session
			row['company'] = ds1.company
			row['document_title'] = ds1.document_title
			row['document_type'] = ds1.document_type
			row['version'] = ds1.version
			row['classification'] = ds1.classification
			row['department'] = ds1.department
			row['category'] = ds1.category
			row['sub_category'] = ds1.sub_category
			row['project_code'] = ds1.project_code
			row['services'] = ds1.services
			row['region'] = ds1.region
			row['therapeutic_area'] = ds1.therapeutic_area
			row['customer'] = ds1.customer
			row['client_poc'] = ds1.client_poc
			row['project_manager'] = ds1.project_manager
			row['bd_poc'] = ds1.bd_poc
			row['viatris_region'] = ds1.viatris_region
			row['project_category'] = ds1.project_category
			row['project_brands'] = ds1.project_brands
			row['file_link'] = "<a href='%s' target='_blank'>Click Me to download</a>" %ds1.file_link
			data.append(row)
	elif((department == 'Training and Developments') or (department == 'Turacoz Events')):
		data3 = frappe.db.sql("""select tdms.name,tdms.`session`,tdms.company,tdms.document_title,tdms.document_type,tdms.version,tdms.classification,tdms.department
					,tdc.category,tsdc.sub_category,tdms.file_link,event_name,location,coordinator,trainers_or_speakers,date_from,date_to 
					from `tabDocument Management System` tdms 
					left join `tabDMS Category` tdc on tdms.category = tdc.name 
					left join `tabDMS Sub Category` tsdc on tdms.sub_category = tsdc.name  where session='{0}' {1} {2} {3} {4} {5} {6} {7}""".format(session,new_search_string,new_company,new_dtype,new_department,new_category,new_sub_category,new_project_code),as_dict=True)
		
		for ds1 in data3:
			row={}
			row['name'] = ds1.name
			row['session'] = ds1.session
			row['company'] = ds1.company
			row['document_title'] = ds1.document_title
			row['document_type'] = ds1.document_type
			row['version'] = ds1.version
			row['classification'] = ds1.classification
			row['department'] = ds1.department
			row['category'] = ds1.category
			row['sub_category'] = ds1.sub_category
			row['event_name'] = ds1.event_name
			row['location'] = ds1.location
			row['coordinator'] = ds1.coordinator
			row['trainers_or_speakers'] = ds1.trainers_or_speakers
			row['date_from'] = ds1.date_from
			row['date_to'] = ds1.date_to
			row['file_link'] = "<a href='%s' target='_blank'>Click Me to download</a>" %ds1.file_link
			data.append(row)
	else:
		data1 = frappe.db.sql("""select tdms.name,tdms.`session`,tdms.company,tdms.document_title,tdms.document_type,tdms.version,tdms.classification,tdms.department
					,tdc.category,tsdc.sub_category,tdms.file_link 
					from `tabDocument Management System` tdms 
					left join `tabDMS Category` tdc on tdms.category = tdc.name 
					left join `tabDMS Sub Category` tsdc on tdms.sub_category = tsdc.name  where session='{0}' {1} {2} {3} {4} {5} {6} {7}""".format(session,new_search_string,new_company,new_dtype,new_department,new_category,new_sub_category,new_project_code),as_dict=True)
		
		for ds1 in data1:
			row={}
			row['name'] = ds1.name
			row['session'] = ds1.session
			row['company'] = ds1.company
			row['document_title'] = ds1.document_title
			row['document_type'] = ds1.document_type
			row['version'] = ds1.version
			row['classification'] = ds1.classification
			row['department'] = ds1.department
			row['category'] = ds1.category
			row['sub_category'] = ds1.sub_category
			row['file_link'] = "<a href='%s' target='_blank'>Click Me to download</a>" %ds1.file_link
			data.append(row)
		
	return data
		

	
def get_columns(filters):
	department = filters.get("department")
	cols = []
	if department == 'Medical Services':
				cols=[
			{
				"fieldname": "name",
				"label": _("DMS Code"),
				"fieldtype": "Link",
				"options": "Document Management System",
				"width": "130"
			},
			{
				"fieldname": "session",
				"label": _("Session"),
				"fieldtype": "Data",
				"width": "80"
			},
			{
				"fieldname": "company",
				"label": _("Company"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "document_title",
				"label": _("Title"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "document_type",
				"label": _("Type"),
				"fieldtype": "Data",
				"width": "120"
			},
			{
				"fieldname": "version",
				"label": _("Ver"),
				"fieldtype": "Data",
				"width": "40"
			},
			{
				"fieldname": "classification",
				"label": _("Classification"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "department",
				"label": _("Department"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "category",
				"label": _("Category"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "sub_category",
				"label": _("Sub Category"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "project_code",
				"label": _("Project Code"),
				"fieldtype": "Link",
				"options": "Project",
				"width": "130"
			},
			{
				"fieldname": "services",
				"label": _("Services"),
				"fieldtype": "Data",
				"width": "80"
			},
			{
				"fieldname": "region",
				"label": _("Region"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "therapeutic_area",
				"label": _("Therapeutic Area"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "customer",
				"label": _("Customer"),
				"fieldtype": "Data",
				"width": "120"
			},
			{
				"fieldname": "client_poc",
				"label": _("Client PoC"),
				"fieldtype": "Data",
				"width": "40"
			},
			{
				"fieldname": "project_manager",
				"label": _("Project Manager"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "bd_poc",
				"label": _("BD PoC"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "viatris_region",
				"label": _("Viatris Region"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "project_category",
				"label": _("Project Category"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "project_brands",
				"label": _("Project Brands"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "file_link",
				"label": _("Attached File Link"),
				"fieldtype": "Data",
				"width": "200"
			},
		]
	elif((department == 'Training and Developments') or (department == 'Turacoz Events')):
		cols=[
			{
				"fieldname": "name",
				"label": _("DMS Code"),
				"fieldtype": "Link",
				"options": "Document Management System",
				"width": "130"
			},
			{
				"fieldname": "session",
				"label": _("Session"),
				"fieldtype": "Data",
				"width": "80"
			},
			{
				"fieldname": "company",
				"label": _("Company"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "document_title",
				"label": _("Title"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "document_type",
				"label": _("Type"),
				"fieldtype": "Data",
				"width": "120"
			},
			{
				"fieldname": "version",
				"label": _("Ver"),
				"fieldtype": "Data",
				"width": "40"
			},
			{
				"fieldname": "classification",
				"label": _("Classification"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "department",
				"label": _("Department"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "category",
				"label": _("Category"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "sub_category",
				"label": _("Sub Category"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "event_name",
				"label": _("Event Name"),
				"fieldtype": "Data",
				"width": "130"
			},
			{
				"fieldname": "location",
				"label": _("Location"),
				"fieldtype": "Data",
				"width": "80"
			},
			{
				"fieldname": "coordinator",
				"label": _("Coordinator"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "trainers_or_speakers",
				"label": _("Speakers"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "date_from",
				"label": _("Date From"),
				"fieldtype": "Date",
				"width": "120"
			},
			{
				"fieldname": "date_to",
				"label": _("Date To"),
				"fieldtype": "Date",
				"width": "40"
			},
			{
				"fieldname": "file_link",
				"label": _("Attached File Link"),
				"fieldtype": "Data",
				"width": "200"
			},
		]
	else:
		cols=[
			{
				"fieldname": "name",
				"label": _("DMS Code"),
				"fieldtype": "Link",
				"options": "Document Management System",
				"width": "130"
			},
			{
				"fieldname": "session",
				"label": _("Session"),
				"fieldtype": "Data",
				"width": "80"
			},
			{
				"fieldname": "company",
				"label": _("Company"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "document_title",
				"label": _("Title"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "document_type",
				"label": _("Type"),
				"fieldtype": "Data",
				"width": "120"
			},
			{
				"fieldname": "version",
				"label": _("Ver"),
				"fieldtype": "Data",
				"width": "40"
			},
			{
				"fieldname": "classification",
				"label": _("Classification"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "department",
				"label": _("Department"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "category",
				"label": _("Category"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "sub_category",
				"label": _("Sub Category"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "file_link",
				"label": _("Attached File Link"),
				"fieldtype": "Data",
				"width": "200"
			},
		]
	return cols 
