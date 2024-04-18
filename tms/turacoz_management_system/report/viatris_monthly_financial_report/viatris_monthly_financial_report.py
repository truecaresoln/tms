# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	start_date = filters.get("from_date")
	data=[]
	data4 = frappe.db.sql("""select payment_date,sum(net_total) as 'payment_received_in_bank',sum(igst) as 'gst',(sum(net_total)*0.10) as 'tds',(sum(net_total)+sum(igst))-(sum(net_total)*0.10) as 'amount_received'  from `tabPayment Request` tpr where customer_name in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and payment_date>='{0}' and payment_status in ('Paid','Partly Paid') and status not in ('Cancelled') group by payment_date order by 1 desc
			""".format(start_date),as_dict=True)
	raised=0
	a=0
	b=0
	raised_tot=0
	received_tot=0
	balance_tot=0
	bank_tot=0
	received_amount=0	
	balance=0

	start_date1 = datetime.strptime(start_date, '%Y-%m-%d').date()
	last_date1 = datetime.now().date()
	x=0
	while start_date1<last_date1:
		x = x + 1
		month=start_date1.month
		year=start_date1.year
		print(month)
		print(year)
		row={}
		month_year = calendar.month_name[month] + ' , ' + str(year)
		row['month'] = "<div><span><b>%s</b></span></div>" %month_year

		data1 = frappe.db.sql("""select MONTH(invoice_date),MONTHNAME(invoice_date) as 'month',sum(grand_total) as 'raised_amount',sum(net_total)*0.1 as 'tds'  from `tabPayment Request` tpr where customer_name in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and MONTH(invoice_date)='{0}' and YEAR(invoice_date)='{1}' and payment_status not in ('Cancelled') and status not in ('Cancelled') group by MONTHNAME(invoice_date) order by 1
		""".format(month,year))
		if data1:
			row['raised_amount'] = round(float(data1[0][2]),2)
			a = a + round(float(data1[0][2]),2)
			row['received_amount'] = round(float(data1[0][3]),2)
			b = b + round(float(data1[0][3]),2)
			row['balance'] = round(row['raised_amount']-row['received_amount'],2)
			raised_tot = raised_tot + round(row['raised_amount']-row['received_amount'],2)
			raised = round(row['raised_amount']-row['received_amount'],2)
		else:
			row['raised_amount'] = 0.0
			a = a + 0.0
			row['received_amount'] = 0.0
			b = b + 0.0
			row['balance'] = 0.0
			raised_tot = raised_tot + 0.0
			raised = 0.0	
		
		data2 = frappe.db.sql("""select MONTH(invoice_date),MONTHNAME(invoice_date) as 'month',sum(grand_total)-sum(net_total)*0.1 as 'received_amount'  from `tabPayment Request` tpr where customer_name in ('Viatris Centre of Excellence','Mylan Centre of Excellence')
			and MONTH(invoice_date)='{0}' and YEAR(invoice_date)='{1}' and payment_status in ('Paid','Partly Paid') and status not in ('Cancelled') group by MONTHNAME(invoice_date) order by 1
			""".format(month,year))

		if data2:
			row['payment_received'] = round(float(data2[0][2]),2)
			received_amount=round(float(data2[0][2]),2)
			received_tot = received_tot + round(float(data2[0][2]),2)
			balance = raised - received_amount
			row['transaction_details'] = round(balance,2) 		
			balance_tot = balance_tot + balance			
		else:
			row['payment_received'] = 0.0
			received_amount=0.0
			received_tot = received_tot + 0.0
			balance = raised - received_amount
			row['transaction_details'] = round(balance,2) 		
			balance_tot = balance_tot + balance			

		data3 = frappe.db.sql("""select MONTH(date_of_transaction),YEAR(date_of_transaction),sum(transaction_amount) from `tabBank Transaction Details`
				where customer in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and MONTH(date_of_transaction)='{0}' and YEAR(date_of_transaction)='{1}' group by MONTH(date_of_transaction),YEAR(date_of_transaction) order by 1
			""".format(month,year))
		
		if data3:
			row['diff'] = round(float(data3[0][2]),2)
			bank_tot = bank_tot + round(float(data3[0][2]),2)
		else:
			row['diff'] = 0.0
		data.append(row)
		start_date1 = start_date1 + relativedelta(months=+1)

	row={}
	row['month'] = "<div><span><b>Total:</b></span></div>"
	row['raised_amount'] = "<div><span><b>%s</b></span></div>" %round(a,2)
	row['received_amount'] = "<div><span><b>%s</b></span></div>" %round(b,2)
	row['balance'] = "<div><span><b>%s</b></span></div>" %round(raised_tot,2)
	row['payment_received'] = "<div><span><b>%s</b></span></div>" %round(received_tot,2)
	row['transaction_details'] = "<div><span><b>%s</b></span></div>" %round(balance_tot,2)
	row['diff'] = "<div><span><b>%s</b></span></div>" %round(bank_tot,2)
	data.append(row)
	row={}
	data.append(row)
	row={}
	row['month'] = "<div><span><center><b>Payment Date in Bank</b></center></span></div>"
	row['raised_amount'] = "<div><span><center><b>Basic Amount (A)</b></center></span></div>"
	row['received_amount'] = "<div><span><center><b>GST (B = 18% of A)</b></center></span></div>"
	row['balance'] = "<div><span><center><b>TDS (C = 10% of A)</b></center></span></div>"
	row['payment_received'] = "<div><span><center><b>Gross Amount Receivable (A+B-C)</b></center></span></div>"
	row['transaction_details'] = "<div><span><center><b>Gross Amount Received</b></center></span></div>"
	row['diff'] = "<div><span><center><b>Difference</b></center></span></div>"
	data.append(row)
	
	payment_received_in_bank=0
	tds=0
	gst=0
	received_amount_bank=0
	exact_amount_bank=0
	diff_amount=0
	for rec in data4:
		row={}
		row['month'] = "<div><span><center><b>%s</b></center></span></div>" %rec.payment_date
		row['raised_amount'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(rec.payment_received_in_bank,2))
		row['received_amount'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(rec.gst,2))
		row['balance'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(rec.tds,2))
		row['payment_received'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(rec.amount_received,2))
		payment_received_in_bank = payment_received_in_bank + round(rec.payment_received_in_bank,2)
		gst = gst + round(rec.gst,2)
		tds = tds + round(rec.tds,2)
		received_amount_bank = received_amount_bank + round(rec.amount_received,2)
		data5 = frappe.db.sql("""select date_of_transaction,transaction_amount  from `tabBank Transaction Details` 
				where customer='Viatris Centre of Excellence' and date_of_transaction='{0}'""".format(rec.payment_date))
		if data5:
			row['transaction_details'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(float(data5[0][1]),2))
			exact_amount_bank = exact_amount_bank + float(data5[0][1])
			diff1 = round(rec.amount_received,2) - round(float(data5[0][1]),2)
			row['diff'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(diff1,2)) 
			diff_amount = diff_amount + round(diff1,2)
		data.append(row) 

	row={}
	row['month'] = "<div><span><b>Total:</b></span></div>"
	row['raised_amount'] = "<div><span><center><b>%s</b></center></span></div>" %payment_received_in_bank
	row['received_amount'] = "<div><span><center><b>%s</b></center></span></div>" %round(gst,2)
	row['balance'] = "<div><span><center><b>%s</b></center></span></div>" %round(tds,2)
	row['payment_received'] = "<div><span><center><b>%s</b></center></span></div>" %round(received_amount_bank,2)
	row['transaction_details'] = "<div><span><center><b>%s</b></center></span></div>" %round(exact_amount_bank,2)
	row['diff'] = "<div><span><center><b>%s</b></center></span></div>" %round(diff_amount,2)
	data.append(row)
	
	return data

def get_columns(filters):
			cols=[
			{
				"fieldname": "month",
				"label": _("Month"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "raised_amount",
				"label": _("Invoice Raised (A = Basic + GST)"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "received_amount",
				"label": _("TDS (B = 10% of Basic)"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "balance",
				"label": _("Amount Receivable after deducting TDS (C = A-B)"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "payment_received",
				"label": _("Amount Received From C"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "transaction_details",
				"label": _("Balance"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "diff",
				"label": _("Payment Received As per Bank Statement"),
				"fieldtype": "Data",
				"width": "200"
			}

		]
			return cols
