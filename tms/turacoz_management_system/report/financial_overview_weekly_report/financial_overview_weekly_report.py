# Copyright (c) 2022, RSA and contributors
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
	columns = get_columns()
	data = get_data()
	return columns, data

def get_data():
	data = []
	row = {}
	
	todays_date = date.today()
	firstDateofCurrentMonth = date.today().replace(day=1)
	next_month = date.today().replace(day=28) + timedelta(days=4)
	lastDateofCurrentMonth = next_month - timedelta(days=next_month.day)
	year = todays_date.year
	month_name = todays_date.strftime("%B")
	last_month = date.today() - relativedelta(months=1)
	last_month_name = last_month.strftime("%B")
	last_month_year = last_month.year
		
	
	row["particular"] = "New PO " + "("+ month_name + " " + str(year) +")"
 # data2 = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
 # 		tso.currency,count(tp.name) as project_count,ter.rate_in_inr * sum(tso.net_total) as total_inr  
 # 		from `tabSales Order` tso 
 # 		left join `tabProject` tp on tso.project = tp.name
 # 		left join `tabCurrency Exchange Rate` ter on tso.currency  = ter.name
 # 		WHERE tp.customer  not in ('Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
 # 		and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
 # 		and tp.project_current_status not in ('Cancelled') GROUP by tso.currency""".format(month_name,year), as_dict=True)
	data2 = frappe.db.sql("""select sum(tpf.amount),tpf.currency,
		ter.rate_in_inr * sum(tpf.amount) as total_inr
		from `tabProject Final Over Hubspots` tpf
		left join `tabCurrency Exchange Rate` ter on tpf.currency = ter.name WHERE
		MONTHNAME(STR_TO_DATE(MONTH(tpf.close_date),'%m')) = '{0}' and YEAR(tpf.close_date) = '{1}'
		group by tpf.currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr2 = float()	
	for rec2 in data2:
		final_total_amount_inr2 += float(rec2.total_inr)
		final_total_amount_inr2 = round(final_total_amount_inr2, 2)
	row["total_amount"] = final_total_amount_inr2
	
	data3 = frappe.db.sql("""select sum(tpf.amount),tpf.currency,
		ter.rate_in_inr * sum(tpf.amount) as total_inr
		from `tabProject Final Over Hubspots` tpf
		left join `tabCurrency Exchange Rate` ter on tpf.currency = ter.name WHERE
		tpf.company = 'Turacoz Healthcare Solutions Pvt Ltd'
		and MONTHNAME(STR_TO_DATE(MONTH(tpf.close_date),'%m')) = '{0}' and YEAR(tpf.close_date) = '{1}'
		group by tpf.currency""".format(month_name,year), as_dict=True)
				
	final_total_amount_inr3 = float()	
	for rec3 in data3:
		final_total_amount_inr3 += float(rec3.total_inr)
		final_total_amount_inr3 = round(final_total_amount_inr3, 2)	
	row["ths"] = final_total_amount_inr3
	
	data5 = frappe.db.sql("""select sum(tpf.amount),tpf.currency,
		ter.rate_in_inr * sum(tpf.amount) as total_inr
		from `tabProject Final Over Hubspots` tpf
		left join `tabCurrency Exchange Rate` ter on tpf.currency = ter.name WHERE
		tpf.company = 'Turacoz Solutions PTE Ltd.'
		and MONTHNAME(STR_TO_DATE(MONTH(tpf.close_date),'%m')) = '{0}' and YEAR(tpf.close_date) = '{1}'
		group by tpf.currency""".format(month_name,year), as_dict=True)
	final_total_amount_inr5 = float()	
	for rec5 in data5:
		final_total_amount_inr5 += float(rec5.total_inr)
		final_total_amount_inr5 = round(final_total_amount_inr5, 2)	
						
	row["tspl"] = final_total_amount_inr5
	
	data4 = frappe.db.sql("""select sum(tpf.amount),tpf.currency,
		ter.rate_in_inr * sum(tpf.amount) as total_inr
		from `tabProject Final Over Hubspots` tpf
		left join `tabCurrency Exchange Rate` ter on tpf.currency = ter.name WHERE
		tpf.company = 'Turacoz B.V.'
		and MONTHNAME(STR_TO_DATE(MONTH(tpf.close_date),'%m')) = '{0}' and YEAR(tpf.close_date) = '{1}'
		group by tpf.currency""".format(month_name,year), as_dict=True)
					
	final_total_amount_inr4 = float()	
	for rec4 in data4:
		final_total_amount_inr4 += float(rec4.total_inr)
		final_total_amount_inr4 = round(final_total_amount_inr4, 2)
			
	row["tbv"] = final_total_amount_inr4
	row["viatris"] = 0.0
		
	data.append(row)
	
	row17 = {}
	row17["particular"] = "New Pending PO Till " + "("+ month_name + " " + str(year) +")"

	dataNewPendingPO = frappe.db.sql("""select sum(tpf.amount),tpf.currency,
		ter.rate_in_inr * sum(tpf.amount) as total_inr
		from `tabProject Final Over Hubspots` tpf
		left join `tabCurrency Exchange Rate` ter on tpf.currency = ter.name WHERE popcd_status = 'Not Received'
		and tpf.close_date BETWEEN '2023-04-01' and '{0}'
		group by tpf.currency""".format(todays_date), as_dict=True)
	
	final_total_amount_inr_new_pending_po = float()	
	for recPendingNewPO in dataNewPendingPO:
		final_total_amount_inr_new_pending_po += float(recPendingNewPO.total_inr)
		final_total_amount_inr_new_pending_po = round(final_total_amount_inr_new_pending_po, 2)		
	row17["total_amount"] = final_total_amount_inr_new_pending_po
	
	dataNewPendingPOTHS = frappe.db.sql("""select sum(tpf.amount),tpf.currency,
		ter.rate_in_inr * sum(tpf.amount) as total_inr
		from `tabProject Final Over Hubspots` tpf
		left join `tabCurrency Exchange Rate` ter on tpf.currency = ter.name WHERE popcd_status = 'Not Received'
		and tpf.company = 'Turacoz Healthcare Solutions Pvt Ltd'
		and tpf.close_date BETWEEN '2023-04-01' and '{0}'
		group by tpf.currency""".format(todays_date),as_dict=True)
	
	final_total_amount_inr_new_pending_poTHS = float()	
	for recPendingNewPOTHS in dataNewPendingPOTHS:
		final_total_amount_inr_new_pending_poTHS += float(recPendingNewPOTHS.total_inr)
		final_total_amount_inr_new_pending_poTHS = round(final_total_amount_inr_new_pending_poTHS, 2)		
	row17["ths"] = final_total_amount_inr_new_pending_poTHS
	
	dataNewPendingPOTSPL = frappe.db.sql("""select sum(tpf.amount),tpf.currency,
		ter.rate_in_inr * sum(tpf.amount) as total_inr
		from `tabProject Final Over Hubspots` tpf
		left join `tabCurrency Exchange Rate` ter on tpf.currency = ter.name WHERE popcd_status = 'Not Received'
		and tpf.company = 'Turacoz Solutions PTE Ltd.'
		and tpf.close_date BETWEEN '2023-04-01' and '{0}'
		group by tpf.currency""".format(todays_date),as_dict=True)
	
	final_total_amount_inr_new_pending_poTSPL = float()	
	for recPendingNewPOTSPL in dataNewPendingPOTSPL:
		final_total_amount_inr_new_pending_poTSPL += float(recPendingNewPOTSPL.total_inr)
		final_total_amount_inr_new_pending_poTSPL = round(final_total_amount_inr_new_pending_poTSPL, 2)		
	row17["tspl"] = final_total_amount_inr_new_pending_poTSPL
	
	dataNewPendingPOTBV = frappe.db.sql("""select sum(tpf.amount),tpf.currency,
		ter.rate_in_inr * sum(tpf.amount) as total_inr
		from `tabProject Final Over Hubspots` tpf
		left join `tabCurrency Exchange Rate` ter on tpf.currency = ter.name WHERE popcd_status = 'Not Received'
		and tpf.company = 'Turacoz B.V.'
		and tpf.close_date BETWEEN '2023-04-01' and '{0}'
		group by tpf.currency""".format(todays_date),as_dict=True)
	
	final_total_amount_inr_new_pending_poTBV = float()	
	for recPendingNewPOTBV in dataNewPendingPOTBV:
		final_total_amount_inr_new_pending_poTBV += float(recPendingNewPOTBV.total_inr)
		final_total_amount_inr_new_pending_poTBV = round(final_total_amount_inr_new_pending_poTBV, 2)		
	row17["tbv"] = final_total_amount_inr_new_pending_poTBV
	row17["viatris"] = 0.0
		
	data.append(row17)
	
	row1 = {}
	row1["particular"] = "Invoices to be raised in "+ month_name + " " + str(year) +" - A"
	dataUraised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
					IFNULL(ter.rate_in_inr * sum(tps.payment_amount),0) as total_inr  
					from `tabSales Invoice` tsi 
					left join `tabPayment Schedule` tps on tsi.name = tps.parent
					left join `tabProject` tp on tsi.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
					WHERE tsi.status not in ('Paid','Cancelled')
					and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr_unraised = float()	
	for recUnraised in dataUraised:
		final_total_amount_inr_unraised += float(recUnraised.total_inr)
		final_total_amount_inr_unraised = round(final_total_amount_inr_unraised, 2)	
	row1["total_amount"]	= final_total_amount_inr_unraised
	
	dataUraisedTHS = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
					IFNULL(ter.rate_in_inr * sum(tps.payment_amount),0) as total_inr  
					from `tabSales Invoice` tsi 
					left join `tabPayment Schedule` tps on tsi.name = tps.parent
					left join `tabProject` tp on tsi.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
					WHERE tsi.status not in ('Paid','Cancelled') and 
					tsi.company = 'Turacoz Healthcare Solutions Pvt Ltd'
					and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr_unraisedTHS = float()	
	for recUnraisedTHS in dataUraisedTHS:
		final_total_amount_inr_unraisedTHS += float(recUnraisedTHS.total_inr)
		final_total_amount_inr_unraisedTHS = round(final_total_amount_inr_unraisedTHS, 2)	
	row1["ths"]	= final_total_amount_inr_unraisedTHS
	
	dataUraisedTSPL = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
					IFNULL(ter.rate_in_inr * sum(tps.payment_amount),0) as total_inr  
					from `tabSales Invoice` tsi 
					left join `tabPayment Schedule` tps on tsi.name = tps.parent
					left join `tabProject` tp on tsi.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
					WHERE tsi.status not in ('Paid','Cancelled') and 
					tsi.company = 'Turacoz Solutions PTE Ltd.'
					and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr_unraisedTSPL = float()	
	for recUnraisedTSPL in dataUraisedTSPL:
		final_total_amount_inr_unraisedTSPL += float(recUnraisedTSPL.total_inr)
		final_total_amount_inr_unraisedTSPL = round(final_total_amount_inr_unraisedTSPL, 2)	
	row1["tspl"]	= final_total_amount_inr_unraisedTSPL
	
	dataUraisedTBV = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
					ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
					from `tabSales Invoice` tsi 
					left join `tabPayment Schedule` tps on tsi.name = tps.parent
					left join `tabProject` tp on tsi.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
					WHERE tsi.status not in ('Paid','Cancelled') and 
					tsi.company = 'Turacoz B.V.'
					and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr_unraisedTBV = float()	
	for recUnraisedTBV in dataUraisedTBV:
		final_total_amount_inr_unraisedTBV += float(recUnraisedTBV.total_inr)
		final_total_amount_inr_unraisedTBV = round(final_total_amount_inr_unraisedTBV, 2)	
	row1["tbv"]	= final_total_amount_inr_unraisedTBV
	row1["viatris"] = 0.0
		
	data.append(row1)
	
	row2 = {}
	row2["particular"] = "Invoice raised in " + month_name + " " + str(year) +" - B"
	
	dataRaised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
		IFNULL(ter.rate_in_inr * sum(tps.payment_amount),0) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
		WHERE tsi.status not in ('Paid','Cancelled') and tps.invoice_status='Raised'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
	final_total_amount_inr_raised = float()	
	for recRaised in dataRaised:
		final_total_amount_inr_raised += float(recRaised.total_inr)
		final_total_amount_inr_raised = round(final_total_amount_inr_raised, 2)	
	row2["total_amount"] = final_total_amount_inr_raised
	
	dataRaisedTHS = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
		IFNULL(ter.rate_in_inr * sum(tps.payment_amount),0) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
		WHERE tsi.status not in ('Paid','Cancelled') and tps.invoice_status='Raised'
		and tsi.company = 'Turacoz Healthcare Solutions Pvt Ltd'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
	final_total_amount_inr_raisedTHS = float()	
	for recRaisedTHS in dataRaisedTHS:
		final_total_amount_inr_raisedTHS += float(recRaisedTHS.total_inr)
		final_total_amount_inr_raisedTHS = round(final_total_amount_inr_raisedTHS, 2)	
	row2["ths"]	= final_total_amount_inr_raisedTHS
	
	dataRaisedTSPL = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
		ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
		WHERE tsi.status not in ('Paid','Cancelled') and tps.invoice_status='Raised'
		and tsi.company = 'Turacoz Solutions PTE Ltd.'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
	final_total_amount_inr_raisedTSPL = float()	
	for recRaisedTSPL in dataRaisedTSPL:
		final_total_amount_inr_raisedTSPL += float(recRaisedTSPL.total_inr)
		final_total_amount_inr_raisedTSPL = round(final_total_amount_inr_raisedTSPL, 2)	
	row2["tspl"] = final_total_amount_inr_raisedTSPL
	
	dataRaisedTBV = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
		ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
		WHERE tsi.status not in ('Paid','Cancelled') and tps.invoice_status='Raised'
		and tsi.company = 'Turacoz B.V.'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
	final_total_amount_inr_raisedTBV = float()	
	for recRaisedTBV in dataRaisedTBV:
		final_total_amount_inr_raisedTBV += float(recRaisedTBV.total_inr)
		final_total_amount_inr_raisedTBV = round(final_total_amount_inr_raisedTBV, 2)	
	row2["tbv"]	= final_total_amount_inr_raisedTBV
	row2["viatris"] = 0.0
		
	data.append(row2)
	
	row3 = {}
	row3["particular"] = "Balance Invoices to be raised in " + month_name + " " + str(year) +" - C (C=A-B)"
	
	dataInvoiceTobeRaised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
		tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled')
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
		MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr_invoice_to_be_raised = float()	
	for recInvoiceToBeRaised in dataInvoiceTobeRaised:
		final_total_amount_inr_invoice_to_be_raised += float(recInvoiceToBeRaised.total_inr)
		final_total_amount_inr_invoice_to_be_raised = round(final_total_amount_inr_invoice_to_be_raised, 2)	
	row3["total_amount"] = final_total_amount_inr_invoice_to_be_raised
	
	dataInvoiceTobeRaisedTHS = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
		tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled')
		and tsi.company = 'Turacoz Healthcare Solutions Pvt Ltd'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
		MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr_invoice_to_be_raisedTHS = float()	
	for recInvoiceToBeRaisedTHS in dataInvoiceTobeRaisedTHS:
		final_total_amount_inr_invoice_to_be_raisedTHS += float(recInvoiceToBeRaisedTHS.total_inr)
		final_total_amount_inr_invoice_to_be_raisedTHS = round(final_total_amount_inr_invoice_to_be_raisedTHS, 2)	
	row3["ths"] = final_total_amount_inr_invoice_to_be_raisedTHS
	
	dataInvoiceTobeRaisedTSPL = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
		tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled')
		and tsi.company = 'Turacoz Solutions PTE Ltd.'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
		MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr_invoice_to_be_raisedTSPL = float()	
	for recInvoiceToBeRaisedTSPL in dataInvoiceTobeRaisedTSPL:
		final_total_amount_inr_invoice_to_be_raisedTSPL += float(recInvoiceToBeRaisedTSPL.total_inr)
		final_total_amount_inr_invoice_to_be_raisedTSPL = round(final_total_amount_inr_invoice_to_be_raisedTSPL, 2)	
	row3["tspl"] = final_total_amount_inr_invoice_to_be_raisedTSPL
	
	dataInvoiceTobeRaisedTBV = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
		tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled')
		and tsi.company = 'Turacoz B.V.'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
		MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr_invoice_to_be_raisedTBV = float()	
	for recInvoiceToBeRaisedTBV in dataInvoiceTobeRaisedTBV:
		final_total_amount_inr_invoice_to_be_raisedTBV += float(recInvoiceToBeRaisedTBV.total_inr)
		final_total_amount_inr_invoice_to_be_raisedTBV = round(final_total_amount_inr_invoice_to_be_raisedTBV, 2)	
	row3["tbv"] = final_total_amount_inr_invoice_to_be_raisedTBV
	row3["viatris"] = 0.0
		
	data.append(row3)
	
	row13 = {}
	row13["particular"] = "-----------------------"
	data.append(row13)
	
	row9 = {}
	row9["particular"] = "Overdue unraised invoices till " + last_month_name + " " + str(last_month_year) + " - D"
	dataOverDueInvoiceTillLastMonth = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
		ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled') and tp.project_current_status not in ('Cancelled') and tps.invoice_status = 'Unraised'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		tps.due_date < '{0}' GROUP by tsi.currency""".format(firstDateofCurrentMonth), as_dict = True)
	final_total_amount_inr_unraised_overdue_till_last_month = float()	
	for recOverdueUnraisedLastMonth in dataOverDueInvoiceTillLastMonth:
		final_total_amount_inr_unraised_overdue_till_last_month += float(recOverdueUnraisedLastMonth.total_inr)
		final_total_amount_inr_unraised_overdue_till_last_month = round(final_total_amount_inr_unraised_overdue_till_last_month, 2)	
	row9["total_amount"] = final_total_amount_inr_unraised_overdue_till_last_month

	dataOverDueInvoiceTillLastMonthTHS = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
		ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled') 
		and tsi.company = 'Turacoz Healthcare Solutions Pvt Ltd'
		and tp.project_current_status not in ('Cancelled') and tps.invoice_status = 'Unraised'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		tps.due_date < '{0}' GROUP by tsi.currency""".format(firstDateofCurrentMonth), as_dict = True)
	final_total_amount_inr_unraised_overdue_till_last_monthTHS = float()	
	for recOverdueUnraisedLastMonthTHS in dataOverDueInvoiceTillLastMonthTHS:
		final_total_amount_inr_unraised_overdue_till_last_monthTHS += float(recOverdueUnraisedLastMonthTHS.total_inr)
		final_total_amount_inr_unraised_overdue_till_last_monthTHS = round(final_total_amount_inr_unraised_overdue_till_last_monthTHS, 2)	
	row9["ths"] = final_total_amount_inr_unraised_overdue_till_last_monthTHS
	
	dataOverDueInvoiceTillLastMonthTSPL = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
		ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled') 
		and tsi.company = 'Turacoz Solutions PTE Ltd.'
		and tp.project_current_status not in ('Cancelled') and tps.invoice_status = 'Unraised'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		tps.due_date < '{0}' GROUP by tsi.currency""".format(firstDateofCurrentMonth), as_dict = True)
	final_total_amount_inr_unraised_overdue_till_last_monthTSPL = float()	
	for recOverdueUnraisedLastMonthTSPL in dataOverDueInvoiceTillLastMonthTSPL:
		final_total_amount_inr_unraised_overdue_till_last_monthTSPL += float(recOverdueUnraisedLastMonthTSPL.total_inr)
		final_total_amount_inr_unraised_overdue_till_last_monthTSPL = round(final_total_amount_inr_unraised_overdue_till_last_monthTSPL, 2)	
	row9["tspl"] = final_total_amount_inr_unraised_overdue_till_last_monthTSPL
	
	dataOverDueInvoiceTillLastMonthTBV = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
		ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled') 
		and tsi.company = 'Turacoz B.V.'
		and tp.project_current_status not in ('Cancelled') and tps.invoice_status = 'Unraised'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		tps.due_date < '{0}' GROUP by tsi.currency""".format(firstDateofCurrentMonth), as_dict = True)
	final_total_amount_inr_unraised_overdue_till_last_monthTBV = float()	
	for recOverdueUnraisedLastMonthTBV in dataOverDueInvoiceTillLastMonthTBV:
		final_total_amount_inr_unraised_overdue_till_last_monthTBV += float(recOverdueUnraisedLastMonthTBV.total_inr)
		final_total_amount_inr_unraised_overdue_till_last_monthTBV = round(final_total_amount_inr_unraised_overdue_till_last_monthTBV, 2)	
	row9["tbv"] = final_total_amount_inr_unraised_overdue_till_last_monthTBV
	row9["viatris"] = 0.0
		
	data.append(row9)
	
	row10 = {}
	row10["particular"] = "Overdue invoices raised till date - E"
	DataOverdueUnraisedRaisedTillDate = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
		ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
		left join `tabPayment Request` tpr on tsi.name = tpr.sales_invoice
		WHERE tsi.status not in ('Paid','Cancelled') and tp.project_current_status not in ('Cancelled') 
		and tps.invoice_status = 'Raised'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		tps.due_date < '{2}'
		and MONTHNAME(STR_TO_DATE(MONTH(tps.raised_date),'%m')) = '{0}' and YEAR(tps.raised_date) = '{1}' 
		GROUP by tsi.currency""".format(month_name,year,firstDateofCurrentMonth), as_dict = True)
	final_total_amount_inr_unraised_overdue_raised_till_date = float()	
	for recOverdueUnraisedRaisedTillDate in DataOverdueUnraisedRaisedTillDate:
		final_total_amount_inr_unraised_overdue_raised_till_date += float(recOverdueUnraisedRaisedTillDate.total_inr)
		final_total_amount_inr_unraised_overdue_raised_till_date = round(final_total_amount_inr_unraised_overdue_raised_till_date, 2)	
	row10["total_amount"] = final_total_amount_inr_unraised_overdue_raised_till_date
	
	DataOverdueUnraisedRaisedTillDateTHS = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
		ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
		left join `tabPayment Request` tpr on tsi.name = tpr.sales_invoice
		WHERE tsi.status not in ('Paid','Cancelled') 
		and tsi.company = 'Turacoz Healthcare Solutions Pvt Ltd'
		and tp.project_current_status not in ('Cancelled') 
		and tps.invoice_status = 'Raised'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		tps.due_date < '{2}'
		and MONTHNAME(STR_TO_DATE(MONTH(tps.raised_date),'%m')) = '{0}' and YEAR(tps.raised_date) = '{1}' 
		GROUP by tsi.currency""".format(month_name,year,firstDateofCurrentMonth), as_dict = True)
	
	final_total_amount_inr_unraised_overdue_raised_till_dateTHS = float()	
	for recOverdueUnraisedRaisedTillDateTHS in DataOverdueUnraisedRaisedTillDateTHS:
		final_total_amount_inr_unraised_overdue_raised_till_dateTHS += float(recOverdueUnraisedRaisedTillDateTHS.total_inr)
		final_total_amount_inr_unraised_overdue_raised_till_dateTHS = round(final_total_amount_inr_unraised_overdue_raised_till_dateTHS, 2)	
	row10["ths"] = final_total_amount_inr_unraised_overdue_raised_till_dateTHS
	
	DataOverdueUnraisedRaisedTillDateTSPL = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
		ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
		left join `tabPayment Request` tpr on tsi.name = tpr.sales_invoice
		WHERE tsi.status not in ('Paid','Cancelled') 
		and tsi.company = 'Turacoz Solutions PTE Ltd.'
		and tp.project_current_status not in ('Cancelled') 
		and tps.invoice_status = 'Raised'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		tps.due_date < '{2}'
		and MONTHNAME(STR_TO_DATE(MONTH(tps.raised_date),'%m')) = '{0}' and YEAR(tps.raised_date) = '{1}' 
		GROUP by tsi.currency""".format(month_name,year,firstDateofCurrentMonth), as_dict = True)
	
	final_total_amount_inr_unraised_overdue_raised_till_dateTSPL = float()	
	for recOverdueUnraisedRaisedTillDateTSPL in DataOverdueUnraisedRaisedTillDateTSPL:
		final_total_amount_inr_unraised_overdue_raised_till_dateTSPL += float(recOverdueUnraisedRaisedTillDateTSPL.total_inr)
		final_total_amount_inr_unraised_overdue_raised_till_dateTSPL = round(final_total_amount_inr_unraised_overdue_raised_till_dateTSPL, 2)	
	row10["tspl"] = final_total_amount_inr_unraised_overdue_raised_till_dateTSPL
	
	DataOverdueUnraisedRaisedTillDateTBV = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
		ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
		left join `tabPayment Request` tpr on tsi.name = tpr.sales_invoice
		WHERE tsi.status not in ('Paid','Cancelled') 
		and tsi.company = 'Turacoz B.V.'
		and tp.project_current_status not in ('Cancelled') 
		and tps.invoice_status = 'Raised'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		tps.due_date < '{2}'
		and MONTHNAME(STR_TO_DATE(MONTH(tps.raised_date),'%m')) = '{0}' and YEAR(tps.raised_date) = '{1}' 
		GROUP by tsi.currency""".format(month_name,year,firstDateofCurrentMonth), as_dict = True)
	
	final_total_amount_inr_unraised_overdue_raised_till_dateTBV = float()	
	for recOverdueUnraisedRaisedTillDateTBV in DataOverdueUnraisedRaisedTillDateTBV:
		final_total_amount_inr_unraised_overdue_raised_till_dateTBV += float(recOverdueUnraisedRaisedTillDateTBV.total_inr)
		final_total_amount_inr_unraised_overdue_raised_till_dateTBV = round(final_total_amount_inr_unraised_overdue_raised_till_dateTBV, 2)	
	row10["tbv"] = final_total_amount_inr_unraised_overdue_raised_till_dateTBV
	
	row10["viatris"] = 0.0
		
	data.append(row10)
	
	row11 = {}
	row11["particular"] = "Balance overdue invoices - F (F=D-E)"
	row11["total_amount"] = final_total_amount_inr_unraised_overdue_till_last_month-final_total_amount_inr_unraised_overdue_raised_till_date
	row11["ths"] = final_total_amount_inr_unraised_overdue_till_last_monthTHS-final_total_amount_inr_unraised_overdue_raised_till_dateTHS
	row11["tspl"] = final_total_amount_inr_unraised_overdue_till_last_monthTSPL-final_total_amount_inr_unraised_overdue_raised_till_dateTSPL
	row11["tbv"] = final_total_amount_inr_unraised_overdue_till_last_monthTBV-final_total_amount_inr_unraised_overdue_raised_till_dateTBV
	row11["viatris"] = 0.0
	data.append(row11)
	
	row12 = {}
	row12["particular"] = "-----------------------"
	data.append(row12)
	
	row14 = {}
	row14["particular"] = "Total Invoices Due - G (G=A+D)"
	row14["total_amount"] = final_total_amount_inr_unraised+final_total_amount_inr_unraised_overdue_till_last_month
	row14["ths"] = final_total_amount_inr_unraisedTHS+final_total_amount_inr_unraised_overdue_till_last_monthTHS
	row14["tspl"] = final_total_amount_inr_unraisedTSPL+final_total_amount_inr_unraised_overdue_till_last_monthTSPL
	row14["tbv"] = final_total_amount_inr_unraisedTBV+final_total_amount_inr_unraised_overdue_till_last_monthTBV
	row14["viatris"] = 0.0
	
	data.append(row14)
	
	row15 = {}
	row15["particular"] = "Total Invoices Raised - H (H=B+E)"
	row15["total_amount"] = final_total_amount_inr_raised+final_total_amount_inr_unraised_overdue_raised_till_date
	row15["ths"] = final_total_amount_inr_raisedTHS+final_total_amount_inr_unraised_overdue_raised_till_dateTHS
	row15["tspl"] = final_total_amount_inr_raisedTSPL+final_total_amount_inr_unraised_overdue_raised_till_dateTSPL
	row15["tbv"] = final_total_amount_inr_raisedTBV+final_total_amount_inr_unraised_overdue_raised_till_dateTBV
	row15["viatris"] = 0.0
	data.append(row15)
	
	row18 = {}
	row18["particular"] = "Balance Invoices Due - I (I=G-H)"
	row18["total_amount"] = (final_total_amount_inr_unraised+final_total_amount_inr_unraised_overdue_till_last_month)-(final_total_amount_inr_raised+final_total_amount_inr_unraised_overdue_raised_till_date)
	row18["ths"] = (final_total_amount_inr_unraisedTHS+final_total_amount_inr_unraised_overdue_till_last_monthTHS)-(final_total_amount_inr_raisedTHS+final_total_amount_inr_unraised_overdue_raised_till_dateTHS)
	row18["tspl"] = (final_total_amount_inr_unraisedTSPL+final_total_amount_inr_unraised_overdue_till_last_monthTSPL)-(final_total_amount_inr_raisedTSPL+final_total_amount_inr_unraised_overdue_raised_till_dateTSPL)
	row18["tbv"] = (final_total_amount_inr_unraisedTBV+final_total_amount_inr_unraised_overdue_till_last_monthTBV)-(final_total_amount_inr_raisedTBV+final_total_amount_inr_unraised_overdue_raised_till_dateTBV)
	row18["viatris"] = 0.0
	data.append(row18)
	
	row16 = {}
	row16["particular"] = "-----------------------"
	data.append(row16)
		
	row5 = {}
	row5["particular"] = "Total Payment Due Till " + "("+ month_name + " " + str(year) +")"
	
	dataExpected = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
		tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
		left join `tabProject` tp on tpr.project = tp.name
		WHERE tp.project_type='External' and tpr.payment_status not in ('Cancelled','Paid') and tpr.due_date is not NULL and
		tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		tpr.due_date<='{0}' GROUP by tpr.invoice_currency""".format(lastDateofCurrentMonth), as_dict=True)
		
	final_total_amount_inr_expected = float()	
	for recExpected in dataExpected:
		final_total_amount_inr_expected += float(recExpected.total_inr)
		final_total_amount_inr_expected = round(final_total_amount_inr_expected, 2)	
	row5["total_amount"] = final_total_amount_inr_expected
	
	dataExpectedTHS = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
		tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
		left join `tabProject` tp on tpr.project = tp.name
		WHERE tp.project_type='External' and tpr.payment_status not in ('Cancelled','Paid') and tpr.due_date is not NULL 
		and tpr.company = 'Turacoz Healthcare Solutions Pvt Ltd'
		and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		tpr.due_date<='{0}' GROUP by tpr.invoice_currency""".format(lastDateofCurrentMonth), as_dict=True)
	
	final_total_amount_inr_expectedTHS = float()	
	for recExpectedTHS in dataExpectedTHS:
		final_total_amount_inr_expectedTHS += float(recExpectedTHS.total_inr)
		final_total_amount_inr_expectedTHS = round(final_total_amount_inr_expectedTHS, 2)	
	row5["ths"] = final_total_amount_inr_expectedTHS
	
	dataExpected = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
		tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
		left join `tabProject` tp on tpr.project = tp.name
		WHERE tp.project_type='External' and tpr.payment_status not in ('Cancelled','Paid') and tpr.due_date is not NULL 
		and tpr.company = 'Turacoz Solutions PTE Ltd.'
		and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		tpr.due_date<='{0}' GROUP by tpr.invoice_currency""".format(lastDateofCurrentMonth), as_dict=True)
				
	type = "Monthly_Payment_Due"
	final_total_amount_inr_expected = float()	
	for recExpected in dataExpected:
		final_total_amount_inr_expected += float(recExpected.total_inr)
		final_total_amount_inr_expected = round(final_total_amount_inr_expected, 2)	
	row5["tspl"] = final_total_amount_inr_expected
	
	dataExpected = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
		tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
		left join `tabProject` tp on tpr.project = tp.name
		WHERE tp.project_type='External' and tpr.payment_status not in ('Cancelled','Paid') and tpr.due_date is not NULL 
		and tpr.company = 'Turacoz B.V.'
		and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		tpr.due_date<='{0}' GROUP by tpr.invoice_currency""".format(lastDateofCurrentMonth), as_dict=True)
		
	final_total_amount_inr_expected = float()	
	for recExpected in dataExpected:
		final_total_amount_inr_expected += float(recExpected.total_inr)
		final_total_amount_inr_expected = round(final_total_amount_inr_expected, 2)	
	row5["tbv"] = final_total_amount_inr_expected
	
	dataViatrisPending = frappe.db.sql("""select sum(grand_total) as total_pending_amount from `tabPayment Request` 
		where customer_name in ('Viatris Centre of Excellence') and payment_status in ('Overdue','Unpaid')
		and status not in ('Cancelled');""", as_dict = True)
	if dataViatrisPending:
		row5["viatris"] = dataViatrisPending[0]['total_pending_amount']
	else:
		row5["viatris"] = 0.0	
		
	data.append(row5)
	
	row6 = {}
	row6["particular"] = "Payment Received " + "("+ month_name + " " + str(year) +")"
	
	dataReceived = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
		tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name 
		WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL and
		tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr_received = float()	
	for recReceived in dataReceived:
		final_total_amount_inr_received += float(recReceived.total_inr)
		final_total_amount_inr_received = round(final_total_amount_inr_received, 2)	
	row6["total_amount"]	= final_total_amount_inr_received
	
	dataReceivedTHS = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
		tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name 
		WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL 
		and tpr.company = 'Turacoz Healthcare Solutions Pvt Ltd'
		and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr_receivedTHS = float()	
	for recReceivedTHS in dataReceivedTHS:
		final_total_amount_inr_receivedTHS += float(recReceivedTHS.total_inr)
		final_total_amount_inr_receivedTHS = round(final_total_amount_inr_receivedTHS, 2)	
	row6["ths"]	= final_total_amount_inr_receivedTHS
	
	dataReceivedTSPL = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
		tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name 
		WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL 
		and tpr.company = 'Turacoz Solutions PTE Ltd.'
		and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr_receivedTSPL = float()	
	for recReceivedTSPL in dataReceivedTSPL:
		final_total_amount_inr_receivedTSPL += float(recReceivedTSPL.total_inr)
		final_total_amount_inr_receivedTSPL = round(final_total_amount_inr_receivedTSPL, 2)	
	row6["tspl"]	= final_total_amount_inr_receivedTSPL
	
	dataReceivedTBV = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
		tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name 
		WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL 
		and tpr.company = 'Turacoz B.V.'
		and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
	
	final_total_amount_inr_receivedTBV = float()	
	for recReceivedTBV in dataReceivedTBV:
		final_total_amount_inr_receivedTBV += float(recReceivedTBV.total_inr)
		final_total_amount_inr_receivedTBV = round(final_total_amount_inr_receivedTBV, 2)	
	row6["tbv"]	= final_total_amount_inr_receivedTBV
	
	dataReceivedViatris = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
		tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name 
		WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL
		and tpr.party in ('Viatris Centre of Excellence') and
		MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
	if dataReceivedViatris:
		row6["viatris"] = dataReceivedViatris[0]['total_inr']
	else:
		row6["viatris"] = 0.0	
		
	data.append(row6)
	
	
	row8 = {}
	row8["particular"] = "Payment Received YTD (Total Revenue)" + "(1 April 2023 to "+ month_name + " " + str(year) +")"
	
	actualReceived = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
		tpr.invoice_currency, ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
		from `tabPayment Request` tpr
		left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
		WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL and
		tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		tpr.payment_date BETWEEN '2023-04-01' and '{0}' GROUP by tpr.invoice_currency""".format(todays_date), as_dict=True)
	
	final_total_amount_inr_received_actual = float()
	for actualReceived in actualReceived:
		final_total_amount_inr_received_actual += float(actualReceived.total_inr)
		final_total_amount_inr_received_actual = round(final_total_amount_inr_received_actual, 2)	
	row8["total_amount"]	= final_total_amount_inr_received_actual
	
	actualReceivedTHS = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
		tpr.invoice_currency, ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
	   	from `tabPayment Request` tpr
	   	left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
	   	WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL 
	   	and tpr.company = 'Turacoz Healthcare Solutions Pvt Ltd'
	   	and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
	   	tpr.payment_date BETWEEN '2023-04-01' and '{0}' GROUP by tpr.invoice_currency""".format(todays_date), as_dict=True)
	
	final_total_amount_inr_received_actualTHS = float()
	for actualReceivedTHS in actualReceivedTHS:
		final_total_amount_inr_received_actualTHS += float(actualReceivedTHS.total_inr)
		final_total_amount_inr_received_actualTHS = round(final_total_amount_inr_received_actualTHS, 2)	
	row8["ths"]	= final_total_amount_inr_received_actualTHS
	
	actualReceivedTSPL = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
		tpr.invoice_currency, ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
	   	from `tabPayment Request` tpr
	   	left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
	   	WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL 
	   	and tpr.company = 'Turacoz Solutions PTE Ltd.'
	   	and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
	   	tpr.payment_date BETWEEN '2023-04-01' and '{0}' GROUP by tpr.invoice_currency""".format(todays_date), as_dict=True)
	
	final_total_amount_inr_received_actualTSPL = float()
	for actualReceivedTSPL in actualReceivedTSPL:
		final_total_amount_inr_received_actualTSPL += float(actualReceivedTSPL.total_inr)
		final_total_amount_inr_received_actualTSPL = round(final_total_amount_inr_received_actualTSPL, 2)	
	row8["tspl"]	= final_total_amount_inr_received_actualTSPL
	
	actualReceivedTBV = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
		tpr.invoice_currency, ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
	   	from `tabPayment Request` tpr
	   	left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
	   	WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL 
	   	and tpr.company = 'Turacoz B.V.'
	   	and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
	   	tpr.payment_date BETWEEN '2023-04-01' and '{0}' GROUP by tpr.invoice_currency""".format(todays_date), as_dict=True)
	
	final_total_amount_inr_received_actualTBV = float()
	for actualReceivedTBV in actualReceivedTBV:
		final_total_amount_inr_received_actualTBV += float(actualReceivedTBV.total_inr)
		final_total_amount_inr_received_actualTBV = round(final_total_amount_inr_received_actualTBV, 2)	
	row8["tbv"]	= final_total_amount_inr_received_actualTBV
	
	dataViatrisReceivedYTD = frappe.db.sql("""select sum(grand_total) as total_received_amount from `tabPayment Request` 
		where customer_name in ('Viatris Centre of Excellence') and payment_status in ('Paid')
		and status not in ('Cancelled') and invoice_date BETWEEN '2023-04-01' and '{0}';""".format(todays_date), as_dict = True)
	if dataViatrisReceivedYTD:
		row8["viatris"] = dataViatrisReceivedYTD[0]['total_received_amount']
	else:
		row8["viatris"] = 0.0	 	
					
	data.append(row8)
				
	return data

def get_columns():
	cols = [
			{
				"fieldname": "particular",
				"label": _("Particular"),
				"fieldtype": "Data",
				"width": "400"
			},
			{
				"fieldname": "total_amount",
				"label": _("Total Amount"),
				"fieldtype": "Currency",
				"width": "150"
			},
			{
				"fieldname": "ths",
				"label": _("THS"),
				"fieldtype": "Currency",
				"width": "150"
			},
			{
				"fieldname": "tspl",
				"label": _("TSPL"),
				"fieldtype": "Currency",
				"width": "150"
			},
			{
				"fieldname": "tbv",
				"label": _("TBV"),
				"fieldtype": "Currency",
				"width": "150"
			},
			{
				"fieldname": "viatris",
				"label": _("Viatris"),
				"fieldtype": "Currency",
				"width": "150"
			},
			
		]
	return cols
