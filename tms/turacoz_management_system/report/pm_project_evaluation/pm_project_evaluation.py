# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
from collections import Counter
import datetime

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	from_date=filters.get("from_date")
	to_date=filters.get("to_date")
	data = []
	
	data1 = frappe.db.sql("""select manager_name,`tabProject`.name,project_current_status,project_title,customer,contact_person,
		expected_start_date,turacoz_start_date,DATEDIFF(NOW(),turacoz_start_date) as 'days',expected_end_date,expected_hour,actual_time, 
		`tpd`.deliverable as document_deliverable,
						`tpd`.start_date,`tpd`.end_date,`tpd`.client_sent_date,`tpd`.comment_received_date,
						`tpd`.input_from_client,`tpd`.internal_remarks,`tpd`.revision_start_date,
						`tpd`.revision_end_date,`tpd`.journal_resubmission
		from `tabProject` 
		left join (select * from `tabProject New Update`) as `PU` on (`PU`.name=`tabProject`.name)
		left join (select * from `tabProject Update Data` order by parent desc) as `tpd` on (tpd.parent=`PU`.name)
		where customer not in ('Viatris Centre of Excellence','Turacoz Healthcare Solution Pvt Ltd','Turacoz Solutions PTE Ltd') and project_current_status not in ('Completed','Cancelled')
		and project_type ='External'
		group by `tabProject`.name
		order by manager_name,project_current_status;""", as_dict = True)
	
	for rec in data1:
		row = {}
		
		row['manager_name'] = rec.manager_name
		row['name'] = rec.name
		row['project_current_status'] = rec.project_current_status
		if rec.project_current_status == 'Completed Technically':
			row["tc"] = 'TC'
		else:
			row["tc"] = 'TP'
		data2 = frappe.db.sql("""select * from `tabSales Invoice` where project='{0}' and status='Paid'""".format(rec.name),as_dict=True)
		if data2:
			row["fc"] = 'FC'
		else:
			row["fc"] = 'FP'
		row['project_title'] = rec.project_title
		row['customer'] = rec.customer
		row['contact_person'] = rec.contact_person
		row['expected_start_date'] = rec.expected_start_date
		row['turacoz_start_date'] = rec.turacoz_start_date
		row['days'] = rec.days
		row['expected_end_date'] = rec.expected_end_date
		row['expected_hour'] = rec.expected_hour
		row['actual_time'] = rec.actual_time
		row['document_deliverable'] = rec.document_deliverable
		row['start_date'] = rec.start_date
		row['end_date'] = rec.end_date
		row['client_sent_date'] = rec.client_sent_date
		row['internal_remarks'] = rec.internal_remarks
		
		data.append(row)
	
	return data

def get_columns(filters):
	cols = []
	cols = [
		{
			"fieldname": "manager_name",
			"label": _("Project Manager"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "name",
			"label": _("Project Code"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "project_current_status",
			"label": _("Project Status"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "tc",
			"label": _("Technically Closed"),
			"fieldtype": "Data",
			"width": "100"
		},		{
			"fieldname": "fc",
			"label": _("Financially Closed"),
			"fieldtype": "Data",
			"width": "100"
		},
		{
			"fieldname": "project_title",
			"label": _("Project Title"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "contact_person",
			"label": _("Client PoC"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "expected_start_date",
			"label": _("Expected Start Date"),
			"fieldtype": "Date",
			"width": "200"
		},
		{
			"fieldname": "turacoz_start_date",
			"label": _("Actual Start Date"),
			"fieldtype": "Date",
			"width": "200"
		},
		{
			"fieldname": "expected_end_date",
			"label": _("Expected End Date"),
			"fieldtype": "Date",
			"width": "200"
		},
		{
			"fieldname": "days",
			"label": _("Process Days"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "expected_hour",
			"label": _("Expected Hours"),
			"fieldtype": "Float",
			"width": "200"
		},
		{
			"fieldname": "actual_time",
			"label": _("Actual Hours"),
			"fieldtype": "Float",
			"width": "200"
		},
		{
			"fieldname": "document_deliverable",
			"label": _("Document Deliverable"),
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"fieldname": "start_date",
			"label": _("Deliverable Start Date"),
			"fieldtype": "Date",
			"width": "200"
		},
		{
			"fieldname": "end_date",
			"label": _("Deliverable End Date"),
			"fieldtype": "Date",
			"width": "200"
		},	
		{
			"fieldname": "client_sent_date",
			"label": _("Deliverable Sent to Client"),
			"fieldtype": "Date",
			"width": "200"
		},
		{
			"fieldname": "internal_remarks",
			"label": _("Deliverable Remark"),
			"fieldtype": "Data",
			"width": "200"
		},	
	]
	
	return cols
