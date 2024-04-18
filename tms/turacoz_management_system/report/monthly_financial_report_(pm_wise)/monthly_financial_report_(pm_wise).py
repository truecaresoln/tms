# Copyright (c) 2023, RSA and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
from collections import Counter
from datetime import date
from datetime import datetime

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data

def get_data(filters):
	todays_date = date.today()
	firstDateofCurrentMonth = date.today().replace(day=1)
	year = todays_date.year
	month_name = todays_date.strftime("%B")
	dt1 = firstDateofCurrentMonth
	
	data=[]
	row={}
	row['months'] = month_name+' '+str(year)
	data.append(row)
	data1=frappe.db.sql("""select user_id,employee_name from `tabTeam Assignment` where team='Non-Viatris'""",as_dict=True)
	for rec in data1:
		pm = rec.user_id
		pm1 = rec.employee_name
		row={}
		row['months'] = pm1
		data.append(row)
		invoicestoberaised = float()
		invoicestoberaisedinINR = float()
		invoicesraised = float()
		invoicesraisedinINR = float()
		paymentexpected = float()
		paymentexpectedinINR = float()
		paymentexpected1 = float()
		paymentexpectedinINR1 = float()
		data2=frappe.db.sql("""select tp.name,tp.project_title,tp.customer,tp.contact_person,tp.manager_name,tps.payment_amount as total_amount,
				tsi.currency,ter.rate_in_inr * tps.payment_amount as total_inr from `tabSales Invoice` tsi 
				left join `tabPayment Schedule` tps on tsi.name = tps.parent
				left join `tabProject` tp on tsi.project = tp.name
				left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
				WHERE tsi.status not in ('Paid','Cancelled') and tp.project_manager='{2}'
				and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
				MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}'
				order by tsi.currency""".format(month_name,year,pm),as_dict=True)
		
		if data2==[]:
			print(pm)
		else:
			row={}
			row['months'] = 'Invoices to be Raised'
			data.append(row)
			for rec1 in data2:
				row={}
				row['name']=rec1.name
				row['project_title']=rec1.project_title
				row['customer']=rec1.customer
				row['contact_person']=rec1.contact_person
				row['currency']=rec1.currency
				row['total_amount']=rec1.total_amount
				invoicestoberaised += float(rec1.total_amount)
				invoicestoberaised = round(invoicestoberaised, 2)	
				row['total_inr']=rec1.total_inr
				invoicestoberaisedinINR += float(rec1.total_inr)
				invoicestoberaisedinINR = round(invoicestoberaisedinINR, 2)	
				data.append(row)
			row={}
			row['total_inr'] = invoicestoberaisedinINR
			row['contact_person']='<b>Total</b>'
			data.append(row)

		data5=frappe.db.sql("""select tp.name,tp.project_title,tp.customer,tp.contact_person,tp.manager_name,tpr.grand_total as total_amount,
		tpr.invoice_currency,ter.rate_in_inr * tpr.grand_total as total_inr,tpr.name as invoice
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
		left join `tabProject` tp on tpr.project = tp.name
		WHERE tp.project_type='External' and tpr.status != 'Draft' and tpr.payment_status not in ('Cancelled','Paid')  and tp.project_manager='{2}' and tpr.invoice_date is not NULL and
		tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}'
		order by tpr.invoice_currency""".format(month_name,year,pm),as_dict=True)
		
		if data5==[]:
			print(pm)
		else:
			row={}
			row['months'] = "Invoices Raised in "+ month_name
			data.append(row)
			for rec1 in data5:
				row={}
				row['months'] = rec1.invoice
				row['name']=rec1.name
				row['project_title']=rec1.project_title
				row['customer']=rec1.customer
				row['contact_person']=rec1.contact_person
				row['currency']=rec1.invoice_currency
				row['total_amount']=rec1.total_amount
				invoicesraised += float(rec1.total_amount)
				invoicesraised = round(invoicesraised, 2)	
				row['total_inr']=rec1.total_inr
				invoicesraisedinINR += float(rec1.total_inr)
				invoicesraisedinINR = round(invoicesraisedinINR, 2)	
				data.append(row)
			row={}
			row['total_inr'] = invoicesraisedinINR
			row['contact_person']='<b>Total</b>'
			data.append(row)
			row={}
			row['total_inr'] = invoicestoberaisedinINR + invoicesraisedinINR
			row['contact_person']="<b>Total Invoices for " + month_name + "</b>"
			data.append(row)
			
		data3=frappe.db.sql("""select tp.name,tp.project_title,tp.customer,tp.contact_person,tp.manager_name,tpr.grand_total as total_amount,
				tpr.invoice_currency,ter.rate_in_inr * tpr.grand_total as total_inr,tpr.name as invoice 
				from `tabPayment Request` tpr 
				left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
				left join `tabProject` tp on tpr.project = tp.name
				WHERE tp.project_type='External' and tpr.payment_status not in ('Cancelled','Paid') and tpr.due_date is not NULL and tp.project_manager='{2}' and 
				tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
				MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}'
				order by tpr.invoice_currency """.format(month_name,year,pm),as_dict=True)
		
		if data3==[]:
			print(pm)
		else:
			row={}
			row['months'] = "Pending Payments of "+ month_name 
			data.append(row)
			for rec1 in data3:
				row={}
				row['months'] = rec1.invoice
				row['name']=rec1.name
				row['project_title']=rec1.project_title
				row['customer']=rec1.customer
				row['contact_person']=rec1.contact_person
				row['currency']=rec1.invoice_currency
				row['total_amount']=rec1.total_amount
				paymentexpected += float(rec1.total_amount)
				paymentexpected = round(paymentexpected, 2)	
				row['total_inr']=rec1.total_inr
				paymentexpectedinINR += float(rec1.total_inr)
				paymentexpectedinINR = round(paymentexpectedinINR, 2)	
				data.append(row)
			row={}
			row['total_inr'] = paymentexpectedinINR
			row['contact_person']='<b>Total</b>'
			data.append(row)
			
		data4=frappe.db.sql("""select tp.name,tp.project_title,tp.customer,tp.contact_person,tp.manager_name,tpr.grand_total as total_amount,
				tpr.invoice_currency,ter.rate_in_inr * tpr.grand_total as total_inr,tpr.name as invoice 
				from `tabPayment Request` tpr 
				left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
				left join `tabProject` tp on tpr.project = tp.name
				WHERE tp.project_type='External' and tpr.payment_status not in ('Cancelled','Paid') and tpr.due_date is not NULL and tp.project_manager='{1}' and 
				tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
				tpr.due_date< '{0}' order by tpr.invoice_currency """.format(dt1,pm),as_dict=True)
		print(dt1)
		if data4==[]:
			print(pm)
		else:
			row={}
			row['months'] = "Pending Payments Before "+ month_name
			data.append(row)
			for rec1 in data4:
				row={}
				row['months'] = rec1.invoice
				row['name']=rec1.name
				row['project_title']=rec1.project_title
				row['customer']=rec1.customer
				row['contact_person']=rec1.contact_person
				row['currency']=rec1.invoice_currency
				row['total_amount']=rec1.total_amount
				paymentexpected1 += float(rec1.total_amount)
				paymentexpected1 = round(paymentexpected1, 2)	
				row['total_inr']=rec1.total_inr
				paymentexpectedinINR1 += float(rec1.total_inr)
				paymentexpectedinINR1 = round(paymentexpectedinINR1, 2)	
				data.append(row)
			row={}
			row['total_inr'] = paymentexpectedinINR1
			row['contact_person']='<b>Total</b>'
			data.append(row)
			row={}
			row['total_inr'] = paymentexpectedinINR + paymentexpectedinINR1
			row['contact_person']="<b>Total Payment Due on " + month_name + "</b>"
			data.append(row)
			
		data6=frappe.db.sql("""select tp.name,tp.project_title,tp.customer,tp.contact_person,tp.manager_name,tpr.grand_total as total_amount,
				tpr.invoice_currency,ter.rate_in_inr * tpr.grand_total as total_inr,tpr.name as invoice 
				from `tabPayment Request` tpr 
				left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
				left join `tabProject` tp on tpr.project = tp.name
				WHERE tp.project_type='External' and tpr.payment_status in ('Paid') and tp.project_manager='{2}' and 
				tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
				MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' order by tpr.invoice_currency """.format(month_name,year,pm),as_dict=True)
		print(dt1)
		if data6==[]:
			print(pm)
		else:
			row={}
			row['months'] = "Payments Received On "+ month_name
			data.append(row)
			paymentexpected1 = float()
			paymentexpectedinINR1 = float()
			for rec1 in data6:
				row={}
				row['months'] = rec1.invoice
				row['name']=rec1.name
				row['project_title']=rec1.project_title
				row['customer']=rec1.customer
				row['contact_person']=rec1.contact_person
				row['currency']=rec1.invoice_currency
				row['total_amount']=rec1.total_amount
				paymentexpected1 += float(rec1.total_amount)
				paymentexpected1 = round(paymentexpected1, 2)	
				row['total_inr']=rec1.total_inr
				paymentexpectedinINR1 += float(rec1.total_inr)
				paymentexpectedinINR1 = round(paymentexpectedinINR1, 2)	
				data.append(row)
			row={}
			row['total_inr'] = paymentexpectedinINR1
			row['contact_person']='<b>Total</b>'
			data.append(row)

	return data

def get_columns(filters):
	cols=[]
	cols = [
			{
				"fieldname": "months",
				"label": ("Particulars"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "name",
				"label": ("Project Code"),
				"fieldtype": "Link",
				"options": "Project",
				"width": "140"
			},
			{
				"fieldname": "project_title",
				"label": ("Project"),
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
				"fieldname": "currency",
				"label": ("Currency"),
				"fieldtype": "Data",
				"width": "50"
			},
			{
				"fieldname": "total_amount",
				"label": ("Amount"),
				"fieldtype": "Data",
				"width": "80"
			},
			{
				"fieldname": "total_inr",
				"label": ("Total Amount(in INR)"),
				"fieldtype": "Currency",
				"width": "100"
			}
		]
	return cols