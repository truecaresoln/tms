# Copyright (c) 2024, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
from collections import Counter
from datetime import date
# import datetime
from forex_python.converter import CurrencyRates
import math
from dateutil.relativedelta import relativedelta
from datetime import timedelta


def execute(filters=None):
	columns, data = [], []
	key = filters.get("key") if filters else None
	if key:
		keys = key
	else:
		keys = ''	
	columns = get_columns(keys)
	data = get_data(keys)
	return columns, data

def get_data(keys):
	todays_date = date.today()
	formatted_date = todays_date.strftime("%d-%m-%Y")
	firstDateofCurrentMonth = date.today().replace(day=1)
	next_month = date.today().replace(day=28) + timedelta(days=4)
	lastDateofCurrentMonth = next_month - timedelta(days=next_month.day)
	year = todays_date.year
	month_name = todays_date.strftime("%B")
	last_month = date.today() - relativedelta(months=1)
	last_month_name = last_month.strftime("%B")
	last_month_year = last_month.year

	year_start_date_data = get_fiscal_year()
	year_start_date = year_start_date_data[0]['year_start_date']

	start_of_week = todays_date - timedelta(days=todays_date.weekday())
	end_of_week = start_of_week + timedelta(days=6)

	data = []
	
	if keys:
		if keys == 'total_unraised_amount_till_date':
			total_unraised_amountTillDate = total_unraised_amount_till_date(todays_date)
			for totalUnraisedAmountTillDate in total_unraised_amountTillDate:
				row = {}
				row["company"] = totalUnraisedAmountTillDate.company
				row["project"] = totalUnraisedAmountTillDate.project
				row["customer"] = totalUnraisedAmountTillDate.customer
				row["due_date"] = totalUnraisedAmountTillDate.due_date
				row["bd_person"] = totalUnraisedAmountTillDate.bd_name
				row["project_manager"] = totalUnraisedAmountTillDate.manager_name
				row["amount"] = round(totalUnraisedAmountTillDate.total_inr, 2)
				data.append(row)
			return data	

		elif keys == 'actual_invoice_raised_mtd':
			actual_invoice_raisedMTD = actual_invoice_raised_mtd(month_name,year)
			for actualInvoiceRaisedMTD in actual_invoice_raisedMTD:
				row = {}
				row["invoice_no"] = actualInvoiceRaisedMTD.name
				row["invoice_date"] = actualInvoiceRaisedMTD.invoice_date
				row["customer"] = actualInvoiceRaisedMTD.customer_name
				row["company"] = actualInvoiceRaisedMTD.company
				row["project"] = actualInvoiceRaisedMTD.project
				row["actual_currency"] = actualInvoiceRaisedMTD.currency
				row["amount_actual"] = actualInvoiceRaisedMTD.grand_total
				row["amount_inr"] = actualInvoiceRaisedMTD.total_inr
				data.append(row)
			return data	

		elif keys == 'actual_invoice_raised_ytd':
			actual_invoice_raisedYTD = actual_invoice_raised_ytd(year_start_date,todays_date)
			for actualInvoiceRaisedYTD in actual_invoice_raisedYTD:
				row = {}
				row["invoice_no"] = actualInvoiceRaisedYTD.name
				row["invoice_date"] = actualInvoiceRaisedYTD.invoice_date
				row["customer"] = actualInvoiceRaisedYTD.customer_name
				row["company"] = actualInvoiceRaisedYTD.company
				row["project"] = actualInvoiceRaisedYTD.project
				row["actual_currency"] = actualInvoiceRaisedYTD.currency
				row["amount_actual"] = actualInvoiceRaisedYTD.grand_total
				row["amount_inr"] = actualInvoiceRaisedYTD.total_inr
				data.append(row)
			return data	


		elif keys == 'payment_received_mtd':
			payment_received_MTD = payment_received_mtd(month_name,year)
			for paymentReceived_MTD in payment_received_MTD:
				row = {}
				row["invoice_no"] = paymentReceived_MTD.name
				row["payment_date"] = paymentReceived_MTD.payment_date
				row["customer"] = paymentReceived_MTD.customer_name
				row["company"] = paymentReceived_MTD.company
				row["project"] = paymentReceived_MTD.project
				row["actual_currency"] = paymentReceived_MTD.currency
				row["amount_actual"] = paymentReceived_MTD.grand_total
				row["amount_inr"] = paymentReceived_MTD.total_inr
				data.append(row)
			return data	

		elif keys == 'payment_received_ytd':
			payment_received_YTD = payment_received_ytd(year_start_date,todays_date)
			for paymentReceived_YTD in payment_received_YTD:
				row = {}
				row["invoice_no"] = paymentReceived_YTD.name
				row["payment_date"] = paymentReceived_YTD.payment_date
				row["customer"] = paymentReceived_YTD.customer_name
				row["company"] = paymentReceived_YTD.company
				row["project"] = paymentReceived_YTD.project
				row["actual_currency"] = paymentReceived_YTD.currency
				row["amount_actual"] = paymentReceived_YTD.grand_total
				row["amount_inr"] = paymentReceived_YTD.total_inr
				data.append(row)
			return data		

		elif keys == 'planned_invoices_to_be_raised_in_week':
			planned_invoices_to_be_raised_inWeek = planned_invoices_to_be_raised_in_week(start_of_week,end_of_week)
			for plannedInvoicesToBeRaisedInWeek in planned_invoices_to_be_raised_inWeek:
				row = {}
				row["company"] = plannedInvoicesToBeRaisedInWeek.company
				row["project"] = plannedInvoicesToBeRaisedInWeek.project
				row["customer"] = plannedInvoicesToBeRaisedInWeek.customer_name
				row["due_date"] = plannedInvoicesToBeRaisedInWeek.due_date
				row["bd_person"] = plannedInvoicesToBeRaisedInWeek.bd_name
				row["project_manager"] = plannedInvoicesToBeRaisedInWeek.manager_name
				row["amount"] = round(plannedInvoicesToBeRaisedInWeek.total_inr, 2)
				data.append(row)
			return data		

		elif keys == 'planned_invoices_to_be_raised_mtd':
			planned_invoices_to_be_raisedMTD = planned_invoices_to_be_raised_mtd(month_name,year)
			for plannedInvoicesToBeRaisedMTD in planned_invoices_to_be_raisedMTD:
				row = {}
				row["company"] = plannedInvoicesToBeRaisedMTD.company
				row["project"] = plannedInvoicesToBeRaisedMTD.project
				row["customer"] = plannedInvoicesToBeRaisedMTD.customer_name
				row["due_date"] = plannedInvoicesToBeRaisedMTD.due_date
				row["bd_person"] = plannedInvoicesToBeRaisedMTD.bd_name
				row["project_manager"] = plannedInvoicesToBeRaisedMTD.manager_name
				row["amount"] = round(plannedInvoicesToBeRaisedMTD.total_inr, 2)
				data.append(row)
			return data	

		elif keys == 'payment_to_be_received_mtd':
			payment_tobe_receivedMTD = payment_to_be_received_mtd(month_name,year)
			for paymentToBeReceivedMTD in payment_tobe_receivedMTD:
				row = {}
				row["invoice_no"] = paymentToBeReceivedMTD.name
				row["payment_date"] = paymentToBeReceivedMTD.payment_date
				row["customer"] = paymentToBeReceivedMTD.customer_name
				row["company"] = paymentToBeReceivedMTD.company
				row["project"] = paymentToBeReceivedMTD.project
				row["actual_currency"] = paymentToBeReceivedMTD.currency
				row["amount_actual"] = paymentToBeReceivedMTD.grand_total
				row["amount_inr"] = paymentToBeReceivedMTD.total_inr
				data.append(row)
			return data		

		elif keys == 'payment_to_be_received_ytd':
			payment_tobe_receivedYTD = payment_to_be_received_cumulative_ytd(todays_date)
			for paymentToBeReceivedYTD in payment_tobe_receivedYTD:
				row = {}
				row["invoice_no"] = paymentToBeReceivedYTD.name
				row["payment_date"] = paymentToBeReceivedYTD.payment_date
				row["customer"] = paymentToBeReceivedYTD.customer_name
				row["company"] = paymentToBeReceivedYTD.company
				row["project"] = paymentToBeReceivedYTD.project
				row["actual_currency"] = paymentToBeReceivedYTD.currency
				row["amount_actual"] = paymentToBeReceivedYTD.grand_total
				row["amount_inr"] = paymentToBeReceivedYTD.total_inr
				data.append(row)
			return data	

def get_columns(keys):
	cols = []
	if keys == 'total_unraised_amount_till_date' or keys == 'planned_invoices_to_be_raised_in_week' or keys== 'planned_invoices_to_be_raised_mtd':
		cols = [
			{
				"fieldname": "company",
				"label": _("Company"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "project",
				"label": _("project"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "customer",
				"label": _("Customer"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "due_date",
				"label": _("Due Date"),
				"fieldtype": "Date",
				"width": "100"
			},
			{
				"fieldname": "bd_person",
				"label": _("BD Person"),
				"fieldtype": "Data",
				"width": "100"
			},
			{
				"fieldname": "project_manager",
				"label": _("Project Manager"),
				"fieldtype": "Data",
				"width": "100"
			},
			{
				"fieldname": "amount",
				"label": _("Amount in INR"),
				"fieldtype": "Currency",
				"width": "150"
			},
			{
				"fieldname": "comment",
				"label": _("Comment"),
				"fieldtype": "Button",
				"width": "100"
			},
		]
	elif keys == 'actual_invoice_raised_mtd' or keys== 'actual_invoice_raised_ytd':
		cols = [
			{
				"fieldname": "invoice_no",
				"label": _("Invoice No"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "invoice_date",
				"label": _("Invoice Date"),
				"fieldtype": "Date",
				"width": "100"
			},
			{
				"fieldname": "customer",
				"label": _("Customer"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "company",
				"label": _("Company"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "project",
				"label": _("Project"),
				"fieldtype": "Data",
				"width": "100"
			},
			{
				"fieldname": "actual_currency",
				"label": _("Actual Currency"),
				"fieldtype": "Data",
				"width": "100"
			},
			{
				"fieldname": "amount_actual",
				"label": _("Amount in actual Currency"),
				"fieldtype": "Float",
				"width": "100"
			},
			{
				"fieldname": "amount_inr",
				"label": _("Amount in INR"),
				"fieldtype": "Currency",
				"width": "150"
			},
			{
				"fieldname": "comment",
				"label": _("Comment"),
				"fieldtype": "Button",
				"width": "100"
			},
		]
	elif keys == 'payment_received_mtd' or keys== 'payment_received_ytd' or keys == 'payment_to_be_received_mtd' or keys == 'payment_to_be_received_ytd':
		cols = [
			{
				"fieldname": "invoice_no",
				"label": _("Invoice No"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "payment_date",
				"label": _("Invoice Date"),
				"fieldtype": "Date",
				"width": "100"
			},
			{
				"fieldname": "customer",
				"label": _("Customer"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "company",
				"label": _("Company"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "project",
				"label": _("Project"),
				"fieldtype": "Data",
				"width": "100"
			},
			{
				"fieldname": "actual_currency",
				"label": _("Actual Currency"),
				"fieldtype": "Data",
				"width": "100"
			},
			{
				"fieldname": "amount_actual",
				"label": _("Amount in actual Currency"),
				"fieldtype": "Float",
				"width": "100"
			},
			{
				"fieldname": "amount_inr",
				"label": _("Amount in INR"),
				"fieldtype": "Currency",
				"width": "150"
			},
			{
				"fieldname": "comment",
				"label": _("Comment"),
				"fieldtype": "Button",
				"width": "100"
			},
		]			
	return cols	

def get_fiscal_year():
	data = frappe.db.sql("""select year_start_date,year_end_date from `tabFiscal Year` tfy WHERE disabled = 0""",as_dict=True)
	return data

def total_unraised_amount_till_date(todays_date):
	data = frappe.db.sql("""select tsi.project,tsi.customer,tsi.company,tps.due_date,tp.bd_name,
		tp.manager_name,ter.rate_in_inr * tps.payment_amount as total_inr,
		tps.payment_amount as total_amount,tsi.currency
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled') and tp.project_current_status not in ('Cancelled') and tps.invoice_status = 'Unraised'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		tps.due_date <= '{0}';""".format(todays_date), as_dict = True)
	return data

def actual_invoice_raised_mtd(month_name,year):
	data = frappe.db.sql("""select tpr.name,tpr.customer_name,tpr.company,tpr.project,tpr.invoice_date,
		tpr.grand_total,tpr.currency,
		CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(ter.rate_in_inr * tpr.grand_total,0)
		END as 'total_inr'			  
		from `tabPayment Request` tpr 
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tpr.currency = ter.name
		WHERE tpr.status not in ('Paid','Cancelled')
		and tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}'
		Order by tpr.company,tpr.invoice_date,tpr.currency""".format(month_name,year),as_dict = True)
	return data

def actual_invoice_raised_ytd(year_start_date,todays_date):
	data = frappe.db.sql("""select tpr.name,tpr.customer_name,tpr.company,tpr.project,tpr.invoice_date,
		tpr.grand_total,tpr.currency,
		CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(ter.rate_in_inr * tpr.grand_total,0)
		END as 'total_inr'				  
		from `tabPayment Request` tpr 
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tpr.currency = ter.name
		WHERE tpr.status not in ('Cancelled')
		and tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		date(tpr.invoice_date) BETWEEN  '{0}' and '{1}'
		Order by tpr.company,tpr.invoice_date,tpr.currency""".format(year_start_date,todays_date),as_dict = True)
	return data

def payment_received_mtd(month_name,year):
	data = frappe.db.sql("""select tpr.name,tpr.customer_name,tpr.company,tpr.project,tpr.invoice_date,
		tpr.payment_date,tpr.grand_total,tpr.currency,
		CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(ter.rate_in_inr * tpr.grand_total,0)
		END as 'total_inr'			  
		from `tabPayment Request` tpr 
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tpr.currency = ter.name
		WHERE tpr.status not in ('Cancelled') and payment_status in ('Paid')
		and tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}'
		Order by tpr.company,tpr.payment_date,tpr.currency;""".format(month_name,year), as_dict = True)
	return data

def payment_received_ytd(year_start_date,todays_date):
	data = frappe.db.sql("""select tpr.name,tpr.customer_name,tpr.company,tpr.project,tpr.invoice_date,
		tpr.payment_date,tpr.grand_total,tpr.currency,
		CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(ter.rate_in_inr * tpr.grand_total,0)
		END as 'total_inr'
		from `tabPayment Request` tpr 
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tpr.currency = ter.name
		WHERE tpr.status not in ('Cancelled') and tpr.payment_status in ('Paid')
		and tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		date(tpr.payment_date) BETWEEN  '{0}' and '{1}'
		Order by tpr.company,tpr.invoice_date,tpr.currency""".format(year_start_date,todays_date), as_dict = True)
	return data

def planned_invoices_to_be_raised_in_week(start_of_week,end_of_week):
	data = frappe.db.sql("""select tsi.project,customer_name,tsi.company,tps.due_date,tp.bd_name,tp.manager_name,
		IFNULL(ter.rate_in_inr * tps.payment_amount,0) as total_inr,tps.payment_amount as total_amount,tsi.currency
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled')
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		date(tps.due_date) BETWEEN  '{0}' and '{1}'
		Order by tsi.company,tps.due_date,tsi.currency""".format(start_of_week,end_of_week), as_dict = True)
	return data

def planned_invoices_to_be_raised_mtd(month_name,year):
	data = frappe.db.sql("""select tsi.project,customer_name,tsi.company,tps.due_date,tp.bd_name,tp.manager_name,
		IFNULL(ter.rate_in_inr * tps.payment_amount,0) as total_inr,tps.payment_amount as total_amount,tsi.currency
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled')
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}'
		Order by tsi.company,tps.due_date,tsi.currency""".format(month_name,year), as_dict = True)
	return data

def payment_to_be_received_mtd(month_name,year):
	data = frappe.db.sql("""SELECT tpr.name,tpr.invoice_date,tpr.due_date,tpr.customer_name,
		tpr.contact_person as client_poc,tp.manager_name,tpr.company,
		tpr.invoice_currency,tpr.net_total,
		(tcer.rate_in_inr * tpr.net_total) as net_total_in_inr,tpr.total_taxes,tpr.grand_total,
		CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(tcer.rate_in_inr * tpr.grand_total,0)
		END as 'total_inr'
		FROM `tabPayment Request` tpr
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` tcer on tpr.invoice_currency = tcer.name
		WHERE tpr.payment_status in ('Unpaid','Overdue') 
		and tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')			  
		AND MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}';""".format(month_name,year), as_dict = True)
	return data

def payment_to_be_received_cumulative_ytd(todays_date):
	data = frappe.db.sql("""SELECT tpr.name,tpr.invoice_date,tpr.due_date,tpr.customer_name,
		tpr.contact_person as client_poc,tp.manager_name,tpr.company,
		tpr.invoice_currency,tpr.net_total,
		(tcer.rate_in_inr * tpr.net_total) as net_total_in_inr,tpr.total_taxes,tpr.grand_total,
		CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(tcer.rate_in_inr * tpr.grand_total,0)
		END as 'total_inr'
		FROM `tabPayment Request` tpr
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` tcer on tpr.invoice_currency = tcer.name
		WHERE tpr.payment_status in ('Unpaid','Overdue') 
		and tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')			  
		AND date(tpr.due_date) <= '{0}';""".format(todays_date), as_dict = True)
	return data



	
