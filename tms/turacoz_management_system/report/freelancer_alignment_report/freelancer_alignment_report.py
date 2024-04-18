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
	freelancer = filters.get("freelancer")
	task_status = filters.get("task_status")
	data = []
	
	if freelancer:
		freelancer1 = " and tf.name = '%s'" %freelancer
	else:
		freelancer1 = ''	
	
	data1 = frappe.db.sql("""select tf.name as freelancer_id,tf.freelancer_name,tfpd.freelancer_feedback_project_id as freelancer_proj_id,tfpd.project,tfpd.role,tfpd.type_of_documents,
			tfpd.start_date as task_start_date,tfpd.project_close_date as task_end_date,tp.project_title,tp.customer,
			tp.project_current_status,tp.expected_end_date,tfpd.status,tfpd.actual_close_date,tp.manager_name from `tabFreelancer` tf 
			left join `tabFreelancer Feedback Project Detail` tfpd on tf.name =tfpd.parent
			left join `tabProject` tp on tfpd.project = tp.name 
			where tp.project_current_status not in ('Completed','Completed Technically','Cancelled') and tfpd.status='{0}' {1};""".format(task_status,freelancer1), as_dict=True)
	
	for rec in data1:
		rows = {}
		rows['name'] = rec.freelancer_id
		rows['freelancer_name'] = rec.freelancer_name
		rows['project'] = rec.project
		rows['manager_name'] = rec.manager_name
		rows['task_status'] = rec.status
		rows['role'] = rec.role
		rows['deliverable'] = rec.type_of_documents
		rows['task_start_date'] = rec.task_start_date
		rows['task_end_date'] = rec.task_end_date
		rows['project_title'] = rec.project_title
		rows['client'] = rec.customer
		rows['project_status'] = rec.project_current_status
		rows['expected_end_date'] = rec.expected_end_date
		rows['action'] = '<button style=''color:white;background-color:green;'' type=''button'' onClick= ''consoleerp_hi("{0}","{1}","{2}","{3}","{4}","{5}")''>Action</button>' .format(rec.freelancer_proj_id,rec.project,rec.task_start_date,rec.task_end_date,rec.status,rec.actual_close_date)
		
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
				"fieldname": "task_status",
				"label": ("Task Status"),
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
				"fieldname": "client",
				"label": ("Client"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "project_status",
				"label": ("Project Status"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "expected_end_date",
				"label": ("Project Expected End Date"),
				"fieldtype": "Date",
				"width": "150"
			},
			{
				"fieldname": "action",
				"label": ("Action"),
				"fieldtype": "Button",
				"width": "150"
			}
		]
	return cols	

@frappe.whitelist()
def update_planned(proje_id,status,actual_close_date):

 	data1 = frappe.db.sql("""update `tabFreelancer Feedback Project Detail` set status='{0}',actual_close_date='{1}' where freelancer_feedback_project_id={2};""".format(status,actual_close_date,proje_id))
 	
 	return 1