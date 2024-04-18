# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
from collections import Counter
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data

def get_data(filters):
	status = filters.get("status")
	
	data = []
	
	if status:
		getPublishedData = frappe.db.sql("""SELECT  tpa.name, tpa.article_status,tpa.project,
			title_of_menuscript,tp.customer,tp.therapeutic_area,te.employee_name from `tabPublished Articles` tpa
			left join `tabProject` tp on tpa.project = tp.name
			left join `tabEmployee` te on tpa.project_manager = te.user_id
			where tpa.article_status='{0}';""".format(status), as_dict = True)
	else:
		getPublishedData = frappe.db.sql("""SELECT  tpa.name, tpa.article_status,tpa.project,
			title_of_menuscript,tp.customer,tp.therapeutic_area,te.employee_name from `tabPublished Articles` tpa
			left join `tabProject` tp on tpa.project = tp.name
			left join `tabEmployee` te on tpa.project_manager = te.user_id
			where tpa.article_status in ('In Acceptance','In Submission');""", as_dict = True)
			
	for rec in getPublishedData:
		row = {}
		row["project_code"] = rec.project
		row["project_manager"] = rec.employee_name
		row["therapeutic_area"] = rec.therapeutic_area
		row["title_of_manuscript"] = rec.title_of_menuscript
		row["client"] = rec.customer
		row["status"] = rec.article_status
				
		getPublishedArticleLog = frappe.db.sql("""select journal,link_of_journal,login_id,
		password,status,date_of_submission,remark from `tabPublished Articles Log` 
		where parent = '{0}' order by idx ASC;""".format(rec.name), as_dict = True)
		
		if getPublishedArticleLog:
			i = 1
			for rec1 in getPublishedArticleLog:
				if i == 1:
					row["journal"] = rec1.journal
					row["journal_link"] = rec1.link_of_journal
					row["submission_date"] = rec1.date_of_submission
					row["login_id"] = rec1.login_id
					row["password"] = rec1.password
					row["remark"] = rec1.remark
					data.append(row)
					i +=1
				else:
					row1 = {}
					row1["journal"] = rec1.journal
					row1["journal_link"] = rec1.link_of_journal
					row1["submission_date"] = rec1.date_of_submission
					row1["login_id"] = rec1.login_id
					row1["password"] = rec1.password
					row1["remark"] = rec1.remark
					data.append(row1)	
		
		
	
	return data

def get_columns(filters):
	cols = []
	
	cols=[
			{
				"fieldname": "project_code",
				"label": ("Project Code"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "project_manager",
				"label": ("Project Manager"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "therapeutic_area",
				"label": ("Therapeutic Area"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "title_of_manuscript",
				"label": ("Title of Manuscript"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "client",
				"label": ("Client"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "status",
				"label": ("Status"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "journal",
				"label": ("Journal"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "journal_link",
				"label": ("Link of Journal Submission"),
				"fieldtype": "Data",
				"width": "300"
			},
			{
				"fieldname": "login_id",
				"label": ("Login ID"),
				"fieldtype": "Data",
				"width": "180"
			},
			{
				"fieldname": "password",
				"label": ("Password"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "submission_date",
				"label": ("Date of Submission"),
				"fieldtype": "Date",
				"width": "150"
			},
			{
				"fieldname": "remark",
				"label": ("Remark"),
				"fieldtype": "Data",
				"width": "300"
			},
		]
			
	return cols
