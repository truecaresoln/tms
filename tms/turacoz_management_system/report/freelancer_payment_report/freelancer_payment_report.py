# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

# import frappe

from __future__ import unicode_literals
from frappe import _
import frappe
from datetime import datetime
from datetime import timedelta
import calendar
import pendulum
import datetime



def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	freelancer = filters.get("freelancer")
	data = []
	
	if(from_date):
		combine1="where date(tfpd.start_date)>='%s'" %from_date
	else:
		combine1=""
			
	if(to_date):
		combine2="and date(tfpd.start_date)<='%s'" %to_date
	else:
		combine2=""

	if freelancer:
		freelancer1 = " and tf.name = '%s'" %freelancer
	else:
		freelancer1 = ''	
	
	data1 = frappe.db.sql("""select tf.name as freelancer_id,tf.freelancer_name,tfpd.name as freelancer_proj_id,tfpd.project,tfpd.role,tfpd.type_of_documents,
			tfpd.start_date as task_start_date,tfpd.project_close_date as task_end_date,tp.project_title,tp.customer,
			tp.project_current_status,tp.expected_end_date,tfpd.status,tfpd.total as total,tfpd.payment_status as payment_status,tp.manager_name from `tabFreelancer` tf 
			left join `tabFreelancer Feedback Project Detail` tfpd on tf.name =tfpd.parent
			left join `tabProject` tp on tfpd.project = tp.name 
			{0} {1} {2};""".format(combine1,combine2,freelancer1), as_dict=True)
	
	for rec in data1:
		rows = {}
		rows['name'] = rec.freelancer_id
		rows['freelancer_name'] = rec.freelancer_name
		rows['project'] = rec.project
		rows['manager_name'] = rec.manager_name
		rows['project_title'] = rec.project_title
		rows['role'] = rec.role
		rows['task_status'] = rec.status
		rows['total'] = rec.total
		rows['payment_status'] = rec.payment_status
		rows['deliverable'] = rec.type_of_documents
		rows['task_start_date'] = rec.task_start_date
		rows['task_end_date'] = rec.task_end_date
		rows['project_status'] = rec.project_current_status
		rows['expected_end_date'] = rec.expected_end_date
		rows['client'] = rec.customer
		
		data.append(rows)
		
	return data	
	
def get_columns(filters):
	freelancer = filters.get("freelancer")
	cols = []
	cols=[
			{
				"fieldname": "name",
				"label": ("Freelancer ID"),
				"fieldtype": "Link",
				"options": "Freelancer",
				"width": "150"
			},
			{
				"fieldname": "freelancer_name",
				"label": ("Freelancer Name"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "project",
				"label": ("Project"),
				"fieldtype": "Link",
				"options": "Project",
				"width": "150"
			},
			{
				"fieldname": "manager_name",
				"label": ("Project Manager"),
				"fieldtype": "Data",
				"width": "150"
			},	
			{
				"fieldname": "project_title",
				"label": ("Project Title"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "role",
				"label": ("Role"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "total",
				"label": ("Amount Payable"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "payment_status",
				"label": ("Payment Status"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "task_status",
				"label": ("Task Status"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "deliverable",
				"label": ("Deliverable"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "task_start_date",
				"label": ("Task Start Date"),
				"fieldtype": "Date",
				"width": "150"
			},
			{
				"fieldname": "task_end_date",
				"label": ("Task End Date"),
				"fieldtype": "Date",
				"width": "150"
			},
			{
				"fieldname": "project_status",
				"label": ("Project Status"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "client",
				"label": ("Client"),
				"fieldtype": "Data",
				"width": "150"
			},
		]
	return cols	