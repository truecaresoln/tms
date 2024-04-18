# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
from forex_python.converter import CurrencyRates
import math


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data

def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	overview_status = filters.get("overview_status")
	detailed_view = filters.get("detailed_view")
	excluding_viatris = filters.get("excluding_viatris")
	data = []
	
		
	getProjectStatus = frappe.db.sql("""select name from `tabProject Status List` tpsl where name not in ('pending','Open','Cancelled') ORDER BY FIELD(name,'Yet to Start','Ongoing','Under Client Review','Under Journal Review','On Hold','Completed');""", as_dict = True)
	for recprostatus in getProjectStatus:
		row = {}
		row1 = {}
		row2 = {}
		row3 = {}
		row['project_status'] = recprostatus.name
		row1['project_status'] = 'Total Received'
		row2['project_status'] = 'Pending Amount'
		row3['project_status'] = '--------------------'
		if recprostatus.name == 'Completed':
			getProjects = frappe.db.sql("""select tp.name, tp.project_current_status from `tabProject` tp where
			tp.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_type = 'External' 
			and tp.project_current_status = '{0}' and turacoz_start_date>='{1}';""".format(recprostatus.name,from_date),as_dict = True)
		else:				
			getProjects = frappe.db.sql("""select tp.name, tp.project_current_status from `tabProject` tp where
			tp.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_type = 'External' 
			and tp.project_current_status = '{0}';""".format(recprostatus.name),as_dict = True)
		total_cost = 0
		total_received = 0
		for recprojects in getProjects:
			getTotalAmountAllProject = frappe.db.sql("""select tsi.grand_total,tsi.currency, (tsi.grand_total*tcer.rate_in_inr) as total_amount_inr from `tabSales Invoice` tsi
				left join `tabCurrency Exchange Rate` tcer on tsi.currency = tcer.currency 
				where tsi.project = '{0}' and tsi.status not in ('Cancelled');""".format(recprojects.name), as_dict = True)
			for rec2 in getTotalAmountAllProject:
				if rec2.total_amount_inr:
					total_cost += rec2.total_amount_inr
				else:
					total_cost += 0	
			
			getReceivedTotal = frappe.db.sql("""select sum(tpr.grand_total) as grand_total, sum(tpr.grand_total*tcer.rate_in_inr) as total_amount_inr from `tabPayment Request` tpr
					left join `tabCurrency Exchange Rate` tcer on tpr.currency = tcer.currency 
					where tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tpr.project = '{0}' and tpr.status not in ('Cancelled') and tpr.payment_status = 'Paid';""".format(recprojects.name), as_dict = True)
			
			for recreceivedtot in getReceivedTotal:
				if recreceivedtot.total_amount_inr:
					total_received += recreceivedtot.total_amount_inr
				else:
					total_received += 0			
				
		row['total_projects_amount'] = round(total_cost,2)
		
		row1['total_projects_amount'] = round(total_received,2)
			
		total_all_pending = round(total_cost,2)-round(total_received,2)
			
		row2['total_projects_amount'] = round(total_all_pending,2)
			
		getPMNames = frappe.db.sql("""select tp.project_manager,te.employee_name from `tabProject` tp 
			left join `tabEmployee` te on tp.project_manager = te.user_id
			where te.status = 'Active' and
			tp.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_type = 'External' and tp.project_current_status not in ('Completed', 'Cancelled', 'Yet to Start')
			group by tp.project_manager;""", as_dict = True)
			
		for recpms in getPMNames:
			pmid = recpms.project_manager
			pmfield_name = recpms.employee_name
			total_cost_pms = 0
			total_received_pms = 0
			
			if recprostatus.name == 'Completed':	
				getProjectsPms = frappe.db.sql("""select tp.name, tp.project_current_status from `tabProject` tp where
					tp.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_type = 'External' 
					and tp.project_current_status = '{0}' and tp.project_manager='{1}' and turacoz_start_date>='{2}';""".format(recprostatus.name,pmid,from_date),as_dict = True)
			else:
				getProjectsPms = frappe.db.sql("""select tp.name, tp.project_current_status from `tabProject` tp where
					tp.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_type = 'External' 
					and tp.project_current_status = '{0}' and tp.project_manager='{1}';""".format(recprostatus.name,pmid),as_dict = True)
				
			for recpmsProject in getProjectsPms:
				getTotalAmountAllProjectPMs = frappe.db.sql("""select tsi.grand_total,tsi.currency, (tsi.grand_total*tcer.rate_in_inr) as total_amount_inr from `tabSales Invoice` tsi
				left join `tabCurrency Exchange Rate` tcer on tsi.currency = tcer.currency 
				where tsi.project = '{0}' and tsi.status not in ('Cancelled');""".format(recpmsProject.name), as_dict = True)
				
				for recAmountPMs in getTotalAmountAllProjectPMs:
					if recAmountPMs.total_amount_inr:
						total_cost_pms += recAmountPMs.total_amount_inr
					else:
						total_cost_pms += 0
						
				getReceived = frappe.db.sql("""select sum(tpr.grand_total) as grand_total, sum(tpr.grand_total*tcer.rate_in_inr) as total_amount_inr from `tabPayment Request` tpr
					left join `tabCurrency Exchange Rate` tcer on tpr.currency = tcer.currency 
					where tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tpr.project = '{0}' and tpr.status not in ('Cancelled') and tpr.payment_status = 'Paid';""".format(recpmsProject.name), as_dict = True)
			
				for recreceived in getReceived:
					if recreceived.total_amount_inr:
						total_received_pms += recreceived.total_amount_inr
					else:
						total_received_pms += 0			
					
			row[pmfield_name] = round(total_cost_pms,2)		
				
			row1[pmfield_name] = round(total_received_pms,2)
			
			total_pending = round(total_cost_pms,2)-round(total_received_pms,2)
			
			row2[pmfield_name] = round(total_pending,2)
				
		data.append(row)	
		data.append(row1)
		data.append(row2)
		data.append(row3)
		
	
	return data

def get_columns(filters):
	cols = []
	cols = [
		{
			"fieldname": "project_status",
			"label": _("Project Status"),
			"fieldtype": "Data",
			"width": "150"
		},
		{
			"fieldname": "total_projects_amount",
			"label": _("Total Amount"),
			"fieldtype": "Data",
			"width": "150"
		},
	]
	
	getPMNames = frappe.db.sql("""select tp.project_manager,te.employee_name from `tabProject` tp 
		left join `tabEmployee` te on tp.project_manager = te.user_id
		where te.status = 'Active' and
		tp.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_type = 'External' and tp.project_current_status not in ('Completed', 'Cancelled', 'Yet to Start')
		group by tp.project_manager;""", as_dict = True)
	for rec in getPMNames:
		row = {}
		row["fieldname"] = rec.employee_name
		row["label"] = rec.employee_name
		row["fieldtype"] = "Data"
		cols.append(row)
		
	return cols	