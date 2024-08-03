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
	columns = get_columns()
	data = get_data()
	return columns, data

def get_data():
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
	row = {}
	
	row["particular"] = "<b>Purchase Order</b>"

	total_new_po_mtd = 0
	ths_new_po_mtd = 0
	tbv_new_po_mtd = 0
	tspl_new_po_mtd = 0
	new_po_receivedMTD = new_po_received_mtd(month_name,year)
	for new_poReceivedMTD in new_po_receivedMTD:
		total_new_po_mtd += new_poReceivedMTD.total_inr
		if new_poReceivedMTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_new_po_mtd += new_poReceivedMTD.total_inr
		elif new_poReceivedMTD.company == 'Turacoz B.V.':
			tbv_new_po_mtd += new_poReceivedMTD.total_inr
		elif new_poReceivedMTD.company == 'Turacoz Solutions PTE Ltd.':
			tspl_new_po_mtd += new_poReceivedMTD.total_inr

	row1 = {}
	row1["particular"] = 'New PO Received in MTD ({0} {1})'.format(month_name,year)
	row1["total"] = round(total_new_po_mtd, 2)
	row1["ths"] = round(ths_new_po_mtd, 2)
	row1["tbv"] = round(tbv_new_po_mtd, 2)
	row1["tspl"] = round(tspl_new_po_mtd, 2)


	total_new_po_ytd = 0
	ths_new_po_ytd = 0
	tbv_new_po_ytd = 0
	tspl_new_po_ytd = 0
	new_po_receivedYTD = new_po_received_ytd(year_start_date,todays_date)
	for new_poReceivedYTD in new_po_receivedYTD:
		total_new_po_ytd += new_poReceivedYTD.total_inr
		if new_poReceivedYTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_new_po_ytd += new_poReceivedYTD.total_inr
		elif new_poReceivedYTD.company == 'Turacoz B.V.':
			tbv_new_po_ytd += new_poReceivedYTD.total_inr
		elif new_poReceivedYTD.company == 'Turacoz Solutions PTE Ltd.':
			tspl_new_po_ytd += new_poReceivedYTD.total_inr

	row2 = {}
	row2["particular"] = 'New PO Received in YTD ({0})'.format(year)
	row2["total"] = round(total_new_po_ytd, 2)
	row2["ths"] = round(ths_new_po_ytd, 2)
	row2["tbv"] = round(tbv_new_po_ytd, 2)
	row2["tspl"] = round(tspl_new_po_ytd, 2)


	total_pending_po_tillToday = 0
	ths_pending_po_tillToday = 0
	tbv_pending_po_tillToday = 0
	tspl_pending_po_tillToday = 0
	pending_po_tillToday = pending_po_till_today(todays_date)
	for pending_PoTillToday in pending_po_tillToday:
		total_pending_po_tillToday += pending_PoTillToday.total_inr
		if pending_PoTillToday.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_pending_po_tillToday += pending_PoTillToday.total_inr
		elif pending_PoTillToday.company == 'Turacoz B.V.':
			tbv_pending_po_tillToday += pending_PoTillToday.total_inr
		elif pending_PoTillToday.company == 'Turacoz Solutions PTE Ltd.':
			tspl_pending_po_tillToday += pending_PoTillToday.total_inr

	row3 = {}
	row3["particular"] = 'Pending PO till <b>{0}</b>'.format(formatted_date)
	row3["total"] = round(total_pending_po_tillToday, 2)
	row3["ths"] = round(ths_pending_po_tillToday, 2)
	row3["tbv"] = round(tbv_pending_po_tillToday, 2)
	row3["tspl"] = round(tspl_pending_po_tillToday, 2)

	row4 = {}
	row4["particular"] = "<b>Invoices</b>"

	total_unraised_till_date = 0
	ths_unraised_till_date = 0
	tbv_unraised_till_date = 0
	tspl_unraised_till_date = 0
	overdueunraiseTillDate = overdue_unraised_invoices_till_date(todays_date)
	for unraisedTillDate in overdueunraiseTillDate:
		total_unraised_till_date += unraisedTillDate.total_inr
		if unraisedTillDate.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_unraised_till_date += unraisedTillDate.total_inr
		elif unraisedTillDate.company == 'Turacoz B.V.':
			tbv_unraised_till_date += unraisedTillDate.total_inr
		elif unraisedTillDate.company == 'Turacoz Solutions PTE Ltd.':
			tspl_unraised_till_date += unraisedTillDate.total_inr

	row5 = {}
	row5["particular"] = "Overdue Unraised Invoices till <b>{0}</b>".format(formatted_date)
	row5["total"] = '<a href="/app/query-report/Monthly Financial Detailed Preview Report?key=total_unraised_amount_till_date" target="_blank">{0}</a>'.format(round(total_unraised_till_date, 2))
	row5["ths"] = round(ths_unraised_till_date, 2)
	row5["tbv"] = round(tbv_unraised_till_date, 2)
	row5["tspl"] = round(tspl_unraised_till_date, 2)

	total_raised_mtd = 0
	ths_raised_mtd = 0
	tbv_raised_mtd = 0
	tspl_raised_mtd = 0
	actual_invoices_raisedMTD_data = actual_invoices_raised_mtd(month_name,year)
	for actualInvoiceRaisedMTD in actual_invoices_raisedMTD_data:
		total_raised_mtd += actualInvoiceRaisedMTD.total_inr
		if actualInvoiceRaisedMTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_raised_mtd += actualInvoiceRaisedMTD.total_inr
		elif actualInvoiceRaisedMTD.company == 'Turacoz B.V.':
			tbv_raised_mtd += actualInvoiceRaisedMTD.total_inr
		elif actualInvoiceRaisedMTD.company == 'Turacoz Solutions PTE Ltd.':
			tspl_raised_mtd += actualInvoiceRaisedMTD.total_inr

	row6 = {}
	row6["particular"] = "Actual Invoices Raised MTD ({0} {1})".format(month_name,year)
	row6["total"] = '<a href="/app/query-report/Monthly Financial Detailed Preview Report?key=actual_invoice_raised_mtd" target="_blank">{0}</a>'.format(round(total_raised_mtd, 2))
	row6["ths"] = round(ths_raised_mtd, 2)
	row6["tbv"] = round(tbv_raised_mtd, 2)
	row6["tspl"] = round(tspl_raised_mtd, 2)


	total_raised_ytd = 0
	ths_raised_ytd = 0
	tbv_raised_ytd = 0
	tspl_raised_ytd = 0
	actual_invoices_raisedMTD = actual_invoices_raised_ytd(year_start_date,todays_date)
	for actualInvoiceRaisedYTD in actual_invoices_raisedMTD:
		total_raised_ytd += actualInvoiceRaisedYTD.total_inr
		if actualInvoiceRaisedYTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_raised_ytd += actualInvoiceRaisedYTD.total_inr
		elif actualInvoiceRaisedYTD.company == 'Turacoz B.V.':
			tbv_raised_ytd += actualInvoiceRaisedYTD.total_inr
		elif actualInvoiceRaisedYTD.company == 'Turacoz Solutions PTE Ltd.':
			tspl_raised_ytd += actualInvoiceRaisedYTD.total_inr

	row7 = {}
	row7["particular"] = "Actual Invoices Raised YTD ({0})".format(year)
	row7["total"] = '<a href="/app/query-report/Monthly Financial Detailed Preview Report?key=actual_invoice_raised_ytd" target="_blank">{0}</a>'.format(round(total_raised_ytd, 2))
	row7["ths"] = round(ths_raised_ytd, 2)
	row7["tbv"] = round(tbv_raised_ytd, 2)
	row7["tspl"] = round(tspl_raised_ytd, 2)

	row8 = {}
	row8["particular"] = "<b>Payment</b>"


	total_received_mtd = 0
	ths_received_mtd = 0
	tbv_received_mtd = 0
	tspl_received_mtd = 0
	payment_receivedMTD = payment_received_mtd(month_name,year)
	for paymentReceivedMTD in payment_receivedMTD:
		total_received_mtd += paymentReceivedMTD.total_inr
		if paymentReceivedMTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_received_mtd += paymentReceivedMTD.total_inr
		elif paymentReceivedMTD.company == 'Turacoz B.V.':
			tbv_received_mtd += paymentReceivedMTD.total_inr
		elif paymentReceivedMTD.company == 'Turacoz Solutions PTE Ltd.':
			tspl_received_mtd += paymentReceivedMTD.total_inr

	row9 = {}
	row9["particular"] = "Payment Received MTD ({0} {1})".format(month_name,year)
	row9["total"] = '<a href="/app/query-report/Monthly Financial Detailed Preview Report?key=payment_received_mtd" target="_blank">{0}</a>'.format(round(total_received_mtd, 2))
	row9["ths"] = round(ths_received_mtd, 2)
	row9["tbv"] = round(tbv_received_mtd, 2)
	row9["tspl"] = round(tspl_received_mtd, 2)


	total_received_ytd = 0
	ths_received_ytd = 0
	tbv_received_ytd = 0
	tspl_received_ytd = 0
	payment_receivedYTD = payment_received_ytd(year_start_date,todays_date)
	for paymentReceivedYTD in payment_receivedYTD:
		total_received_ytd += paymentReceivedYTD.total_inr
		if paymentReceivedYTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_received_ytd += paymentReceivedYTD.total_inr
		elif paymentReceivedYTD.company == 'Turacoz B.V.':
			tbv_received_ytd += paymentReceivedYTD.total_inr
		elif paymentReceivedYTD.company == 'Turacoz Solutions PTE Ltd.':
			tspl_received_ytd += paymentReceivedYTD.total_inr

	row10 = {}
	row10["particular"] = "Payment Received YTD ({0})".format(year)
	row10["total"] = '<a href="/app/query-report/Monthly Financial Detailed Preview Report?key=payment_received_ytd" target="_blank">{0}</a>'.format(round(total_received_ytd, 2))
	row10["ths"] = round(ths_received_ytd, 2)
	row10["tbv"] = round(tbv_received_ytd, 2)
	row10["tspl"] = round(tspl_received_ytd, 2)

	row11 = {}
	row11["particular"] = "<b>Forecast</b>"


	total_planned_weekly = 0
	ths_planned_weekly = 0
	tbv_planned_weekly = 0
	tspl_planned_weekly = 0
	planned_invoicesWeekly = planned_invoices_weekly(start_of_week,end_of_week)
	for plannedInvoicesWeekly in planned_invoicesWeekly:
		total_planned_weekly += plannedInvoicesWeekly.total_inr
		if plannedInvoicesWeekly.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_planned_weekly += plannedInvoicesWeekly.total_inr
		elif plannedInvoicesWeekly.company == 'Turacoz B.V.':
			tbv_planned_weekly += plannedInvoicesWeekly.total_inr
		elif plannedInvoicesWeekly.company == 'Turacoz Solutions PTE Ltd.':
			tspl_planned_weekly += plannedInvoicesWeekly.total_inr

	row12 = {}
	row12["particular"] = "Planned Invoices to be Raised in <b>{0}</b> to <b>{1}</b>".format(start_of_week,end_of_week)
	row12["total"] = '<a href="/app/query-report/Monthly Financial Detailed Preview Report?key=planned_invoices_to_be_raised_in_week" target="_blank">{0}</a>'.format(round(total_planned_weekly, 2))
	row12["ths"] = round(ths_planned_weekly, 2)
	row12["tbv"] = round(tbv_planned_weekly, 2)
	row12["tspl"] = round(tspl_planned_weekly, 2)


	total_toberaised_mtd = 0
	ths_toberaised_mtd = 0
	tbv_toberaised_mtd = 0
	tspl_toberaised_mtd = 0
	planned_invoices_to_be_raiseMTD = planned_invoices_to_be_raise_mtd(month_name,year)
	for planned_invoices_ToBeraiseMTD in planned_invoices_to_be_raiseMTD:
		total_toberaised_mtd += planned_invoices_ToBeraiseMTD.total_inr
		if planned_invoices_ToBeraiseMTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_toberaised_mtd += planned_invoices_ToBeraiseMTD.total_inr
		elif planned_invoices_ToBeraiseMTD.company == 'Turacoz B.V.':
			tbv_toberaised_mtd += planned_invoices_ToBeraiseMTD.total_inr
		elif planned_invoices_ToBeraiseMTD.company == 'Turacoz Solutions PTE Ltd.':
			tspl_toberaised_mtd += planned_invoices_ToBeraiseMTD.total_inr

	row13 = {}
	row13["particular"] = "Planned Invoices to be Raised in MTD ({0} {1})".format(month_name,year)
	row13["total"] = '<a href="/app/query-report/Monthly Financial Detailed Preview Report?key=planned_invoices_to_be_raised_mtd" target="_blank">{0}</a>'.format(round(total_toberaised_mtd, 2))
	row13["ths"] = round(ths_toberaised_mtd, 2)
	row13["tbv"] = round(tbv_toberaised_mtd, 2)
	row13["tspl"] = round(tspl_toberaised_mtd, 2)


	total_tobereceived_mtd = 0
	ths_tobereceived_mtd = 0
	tbv_tobereceived_mtd = 0
	tspl_tobereceived_mtd = 0
	payment_to_be_receivedMTD = payment_to_be_received_mtd(month_name,year)
	for payment_ToBeReceivedMTD in payment_to_be_receivedMTD:
		total_tobereceived_mtd += payment_ToBeReceivedMTD.total_inr
		if payment_ToBeReceivedMTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_tobereceived_mtd += payment_ToBeReceivedMTD.total_inr
		elif payment_ToBeReceivedMTD.company == 'Turacoz B.V.':
			tbv_tobereceived_mtd += payment_ToBeReceivedMTD.total_inr
		elif payment_ToBeReceivedMTD.company == 'Turacoz Solutions PTE Ltd.':
			tspl_tobereceived_mtd += payment_ToBeReceivedMTD.total_inr
	row14 = {}
	row14["particular"] = "Payment to be Received in MTD ({0} {1})".format(month_name,year)
	row14["total"] = '<a href="/app/query-report/Monthly Financial Detailed Preview Report?key=payment_to_be_received_mtd" target="_blank">{0}</a>'.format(round(total_tobereceived_mtd, 2))
	row14["ths"] = round(ths_tobereceived_mtd, 2)
	row14["tbv"] = round(tbv_tobereceived_mtd, 2)
	row14["tspl"] = round(tspl_tobereceived_mtd, 2)


	total_tobereceived_ytd = 0
	ths_tobereceived_ytd = 0
	tbv_tobereceived_ytd = 0
	tspl_tobereceived_ytd = 0
	payment_to_be_received_cumulativeYTD = payment_to_be_received_cumulative_ytd(todays_date)
	for payment_ToBeReceivedYTD in payment_to_be_received_cumulativeYTD:
		total_tobereceived_ytd += payment_ToBeReceivedYTD.total_inr
		if payment_ToBeReceivedYTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_tobereceived_ytd += payment_ToBeReceivedYTD.total_inr
		elif payment_ToBeReceivedYTD.company == 'Turacoz B.V.':
			tbv_tobereceived_ytd += payment_ToBeReceivedYTD.total_inr
		elif payment_ToBeReceivedYTD.company == 'Turacoz Solutions PTE Ltd.':
			tspl_tobereceived_ytd += payment_ToBeReceivedYTD.total_inr

	row15 = {}
	row15["particular"] = "Payment to be Received in YTD(Cumulative) ({0})".format(year)
	row15["total"] = '<a href="/app/query-report/Monthly Financial Detailed Preview Report?key=payment_to_be_received_ytd" target="_blank">{0}</a>'.format(round(total_tobereceived_ytd, 2))
	row15["ths"] = round(ths_tobereceived_ytd, 2)
	row15["tbv"] = round(tbv_tobereceived_ytd, 2)
	row15["tspl"] = round(tspl_tobereceived_ytd, 2)

	row16 = {}
	row16["particular"] = "<b>Viatris Centre of Excellence</b>"

	total_viatris_actual_invoice_raised_mtd = 0
	ths_viatris_actual_invoice_raised_mtd = 0
	tbv_viatris_actual_invoice_raised_mtd = 0
	tspl_viatris_actual_invoice_raised_mtd = 0
	viatris_actual_invoices_raisedMTD = viatris_actual_invoices_raised_mtd(month_name,year)
	for viatrisActualInvoicesRaisedMTD in viatris_actual_invoices_raisedMTD:
		total_viatris_actual_invoice_raised_mtd += viatrisActualInvoicesRaisedMTD.total_inr
		if viatrisActualInvoicesRaisedMTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_viatris_actual_invoice_raised_mtd += viatrisActualInvoicesRaisedMTD.total_inr
		elif viatrisActualInvoicesRaisedMTD.company == 'Turacoz B.V.':
			tbv_viatris_actual_invoice_raised_mtd += viatrisActualInvoicesRaisedMTD.total_inr
		elif viatrisActualInvoicesRaisedMTD.company == 'Turacoz Solutions PTE Ltd.':
			tspl_viatris_actual_invoice_raised_mtd += viatrisActualInvoicesRaisedMTD.total_inr

	row17 = {}
	row17["particular"] = "Actual Invoices Raise MTD ({0} {1})".format(month_name,year)
	row17["total"] = round(total_viatris_actual_invoice_raised_mtd, 2)
	row17["ths"] = round(ths_viatris_actual_invoice_raised_mtd, 2)
	row17["tbv"] = round(tbv_viatris_actual_invoice_raised_mtd, 2)
	row17["tspl"] = round(tspl_viatris_actual_invoice_raised_mtd, 2)


	total_viatris_actual_invoice_raised_ytd = 0
	ths_viatris_actual_invoice_raised_ytd = 0
	tbv_viatris_actual_invoice_raised_ytd = 0
	tspl_viatris_actual_invoice_raised_ytd = 0
	viatris_actual_invoices_raisedYTD = viatris_actual_invoices_raised_ytd(year_start_date,todays_date)
	for viatrisActualInvoicesRaisedYTD in viatris_actual_invoices_raisedYTD:
		total_viatris_actual_invoice_raised_ytd += viatrisActualInvoicesRaisedYTD.total_inr
		if viatrisActualInvoicesRaisedYTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			ths_viatris_actual_invoice_raised_ytd += viatrisActualInvoicesRaisedYTD.total_inr
		elif viatrisActualInvoicesRaisedYTD.company == 'Turacoz B.V.':
			tbv_viatris_actual_invoice_raised_ytd += viatrisActualInvoicesRaisedYTD.total_inr
		elif viatrisActualInvoicesRaisedYTD.company == 'Turacoz Solutions PTE Ltd.':
			tspl_viatris_actual_invoice_raised_ytd += viatrisActualInvoicesRaisedYTD.total_inr

	row18 = {}
	row18["particular"] = "Actual Invoices Raise YTD ({0})".format(year)
	row18["total"] = round(total_viatris_actual_invoice_raised_ytd, 2)
	row18["ths"] = round(ths_viatris_actual_invoice_raised_ytd, 2)
	row18["tbv"] = round(tbv_viatris_actual_invoice_raised_ytd, 2)
	row18["tspl"] = round(tspl_viatris_actual_invoice_raised_ytd, 2)

	viatris_total_payment_received_mtd = 0
	viatris_ths_payment_received_mtd = 0
	viatris_tbv_payment_received_mtd = 0
	viatris_tspl_payment_received_mtd = 0
	viatris_payment_receivedMTD = viatris_payment_received_mtd(month_name,year)
	for viatris_paymentReceivedMTD in viatris_payment_receivedMTD:
		viatris_total_payment_received_mtd += viatris_paymentReceivedMTD.total_inr
		if viatris_paymentReceivedMTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			viatris_ths_payment_received_mtd += viatris_paymentReceivedMTD.total_inr
		elif viatris_paymentReceivedMTD.company == 'Turacoz B.V.':
			viatris_tbv_payment_received_mtd += viatris_paymentReceivedMTD.total_inr
		elif viatris_paymentReceivedMTD.company == 'Turacoz Solutions PTE Ltd.':
			viatris_tspl_payment_received_mtd += viatris_paymentReceivedMTD.total_inr	

	row19 = {}
	row19["particular"] = "Payment Received MTD ({0} {1})".format(month_name,year)
	row19["total"] = round(viatris_total_payment_received_mtd, 2)
	row19["ths"] = round(viatris_ths_payment_received_mtd, 2)
	row19["tbv"] = round(viatris_tbv_payment_received_mtd, 2)
	row19["tspl"] = round(viatris_tspl_payment_received_mtd, 2)


	viatris_total_payment_received_ytd = 0
	viatris_ths_payment_received_ytd = 0
	viatris_tbv_payment_received_ytd = 0
	viatris_tspl_payment_received_ytd = 0
	viatris_payment_receivedYTD = viatris_payment_received_ytd(year_start_date,todays_date)
	for viatris_paymentReceivedYTD in viatris_payment_receivedYTD:
		viatris_total_payment_received_ytd += viatris_paymentReceivedYTD.total_inr
		if viatris_paymentReceivedYTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			viatris_ths_payment_received_ytd += viatris_paymentReceivedYTD.total_inr
		elif viatris_paymentReceivedYTD.company == 'Turacoz B.V.':
			viatris_tbv_payment_received_ytd += viatris_paymentReceivedYTD.total_inr
		elif viatris_paymentReceivedYTD.company == 'Turacoz Solutions PTE Ltd.':
			viatris_tspl_payment_received_ytd += viatris_paymentReceivedYTD.total_inr	

	row20 = {}
	row20["particular"] = "Payment Received YTD ({0})".format(year)
	row20["total"] = round(viatris_total_payment_received_ytd, 2)
	row20["ths"] = round(viatris_ths_payment_received_ytd, 2)
	row20["tbv"] = round(viatris_tbv_payment_received_ytd, 2)
	row20["tspl"] = round(viatris_tspl_payment_received_ytd, 2)


	viatris_total_payment_tobe_received_mtd = 0
	viatris_ths_payment_tobe_received_mtd = 0
	viatris_tbv_payment_tobe_received_mtd = 0
	viatris_tspl_payment_tobe_received_mtd = 0
	viatris_payment_to_be_receivedMTD = viatris_payment_to_be_received_mtd(month_name,year)
	for viatris_payment_to_beReceivedMTD in viatris_payment_to_be_receivedMTD:
		viatris_total_payment_tobe_received_mtd += viatris_payment_to_beReceivedMTD.total_inr
		if viatris_payment_to_beReceivedMTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			viatris_ths_payment_tobe_received_mtd += viatris_payment_to_beReceivedMTD.total_inr
		elif viatris_payment_to_beReceivedMTD.company == 'Turacoz B.V.':
			viatris_tbv_payment_tobe_received_mtd += viatris_payment_to_beReceivedMTD.total_inr
		elif viatris_payment_to_beReceivedMTD.company == 'Turacoz Solutions PTE Ltd.':
			viatris_tspl_payment_tobe_received_mtd += viatris_payment_to_beReceivedMTD.total_inr

	row21 = {}
	row21["particular"] = "Payment to be Received in MTD ({0} {1})".format(month_name,year)
	row21["total"] = round(viatris_total_payment_tobe_received_mtd, 0)
	row21["ths"] = round(viatris_ths_payment_tobe_received_mtd, 2)
	row21["tbv"] = round(viatris_tbv_payment_tobe_received_mtd, 2)
	row21["tspl"] = round(viatris_tspl_payment_tobe_received_mtd, 2)


	viatris_total_payment_tobe_received_ytd = 0
	viatris_ths_payment_tobe_received_ytd = 0
	viatris_tbv_payment_tobe_received_ytd = 0
	viatris_tspl_payment_tobe_received_ytd = 0
	viatris_payment_to_be_receivedYTD = viatris_payment_to_be_received_cumulative_ytd(todays_date)
	for viatris_payment_to_beReceivedYTD in viatris_payment_to_be_receivedYTD:
		viatris_total_payment_tobe_received_ytd += viatris_payment_to_beReceivedYTD.total_inr
		if viatris_payment_to_beReceivedYTD.company == 'Turacoz Healthcare Solutions Pvt Ltd':
			viatris_ths_payment_tobe_received_ytd += viatris_payment_to_beReceivedYTD.total_inr
		elif viatris_payment_to_beReceivedYTD.company == 'Turacoz B.V.':
			viatris_tbv_payment_tobe_received_ytd += viatris_payment_to_beReceivedYTD.total_inr
		elif viatris_payment_to_beReceivedYTD.company == 'Turacoz Solutions PTE Ltd.':
			viatris_tspl_payment_tobe_received_ytd += viatris_payment_to_beReceivedYTD.total_inr


	row22 = {}
	row22["particular"] = "Payment to be Received in YTD(Cumulative) ({0})".format(year)
	row22["total"] = round(viatris_total_payment_tobe_received_ytd, 2)
	row22["ths"] = round(viatris_ths_payment_tobe_received_ytd, 2)
	row22["tbv"] = round(viatris_tbv_payment_tobe_received_ytd, 2)
	row22["tspl"] = round(viatris_tspl_payment_tobe_received_ytd, 2)

	data.append(row)
	data.append(row1)
	data.append(row2)
	data.append(row3)
	data.append(row4)
	data.append(row5)
	data.append(row6)
	data.append(row7)
	data.append(row8)
	data.append(row9)
	data.append(row10)
	data.append(row11)
	data.append(row12)
	data.append(row13)
	data.append(row14)
	data.append(row15)
	data.append(row16)
	data.append(row17)
	data.append(row18)
	data.append(row19)
	data.append(row20)
	data.append(row21)
	data.append(row22)


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
			"fieldname": "total",
			"label": _("Total"),
			"fieldtype": "Data",
			"width": "150"
		},
		{
			"fieldname": "ths",
			"label": _("THS"),
			"fieldtype": "Data",
			"width": "150"
		},	
		{
			"fieldname": "tbv",
			"label": _("TBV"),
			"fieldtype": "Data",
			"width": "150"
		},	
		{
			"fieldname": "tspl",
			"label": _("TSPL"),
			"fieldtype": "Data",
			"width": "150"
		},		
	]
	return cols

def get_fiscal_year():
	data = frappe.db.sql("""select year_start_date,year_end_date from `tabFiscal Year` tfy WHERE disabled = 0""",as_dict=True)
	return data


def overdue_unraised_invoices_till_date(todays_date):
	data = frappe.db.sql("""select tsi.company,sum(ter.rate_in_inr * tps.payment_amount) as total_inr
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled') and tp.project_current_status not in ('Cancelled') and tps.invoice_status = 'Unraised'
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		tps.due_date <= '{0}' group by tsi.company""".format(todays_date),as_dict = True)
	return data

def actual_invoices_raised_mtd(month_name,year):
	data = frappe.db.sql("""select tpr.company,
		sum(CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(ter.rate_in_inr * tpr.grand_total,0)
		END) as 'total_inr'
		from `tabPayment Request` tpr 
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tpr.currency = ter.name
		WHERE tpr.status not in ('Cancelled')
		and tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}'
		group by tpr.company""".format(month_name,year),as_dict = True)
	return data

def actual_invoices_raised_ytd(year_start_date,todays_date):
	data = frappe.db.sql("""select tpr.company,
		sum(CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(ter.rate_in_inr * tpr.grand_total,0)
		END) as 'total_inr'
		from `tabPayment Request` tpr 
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tpr.currency = ter.name
		WHERE tpr.status not in ('Cancelled')
		and tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		date(tpr.invoice_date) BETWEEN  '{0}' and '{1}'
		group by tpr.company""".format(year_start_date,todays_date),as_dict = True)
	return data

def payment_received_mtd(month_name,year):
	data = frappe.db.sql("""select tpr.company,
		sum(CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(ter.rate_in_inr * tpr.grand_total,0)
		END) as 'total_inr'			  
		from `tabPayment Request` tpr 
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tpr.currency = ter.name
		WHERE tpr.status not in ('Cancelled') and payment_status in ('Paid')
		and tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}'
		GROUP BY tpr.company""".format(month_name,year), as_dict = True)
	return data

def payment_received_ytd(year_start_date,todays_date):
	data = frappe.db.sql("""select tpr.company,
		sum(CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(ter.rate_in_inr * tpr.grand_total,0)
		END) as 'total_inr'			  
		from `tabPayment Request` tpr 
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tpr.currency = ter.name
		WHERE tpr.status not in ('Cancelled') and tpr.payment_status in ('Paid')
		and tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd','Turacoz B.V.') and
		date(tpr.payment_date) BETWEEN  '{0}' and '{1}'
		group by tpr.company""".format(year_start_date,todays_date), as_dict = True)
	return data

def planned_invoices_to_be_raise_mtd(month_name,year):
	data = frappe.db.sql("""select tsi.company,sum(IFNULL(ter.rate_in_inr * tps.payment_amount,0)) as total_inr
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled')
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}'
		GROUP BY tsi.company""".format(month_name,year), as_dict = True)
	return data

def payment_to_be_received_mtd(month_name,year):
	data = frappe.db.sql("""SELECT tpr.company,
		sum(CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(tcer.rate_in_inr * tpr.grand_total,0)
		END) as 'total_inr'			  
		FROM `tabPayment Request` tpr
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` tcer on tpr.invoice_currency = tcer.name
		WHERE tpr.payment_status in ('Unpaid','Overdue') 
		and tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')		  
		AND MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' 
		and YEAR(tpr.due_date) = '{1}' GROUP BY tpr.company;""".format(month_name,year), as_dict = True)
	return data

def payment_to_be_received_cumulative_ytd(todays_date):
	data = frappe.db.sql("""SELECT tpr.company,
		sum(CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(tcer.rate_in_inr * tpr.grand_total,0)
		END) as 'total_inr'			  
		FROM `tabPayment Request` tpr
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` tcer on tpr.invoice_currency = tcer.name
		WHERE tpr.payment_status in ('Unpaid','Overdue')
		and tpr.customer_name not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')			   
		AND date(tpr.due_date) <= '{0}' GROUP BY tpr.company;""".format(todays_date), as_dict = True)
	return data

def planned_invoices_weekly(start_of_week,end_of_week):
	data = frappe.db.sql("""select tsi.company,sum(IFNULL(ter.rate_in_inr * tps.payment_amount,0)) as total_inr
		from `tabSales Invoice` tsi 
		left join `tabPayment Schedule` tps on tsi.name = tps.parent
		left join `tabProject` tp on tsi.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
		WHERE tsi.status not in ('Paid','Cancelled')
		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
		date(tps.due_date) BETWEEN  '{0}' and '{1}'
		GROUP BY tsi.company""".format(start_of_week,end_of_week), as_dict = True)
	return data

def new_po_received_mtd(month_name,year):
	data = frappe.db.sql("""select tpdt.company, sum(IFNULL(ter.rate_in_inr * tpdt.project_cost,0)) as total_inr 
		from `tabProject Detail Template` tpdt
		left join `tabCurrency Exchange Rate` ter on tpdt.currency  = ter.name 
		where tpdt.workflow_state not in ('Rejected') and tpdt.popcd_status in ('Received')
		and tpdt.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')			  
		and MONTHNAME(STR_TO_DATE(MONTH(tpdt.popcd_date),'%m')) = '{0}' 
		and YEAR(tpdt.popcd_date) = '{1}' GROUP BY tpdt.company;""".format(month_name,year), as_dict = True)
	return data


def new_po_received_ytd(year_start_date,todays_date):
	data = frappe.db.sql("""select tpdt.company, sum(IFNULL(ter.rate_in_inr * tpdt.project_cost,0)) as total_inr
		from `tabProject Detail Template` tpdt
		left join `tabCurrency Exchange Rate` ter on tpdt.currency  = ter.name 
		where tpdt.workflow_state not in ('Rejected') and tpdt.popcd_status in ('Received')
		and tpdt.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
		and date(tpdt.popcd_date) BETWEEN  '{0}' and '{1}' group by tpdt.company""".format(year_start_date,todays_date), as_dict = True)
	return data

def pending_po_till_today(todays_date):
	data = frappe.db.sql("""select tpdt.company, sum(IFNULL(ter.rate_in_inr * tpdt.project_cost,0)) as total_inr
		from `tabProject Detail Template` tpdt
		left join `tabCurrency Exchange Rate` ter on tpdt.currency  = ter.name 
		where tpdt.workflow_state not in ('Rejected') and tpdt.popcd_status in ('Pending')
		and tpdt.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
		group by tpdt.company""".format(todays_date), as_dict = True)
	return data

# Viatris 

def viatris_actual_invoices_raised_mtd(month_name,year):
	data = frappe.db.sql("""select tpr.company,
		sum(CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(ter.rate_in_inr * tpr.grand_total,0)
		END) as 'total_inr'
		from `tabPayment Request` tpr 
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tpr.currency = ter.name
		WHERE tpr.status not in ('Cancelled')
		and tpr.customer_name in ('Viatris Centre of Excellence') and
		MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}'
		group by tpr.company""".format(month_name,year),as_dict = True)
	return data

def viatris_actual_invoices_raised_ytd(year_start_date,todays_date):
	data = frappe.db.sql("""select tpr.company,
		sum(CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(ter.rate_in_inr * tpr.grand_total,0)
		END) as 'total_inr'
		from `tabPayment Request` tpr 
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tpr.currency = ter.name
		WHERE tpr.status not in ('Cancelled')
		and tpr.customer_name in ('Viatris Centre of Excellence') and
		date(tpr.invoice_date) BETWEEN  '{0}' and '{1}'
		group by tpr.company""".format(year_start_date,todays_date),as_dict = True)
	return data

def viatris_payment_received_mtd(month_name,year):
	data = frappe.db.sql("""select tpr.company,
		sum(CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(ter.rate_in_inr * tpr.grand_total,0)
		END) as 'total_inr'			  
		from `tabPayment Request` tpr 
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tpr.currency = ter.name
		WHERE tpr.status not in ('Cancelled') and payment_status in ('Paid')
		and tpr.customer_name in ('Viatris Centre of Excellence') and
		MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}'
		GROUP BY tpr.company""".format(month_name,year), as_dict = True)
	return data

def viatris_payment_received_ytd(year_start_date,todays_date):
	data = frappe.db.sql("""select tpr.company,
		sum(CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(ter.rate_in_inr * tpr.grand_total,0)
		END) as 'total_inr'			  
		from `tabPayment Request` tpr 
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` ter on tpr.currency = ter.name
		WHERE tpr.status not in ('Cancelled') and tpr.payment_status in ('Paid')
		and tpr.customer_name in ('Viatris Centre of Excellence') and
		date(tpr.payment_date) BETWEEN  '{0}' and '{1}'
		group by tpr.company""".format(year_start_date,todays_date), as_dict = True)
	return data

def viatris_payment_to_be_received_mtd(month_name,year):
	data = frappe.db.sql("""SELECT tpr.company,
		sum(CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(tcer.rate_in_inr * tpr.grand_total,0)
		END) as 'total_inr'			  
		FROM `tabPayment Request` tpr
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` tcer on tpr.invoice_currency = tcer.name
		WHERE tpr.payment_status in ('Unpaid','Overdue') 
		and tpr.customer_name in ('Viatris Centre of Excellence')		  
		AND MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' 
		and YEAR(tpr.due_date) = '{1}' GROUP BY tpr.company;""".format(month_name,year), as_dict = True)
	return data

def viatris_payment_to_be_received_cumulative_ytd(todays_date):
	data = frappe.db.sql("""SELECT tpr.company,
		sum(CASE
		WHEN tpr.currency='INR' THEN ((tpr.net_total+tpr.total_taxes)-(tpr.net_total*0.10))
		ELSE IFNULL(tcer.rate_in_inr * tpr.grand_total,0)
		END) as 'total_inr'			  
		FROM `tabPayment Request` tpr
		left join `tabProject` tp on tpr.project = tp.name
		left join `tabCurrency Exchange Rate` tcer on tpr.invoice_currency = tcer.name
		WHERE tpr.payment_status in ('Unpaid','Overdue')
		and tpr.customer_name in ('Viatris Centre of Excellence')			   
		AND date(tpr.due_date) <= '{0}' GROUP BY tpr.company;""".format(todays_date), as_dict = True)
	return data
	