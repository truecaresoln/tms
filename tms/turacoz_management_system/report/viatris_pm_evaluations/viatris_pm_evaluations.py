# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe
from datetime import date, datetime, timedelta
from warnings import _getcategory


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	start_date = filters.get("from_date")
	end_date = filters.get("to_date")
	project_category = filters.get("project_category")
	viatris_project_country = filters.get("viatris_project_country")
	region = filters.get("region")
	therapeutic_area = filters.get("therapeutic_area")	
	
	today = datetime.today()
	year = today.year
	month = today.month
	
	
	if start_date:
		first_date = start_date
	else:
		first_date = get_first_date_of_current_month(year,month)
		
	if end_date:
		last_date = end_date
	else:
		last_date = get_last_date_of_month(year, month)			
 	
	data = []
	
	if project_category or viatris_project_country or region or therapeutic_area:
		
		data1 = frappe.db.sql("""select DISTINCT tc.first_name, tc.last_name, tp.contact_person from `tabProject` tp
		left join `tabContact` tc on tp.contact_person = tc.name
		where tp.customer = 'Viatris Centre of Excellence'
		and tp.contact_person !='' and tc.first_name !=''
		and date(tp.creation) BETWEEN '{0}' and '{1}';""".format(first_date,last_date),as_dict=True)
		
		for rec in data1:
			
			row = {}
			
			if rec.first_name is not None:
				first_name = rec.first_name
			else:
				first_name = ''
			
			if rec.last_name is not None:
				last_name = rec.last_name
			else:
				last_name = ''		
						
			row['project_manager'] = first_name +' '+last_name
			
			
			dataTotalProjects = get_total_projects_client_poc(rec.contact_person,first_date,last_date)
			row['total_project'] = dataTotalProjects
			
			getCategory = frappe.db.sql("""SELECT name as project_category, 'project_category' as key_type from `tabProject Category` where status = 'Active' and name='{0}' UNION ALL 
				select name as project_category, 'country' as key_type from `tabViatris Project Country` where name='{1}' UNION ALL 
				select name as project_category, 'region' as key_type from `tabViatris Team` where name = '{2}' and status ='Active' UNION ALL 
				select name as project_category, 'therapeutic_area' as key_type from `tabTherapeutic Area` where name = '{3}' and status ='Active';""".format(project_category,viatris_project_country,region,therapeutic_area), as_dict = True)
			for rec1 in getCategory:
				category = rec1.project_category
				dataCategoryWise = get_category_count_client_poc(rec.contact_person,first_date,last_date,rec1.project_category,rec1.key_type)
				row[rec1.project_category] = dataCategoryWise
			data.append(row)
			
	else:
		data1 = frappe.db.sql("""select DISTINCT tp.project_manager from `tabProject` tp 
		where tp.customer = 'Viatris Centre of Excellence'
		and tp.project_manager !=''
		and date(creation) BETWEEN '{0}' and '{1}';""".format(first_date,last_date),as_dict=True)	
	
		for rec in data1:
			row = {}
			
			pmNameData = frappe.db.sql("""Select employee_name from `tabEmployee` where user_id='{0}';""".format(rec.project_manager), as_dict = True)
			pmname = pmNameData[0]['employee_name']
			
			row['project_manager'] = rec.project_manager + ' (' + pmname + ')'
			
			
			dataTotalProjects = get_total_projects(rec.project_manager,first_date,last_date)
			row['total_project'] = dataTotalProjects
			
			getCategory = frappe.db.sql("""SELECT name from `tabProject Category` where status='Active';""", as_dict = True)
			for rec1 in getCategory:
				category = rec1.name
				dataCategoryWise = get_category_count(rec.project_manager,first_date,last_date,category)
				row[rec1.name] = dataCategoryWise
	
			data.append(row)
		
	return data			
		

def get_last_date_of_month(year, month):
	if month == 12:
		last_date = datetime(year, month, 31)
	else:
		last_date = datetime(year, month + 1, 1) + timedelta(days=-1)
	
	return last_date.strftime("%Y-%m-%d")

def get_first_date_of_current_month(year, month):
	first_date = datetime(year, month, 1)
	return first_date.strftime("%Y-%m-%d")

def get_total_projects_client_poc(contact_person,first_date,last_date):
	if contact_person:
		data = frappe.db.sql("""select count(*) as total_projects from `tabProject` tp where tp.contact_person = '{0}'
			and tp.customer = 'Viatris Centre of Excellence' and project_current_status not in('On Hold', 'Cancelled')
			and date(tp.creation) BETWEEN '{1}' and '{2}';""".format(contact_person,first_date,last_date),as_dict=True)
		total_count = data[0]['total_projects']
		return total_count
	

def get_total_projects(project_manager,first_date,last_date):
	if project_manager:
		data = frappe.db.sql("""select count(*) as total_projects from `tabProject` tp where tp.project_manager = '{0}' 
			and tp.customer = 'Viatris Centre of Excellence' and project_current_status not in('On Hold', 'Cancelled')
			and date(tp.creation) BETWEEN '{1}' and '{2}';""".format(project_manager,first_date,last_date),as_dict=True)
		total_count = data[0]['total_projects']
		return total_count
	
def get_category_count_client_poc(contact_person,first_date,last_date,category,key_type):
	if contact_person:
		if key_type == 'project_category':
			data = frappe.db.sql("""select count(*) as total_projects_category_wise from `tabProject` tp where tp.contact_person = '{0}' 
				and tp.customer = 'Viatris Centre of Excellence' and project_current_status not in('On Hold', 'Cancelled')
				and tp.viatris_project_category = '{3}'
				and date(tp.creation) BETWEEN '{1}' and '{2}';""".format(contact_person,first_date,last_date,category), as_dict=True)	
			total_projects = data[0]['total_projects_category_wise']
		
		elif key_type == 'country':
			data = frappe.db.sql("""select count(*) as total_projects_country_wise from `tabProject` tp where tp.contact_person = '{0}' 
				and tp.customer = 'Viatris Centre of Excellence' and project_current_status not in('On Hold', 'Cancelled')
				and tp.country = '{3}'
				and date(tp.creation) BETWEEN '{1}' and '{2}';""".format(contact_person,first_date,last_date,category), as_dict=True)	
			total_projects = data[0]['total_projects_country_wise']
		
		elif key_type == 'region':
			data = frappe.db.sql("""select count(*) as total_projects_region_wise from `tabProject` tp where tp.contact_person = '{0}' 
				and tp.customer = 'Viatris Centre of Excellence' and project_current_status not in('On Hold', 'Cancelled')
				and tp.viatris_team = '{3}'
				and date(tp.creation) BETWEEN '{1}' and '{2}';""".format(contact_person,first_date,last_date,category), as_dict=True)	
			total_projects = data[0]['total_projects_region_wise']	
		
		elif key_type == 'therapeutic_area':
			data = frappe.db.sql("""select count(*) as total_projects_therapeutic_wise from `tabProject` tp where tp.contact_person = '{0}' 
				and tp.customer = 'Viatris Centre of Excellence' and project_current_status not in('On Hold', 'Cancelled')
				and tp.therapeutic_area = '{3}'
				and date(tp.creation) BETWEEN '{1}' and '{2}';""".format(contact_person,first_date,last_date,category), as_dict=True)	
			total_projects = data[0]['total_projects_therapeutic_wise']		
				
		return total_projects
			

def get_category_count(project_manager,first_date,last_date,category):	
	if project_manager:
		data = frappe.db.sql("""select count(*) as total_projects_category_wise from `tabProject` tp where tp.project_manager = '{0}' 
			and tp.customer = 'Viatris Centre of Excellence' and project_current_status not in('On Hold', 'Cancelled')
			and tp.viatris_project_category = '{3}'
			and date(tp.creation) BETWEEN '{1}' and '{2}';""".format(project_manager,first_date,last_date,category), as_dict=True)	
		total_projects_category_wise = data[0]['total_projects_category_wise']
		return total_projects_category_wise
	
def get_total_booked_business(project_manager,first_date,last_date):
	if project_manager:
		dataTotalBookedBusiness = frappe.db.sql("""select sum(project_cost) as total_booked_business from `tabProject` tp 
			where tp.project_manager = '{0}' 
			and tp.customer = 'Viatris Centre of Excellence' 
			and project_current_status not in('On Hold', 'Cancelled')
			and date(tp.ion_request_date) BETWEEN '{1}' and '{2}';""".format(project_manager,first_date,last_date), as_dict = True)
		total_booked_business = dataTotalBookedBusiness[0]['total_booked_business']
		return total_booked_business

def get_total_ion_received(project_manager,first_date,last_date):
	if project_manager:
		dataTotalBookedBusiness = frappe.db.sql("""select sum(project_cost) as total_ion_received from `tabProject` tp 
			where tp.project_manager = '{0}' 
			and tp.customer = 'Viatris Centre of Excellence' 
			and project_current_status not in('On Hold', 'Cancelled')
			and date(tp.ion_received_date) BETWEEN '{1}' and '{2}';""".format(project_manager,first_date,last_date), as_dict = True)
		total_ion_received = dataTotalBookedBusiness[0]['total_ion_received']
		return total_ion_received
	
def payment_to_be_received(project_manager,first_date,last_date):
	if project_manager:
		dataPaymentToBeReceived = frappe.db.sql("""select sum(tpr.grand_total) as payment_to_be_received from `tabPayment Request` tpr
			left join `tabProject` tp on tpr.project = tp.name
			where tp.project_manager = '{0}' and tp.customer = 'Viatris Centre of Excellence' and tpr.payment_status not in ('Overdue','Unpaid') and tpr.status not in ('Cancelled')
			and date(tpr.due_date) between '{1}' and '{2}';""".format(project_manager,first_date,last_date), as_dict = True)
		payment_to_be_received = dataPaymentToBeReceived[0]['payment_to_be_received']
		return payment_to_be_received			
	
def get_columns(filters):
	
	start_date = filters.get("from_date")
	end_date = filters.get("to_date")
	project_category = filters.get("project_category")
	viatris_project_country = filters.get("viatris_project_country")
	region = filters.get("region")
	therapeutic_area = filters.get("therapeutic_area")
	
	cols = []
	
	if project_category or viatris_project_country or region or therapeutic_area:		
		cols=[
				{
					"fieldname": "project_manager",
					"label": _("Project Manager"),
					"fieldtype": "Data",
					"width": "250"
				},
				{
					"fieldname": "total_project",
					"label": _("Total Project"),
					"fieldtype": "Data",
					"width": "100"
				},
							
			]
		start_date = filters.get("from_date")
		end_date = filters.get("to_date")
		
		today = datetime.today()
		year = today.year
		month = today.month
		
		if start_date:
			first_date = start_date
		else:
			first_date = get_first_date_of_current_month(year,month)
			
		if end_date:
			last_date = end_date
		else:
			last_date = get_last_date_of_month(year, month)
			
		getTeam = frappe.db.sql("""SELECT name as project_category from `tabProject Category` where status = 'Active' and name='{0}' UNION ALL 
			select name as project_coutry from `tabViatris Project Country` where name='{1}' UNION ALL 
			select name as region from `tabViatris Team` where name = '{2}' and status ='Active' UNION ALL 
			select name as therapeutic_area from `tabTherapeutic Area` where name = '{3}' and status ='Active';""".format(project_category,viatris_project_country,region,therapeutic_area), as_dict = True)
		
		for rec1 in getTeam:
			row = {}
			row["fieldname"] = rec1.project_category
			row["label"] = rec1.project_category
			row["fieldtype"] = "Data"
			cols.append(row)
	else:
		cols=[
				{
					"fieldname": "project_manager",
					"label": _("Project Manager"),
					"fieldtype": "Data",
					"width": "250"
				},
				{
					"fieldname": "total_project",
					"label": _("Total Project"),
					"fieldtype": "Data",
					"width": "100"
				},
							
			]
		start_date = filters.get("from_date")
		end_date = filters.get("to_date")
		
		today = datetime.today()
		year = today.year
		month = today.month
		
		if start_date:
			first_date = start_date
		else:
			first_date = get_first_date_of_current_month(year,month)
			
		if end_date:
			last_date = end_date
		else:
			last_date = get_last_date_of_month(year, month)
			
		getTeam = frappe.db.sql("""SELECT name from `tabProject Category` where status = 'Active';""", as_dict = True)
		
		for rec1 in getTeam:
			row = {}
			row["fieldname"] = rec1.name
			row["label"] = rec1.name
			row["fieldtype"] = "Data"
			cols.append(row)					
	
	return cols