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
	raised=0
	raised_tot=0
	received_tot=0
	balance_tot=0
	bank_tot=0
	received_amount=0	
	balance=0

	start_date1 = datetime.strptime(start_date, '%Y-%m-%d').date()
	last_date1 = datetime.now().date()

	x=0
	row={}
	row['month'] = "<div><span><b>Company: Turacoz B.V.</b></span></div>"
	data.append(row)
	while start_date1<last_date1:
		x = x + 1
		month=start_date1.month
		year=start_date1.year
		row={}
		month_year = calendar.month_name[month] + ' , ' + str(year)
		row['month'] = "<div><span><b>%s</b></span></div>" %month_year

		data1 = frappe.db.sql("""select MONTH(invoice_date),MONTHNAME(invoice_date) as 'month',net_total as 'net_amount',currency,conversion_rate,net_total * conversion_rate as 'raised_amount'
			from `tabPayment Request` tpr 
			where company='Turacoz B.V.' and customer_name not in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and MONTH(invoice_date)='{0}' and YEAR(invoice_date)='{1}' and payment_status not in ('Cancelled') and status not in ('Cancelled') group by currency  order by 1""".format(month,year),as_dict=True)
		if data1:
			raise_amt=0
			for rec in data1:
				if rec.currency == 'USD':
					raise_amt = raise_amt + round(float(rec.raised_amount),2)
				else:
					raise_amt = raise_amt + round(float(rec.raised_amount),2)
				
			row['raised_amount'] = round(float(raise_amt),2)
			raised_tot = raised_tot + round(float(raise_amt),2)
			raised = round(float(raise_amt),2)
		else:
			row['raised_amount'] = 0.0
			raised_tot = raised_tot + 0.0
			raised = 0.0	
		
		data2 = frappe.db.sql("""select MONTH(invoice_date),MONTHNAME(invoice_date) as 'month',net_total as 'net_amount',currency,conversion_rate,net_total * conversion_rate as 'received_amount' 
			from `tabPayment Request` tpr 
			where company='Turacoz B.V.' and customer_name not in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and MONTH(invoice_date)='{0}' and YEAR(invoice_date)='{1}' and payment_status in ('Paid','Partly Paid') and status not in ('Cancelled') group by currency order by 1""".format(month,year),as_dict=True)

		if data2:
			receive_amt=0;
			for rec in data2:
				if rec.currency == 'USD':
					receive_amt = receive_amt + round(float(rec.received_amount),2)
				else:
					receive_amt = receive_amt + round(float(rec.received_amount),2)
			row['received_amount'] = round(receive_amt,2)
			received_amount=round(receive_amt,2)
			received_tot = received_tot + round(receive_amt,2)
			balance = raised - received_amount
			row['balance'] = round(balance,2) 		
			balance_tot = balance_tot + balance			
		else:
			row['received_amount'] = 0.0
			balance = raised - 0.0
			row['balance'] = round(balance,2) 		
			balance_tot = balance_tot + balance			

		data3 = frappe.db.sql("""select MONTH(invoice_date),MONTHNAME(payment_date) as 'month',net_total as 'net_total',currency,conversion_rate,net_total * conversion_rate as 'payment_received'  
			from `tabPayment Request` tpr 
			where company='Turacoz B.V.' and customer_name not in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and MONTH(payment_date)='{0}' and YEAR(payment_date)='{1}' and payment_status in ('Paid','Partly Paid') and status not in ('Cancelled')  order by 1			""".format(month,year),as_dict=True)
		
		if data3:
			payment_amt=0;
			for rec in data3:
				payment_amt = payment_amt + round(float(rec.payment_received),2)
		
			row['payment_received'] = round(payment_amt,2)
			bank_tot = bank_tot + round(payment_amt,2)
		else:
			row['payment_received'] = 0.0
		data.append(row)
		start_date1 = start_date1 + relativedelta(months=+1)

	row={}
	row['month'] = "<div><span><b>Total:</b></span></div>"
	row['raised_amount'] = "<div><span><b>%s</b></span></div>" %round(raised_tot,2)
	row['received_amount'] = "<div><span><b>%s</b></span></div>" %round(received_tot,2)
	row['balance'] = "<div><span><b>%s</b></span></div>" %round(balance_tot,2)
	row['payment_received'] = "<div><span><b>%s</b></span></div>" %round(bank_tot,2)
	data.append(row)
	row={}
	data.append(row)
	row={}
	row['month'] = "<div><span><center><b>Payment Date in Bank</b></center></span></div>"
	row['raised_amount'] = "<div><span><center><b>Amount Received in EUR</b></center></span></div>"
	row['received_amount'] = "<div><span><center><b>VAT</b></center></span></div>"
	row['balance'] = "<div><span><center><b>Gross Payment Received</b></center></span></div>"
	row['payment_received'] = "<div><span><center><b>Payment Received in Bank</b></center></span></div>"
	row['transaction_details'] = "<div><span><center><b>Difference</b></center></span></div>"
	row['diff'] = "<div><span><center><b>Amount Received in INR</b></center></span></div>"
	data.append(row)
	
	data4 = frappe.db.sql("""select payment_date,sum(net_total*conversion_rate) as 'payment_received_in_bank',sum(total_taxes) as 'gst',sum(net_total*conversion_rate)+sum(total_taxes) as 'gross',tpr.currency,sum(net_total*conversion_rate)*ter.rate_in_inr as 'amount_inr'  
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.currency  = ter.name
		where company='Turacoz B.V.' and customer_name not in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and payment_date>='{0}' and payment_status in ('Paid','Partly Paid') and status not in ('Cancelled') group by payment_date order by 1 desc""".format(start_date),as_dict=True)

	payment_received_in_bank=0
	amount_inr=0
	gst=0
	received_amount_bank=0
	exact_amount_bank=0
	diff_amount=0
	for rec in data4:
		row={}
		row['month'] = "<div><span><center><b>%s</b></center></span></div>" %rec.payment_date
		row['raised_amount'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(rec.payment_received_in_bank,2))
		row['received_amount'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(rec.gst,2))
		row['balance'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(rec.gross,2))
		row['diff'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(rec.amount_inr,2))
		payment_received_in_bank = payment_received_in_bank + round(rec.payment_received_in_bank,2)
		amount_inr = amount_inr + round(rec.amount_inr,2)
		gst = gst + round(rec.gst,2)
		received_amount_bank = received_amount_bank + round(rec.gross,2)
		data5 = frappe.db.sql("""select date_of_transaction,if(sum(transaction_amount) is null,0.0,sum(transaction_amount)) from `tabBank Transaction Details` 
				where company='Turacoz B.V.' and customer not in ('Viatris Centre of Excellence') and date_of_transaction='{0}'""".format(rec.payment_date))
		if data5:
			row['payment_received'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(float(data5[0][1]),2))
			exact_amount_bank = exact_amount_bank + float(data5[0][1])
			diff1 = round(rec.gross,2) - round(float(data5[0][1]),2)
			row['transaction_details'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(diff1,2)) 
			diff_amount = diff_amount + round(diff1,2)
		data.append(row) 

	row={}
	row['month'] = "<div><span><b>Total:</b></span></div>"
	row['raised_amount'] = "<div><span><center><b>%s</b></center></span></div>" %round(payment_received_in_bank,2)
	row['received_amount'] = "<div><span><center><b>%s</b></center></span></div>" %round(gst,2)
	row['balance'] = "<div><span><center><b>%s</b></center></span></div>" %round(received_amount_bank,2)
	row['diff'] = "<div><span><center><b>%s</b></center></span></div>" %round(amount_inr,2)
	row['payment_received'] = "<div><span><center><b>%s</b></center></span></div>" %round(exact_amount_bank,2)
	row['transaction_details'] = "<div><span><center><b>%s</b></center></span></div>" %round(diff_amount,2)
	data.append(row)

	raised=0
	raised_tot=0
	received_tot=0
	balance_tot=0
	bank_tot=0
	received_amount=0	
	balance=0
	start_date1 = datetime.strptime(start_date, '%Y-%m-%d').date()
	last_date1 = datetime.now().date()
	x=0
	row={}
	row['month'] = "<div><span><b>Company: Turacoz Solutions PTE Ltd.</b></span></div>"
	data.append(row)
	while start_date1<last_date1:
		x = x + 1
		month=start_date1.month
		year=start_date1.year
		row={}
		month_year = calendar.month_name[month] + ' , ' + str(year)
		row['month'] = "<div><span><b>%s</b></span></div>" %month_year

		data1 = frappe.db.sql("""select MONTH(invoice_date),MONTHNAME(invoice_date) as 'month',net_total as 'net_amount',currency,conversion_rate,net_total * conversion_rate as 'raised_amount'
			from `tabPayment Request` tpr 
			where company='Turacoz Solutions PTE Ltd.' and customer_name not in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and MONTH(invoice_date)='{0}' and YEAR(invoice_date)='{1}' and payment_status not in ('Cancelled') and status not in ('Cancelled') group by currency order by 1""".format(month,year),as_dict=True)
		if data1:
			raise_amt=0
			for rec in data1:
				raise_amt = raise_amt + round(float(rec.raised_amount),2)
				
			row['raised_amount'] = round(float(raise_amt),2)
			raised_tot = raised_tot + round(float(raise_amt),2)
			raised = round(float(raise_amt),2)
		else:
			row['raised_amount'] = 0.0
			raised_tot = raised_tot + 0.0
			raised = 0.0	
		
		data2 = frappe.db.sql("""select MONTH(invoice_date),MONTHNAME(invoice_date) as 'month',net_total as 'net_amount',currency,conversion_rate,net_total * conversion_rate as 'received_amount' 
			from `tabPayment Request` tpr 
			where company='Turacoz Solutions PTE Ltd.' and customer_name not in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and MONTH(invoice_date)='{0}' and YEAR(invoice_date)='{1}' and payment_status in ('Paid','Partly Paid') and status not in ('Cancelled') group by currency order by 1""".format(month,year),as_dict=True)

		if data2:
			receive_amt=0;
			for rec in data2:
				receive_amt = receive_amt + round(float(rec.received_amount),2)
			row['received_amount'] = round(receive_amt,2)
			received_amount=round(receive_amt,2)
			received_tot = received_tot + round(receive_amt,2)
			balance = raised - received_amount
			row['balance'] = round(balance,2) 		
			balance_tot = balance_tot + balance			
		else:
			row['received_amount'] = 0.0
			balance = raised - 0.0
			row['balance'] = round(balance,2) 		
			balance_tot = balance_tot + balance			

		data3 = frappe.db.sql("""select MONTH(invoice_date),MONTHNAME(payment_date) as 'month',net_total as 'net_total',currency,conversion_rate,net_total * conversion_rate as 'payment_received'  
			from `tabPayment Request` tpr 
			where company='Turacoz Solutions PTE Ltd.' and customer_name not in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and MONTH(payment_date)='{0}' and YEAR(payment_date)='{1}' and payment_status in ('Paid','Partly Paid') and status not in ('Cancelled')  order by 1			""".format(month,year),as_dict=True)
		
		if data3:
			payment_amt=0;
			for rec in data3:
				payment_amt = payment_amt + round(float(rec.payment_received),2)
		
			row['payment_received'] = round(payment_amt,2)
			bank_tot = bank_tot + round(payment_amt,2)
		else:
			row['payment_received'] = 0.0
		data.append(row)
		start_date1 = start_date1 + relativedelta(months=+1)

	row={}
	row['month'] = "<div><span><b>Total:</b></span></div>"
	row['raised_amount'] = "<div><span><b>%s</b></span></div>" %round(raised_tot,2)
	row['received_amount'] = "<div><span><b>%s</b></span></div>" %round(received_tot,2)
	row['balance'] = "<div><span><b>%s</b></span></div>" %round(balance_tot,2)
	row['payment_received'] = "<div><span><b>%s</b></span></div>" %round(bank_tot,2)
	data.append(row)
	row={}
	data.append(row)
	row={}
	row['month'] = "<div><span><center><b>Payment Date in Bank</b></center></span></div>"
	row['raised_amount'] = "<div><span><center><b>Amount Received in USD</b></center></span></div>"
	row['received_amount'] = "<div><span><center><b>VAT</b></center></span></div>"
	row['balance'] = "<div><span><center><b>Gross Payment Received</b></center></span></div>"
	row['payment_received'] = "<div><span><center><b>Payment Received in Bank</b></center></span></div>"
	row['transaction_details'] = "<div><span><center><b>Difference</b></center></span></div>"
	row['diff'] = "<div><span><center><b>Amount Received in INR</b></center></span></div>"
	data.append(row)
	
	data4 = frappe.db.sql("""select payment_date,sum(net_total*conversion_rate) as 'payment_received_in_bank',sum(total_taxes) as 'gst',sum(net_total*conversion_rate)+sum(total_taxes) as 'gross',tpr.currency,sum(net_total*conversion_rate)*ter.rate_in_inr as 'amount_inr'  
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.currency  = ter.name
		where company='Turacoz Solutions PTE Ltd.' and customer_name not in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and payment_date>='{0}' and payment_status in ('Paid','Partly Paid') and status not in ('Cancelled') group by payment_date order by 1 desc""".format(start_date),as_dict=True)

	payment_received_in_bank=0
	amount_inr=0
	gst=0
	received_amount_bank=0
	exact_amount_bank=0
	diff_amount=0
	for rec in data4:
		row={}
		row['month'] = "<div><span><center><b>%s</b></center></span></div>" %rec.payment_date
		row['raised_amount'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(rec.payment_received_in_bank,2))
		row['received_amount'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(rec.gst,2))
		row['balance'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(rec.gross,2))
		row['diff'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(rec.amount_inr,2))
		payment_received_in_bank = payment_received_in_bank + round(rec.payment_received_in_bank,2)
		amount_inr = amount_inr + round(rec.amount_inr,2)
		gst = gst + round(rec.gst,2)
		received_amount_bank = received_amount_bank + round(rec.gross,2)
		data5 = frappe.db.sql("""select date_of_transaction,if(sum(transaction_amount) is null,0.0,sum(transaction_amount)) from `tabBank Transaction Details` 
				where company='Turacoz Solutions PTE Ltd.' and customer not in ('Viatris Centre of Excellence') and date_of_transaction='{0}'""".format(rec.payment_date))
		if data5:
			row['payment_received'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(float(data5[0][1]),2))
			exact_amount_bank = exact_amount_bank + float(data5[0][1])
			diff1 = round(rec.gross,2) - round(float(data5[0][1]),2)
			row['transaction_details'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(diff1,2)) 
			diff_amount = diff_amount + round(diff1,2)
		data.append(row) 

	row={}
	row['month'] = "<div><span><b>Total:</b></span></div>"
	row['raised_amount'] = "<div><span><center><b>%s</b></center></span></div>" %round(payment_received_in_bank,2)
	row['received_amount'] = "<div><span><center><b>%s</b></center></span></div>" %round(gst,2)
	row['balance'] = "<div><span><center><b>%s</b></center></span></div>" %round(received_amount_bank,2)
	row['diff'] = "<div><span><center><b>%s</b></center></span></div>" %round(amount_inr,2)
	row['payment_received'] = "<div><span><center><b>%s</b></center></span></div>" %round(exact_amount_bank,2)
	row['transaction_details'] = "<div><span><center><b>%s</b></center></span></div>" %round(diff_amount,2)
	data.append(row)

	raised=0
	raised_tot=0
	received_tot=0
	balance_tot=0
	bank_tot=0
	received_amount=0	
	balance=0
	start_date1 = datetime.strptime(start_date, '%Y-%m-%d').date()
	last_date1 = datetime.now().date()
	x=0
	row={}
	row['month'] = "<div><span><b>Company: Turacoz Healthcare Solutions Pvt Ltd</b></span></div>"
	data.append(row)
	while start_date1<last_date1:
		x = x + 1
		month=start_date1.month
		year=start_date1.year
		row={}
		month_year = calendar.month_name[month] + ' , ' + str(year)
		row['month'] = "<div><span><b>%s</b></span></div>" %month_year

		data1 = frappe.db.sql("""select MONTH(invoice_date),MONTHNAME(invoice_date) as 'month',net_total as 'net_amount',tpr.currency,conversion_rate,tpr.net_total * ter.rate_in_inr as 'raised_amount'
			from `tabPayment Request` tpr 
			left join `tabCurrency Exchange Rate` ter on tpr.currency  = ter.name
			where company='Turacoz Healthcare Solutions Pvt Ltd' and customer_name not in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and MONTH(invoice_date)='{0}' and YEAR(invoice_date)='{1}' and payment_status not in ('Cancelled') and status not in ('Cancelled') group by tpr.currency order by 1""".format(month,year),as_dict=True)
		if data1:
			raise_amt=0
			for rec in data1:
				raise_amt = raise_amt + round(float(rec.raised_amount),2)
				
			row['raised_amount'] = round(float(raise_amt),2)
			raised_tot = raised_tot + round(float(raise_amt),2)
			raised = round(float(raise_amt),2)
		else:
			row['raised_amount'] = 0.0
			raised_tot = raised_tot + 0.0
			raised = 0.0	
		
		data2 = frappe.db.sql("""select MONTH(invoice_date),MONTHNAME(invoice_date) as 'month',net_total as 'net_amount',tpr.currency,conversion_rate,net_total * ter.rate_in_inr as 'received_amount' 
			from `tabPayment Request` tpr 
			left join `tabCurrency Exchange Rate` ter on tpr.currency  = ter.name
			where company='Turacoz Healthcare Solutions Pvt Ltd' and customer_name not in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and MONTH(invoice_date)='{0}' and YEAR(invoice_date)='{1}' and payment_status in ('Paid','Partly Paid') and status not in ('Cancelled') group by currency order by 1""".format(month,year),as_dict=True)

		if data2:
			receive_amt=0;
			for rec in data2:
				receive_amt = receive_amt + round(float(rec.received_amount),2)
			row['received_amount'] = round(receive_amt,2)
			received_amount=round(receive_amt,2)
			received_tot = received_tot + round(receive_amt,2)
			balance = raised - received_amount
			row['balance'] = round(balance,2) 		
			balance_tot = balance_tot + balance			
		else:
			row['received_amount'] = 0.0
			balance = raised - 0.0
			row['balance'] = round(balance,2) 		
			balance_tot = balance_tot + balance			

		data3 = frappe.db.sql("""select MONTH(invoice_date),MONTHNAME(payment_date) as 'month',net_total as 'net_total',tpr.currency,conversion_rate,net_total * ter.rate_in_inr as 'payment_received'  
			from `tabPayment Request` tpr 
			left join `tabCurrency Exchange Rate` ter on tpr.currency  = ter.name
			where company='Turacoz Healthcare Solutions Pvt Ltd' and customer_name not in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and MONTH(payment_date)='{0}' and YEAR(payment_date)='{1}' and payment_status in ('Paid','Partly Paid') and status not in ('Cancelled')  order by 1			""".format(month,year),as_dict=True)
		
		if data3:
			payment_amt=0;
			for rec in data3:
				payment_amt = payment_amt + round(float(rec.payment_received),2)
		
			row['payment_received'] = round(payment_amt,2)
			bank_tot = bank_tot + round(payment_amt,2)
		else:
			row['payment_received'] = 0.0
		data.append(row)
		start_date1 = start_date1 + relativedelta(months=+1)

	row={}
	row['month'] = "<div><span><b>Total:</b></span></div>"
	row['raised_amount'] = "<div><span><b>%s</b></span></div>" %round(raised_tot,2)
	row['received_amount'] = "<div><span><b>%s</b></span></div>" %round(received_tot,2)
	row['balance'] = "<div><span><b>%s</b></span></div>" %round(balance_tot,2)
	row['payment_received'] = "<div><span><b>%s</b></span></div>" %round(bank_tot,2)
	data.append(row)
	row={}
	data.append(row)
	row={}
	row['month'] = "<div><span><center><b>Payment Date in Bank</b></center></span></div>"
	row['raised_amount'] = "<div><span><center><b>Basic Amount</b></center></span></div>"
	row['received_amount'] = "<div><span><center><b>GST</b></center></span></div>"
	row['balance'] = "<div><span><center><b>TDS</b></center></span></div>"
	row['payment_received'] = "<div><span><center><b>Gross Amount</b></center></span></div>"
	row['transaction_details'] = "<div><span><center><b>Payment Received in Bank</b></center></span></div>"
	row['diff'] = "<div><span><center><b>Difference</b></center></span></div>"
	data.append(row)
	
	data4 = frappe.db.sql("""select payment_date,sum(net_total)*ter.rate_in_inr as 'payment_received_in_bank',sum(total_taxes) as 'gst',if(tpr.currency='INR',(sum(net_total)*0.10),0.0) as 'tds',tpr.currency,if(tpr.currency='INR',(sum(net_total)*ter.rate_in_inr+sum(total_taxes)-(sum(net_total)*0.10)),(sum(net_total)*ter.rate_in_inr))  as 'amount_received'
		from `tabPayment Request` tpr 
		left join `tabCurrency Exchange Rate` ter on tpr.currency  = ter.name
		where company='Turacoz Healthcare Solutions Pvt Ltd' and customer_name not in ('Viatris Centre of Excellence','Mylan Centre of Excellence') and payment_date>='{0}' and payment_status in ('Paid','Partly Paid') and status not in ('Cancelled') group by payment_date order by 1 desc
""".format(start_date),as_dict=True)

	payment_received_in_bank=0
	amount_inr=0
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
		data5 = frappe.db.sql("""select date_of_transaction,if(sum(transaction_amount) is null,0.0,sum(transaction_amount))  from `tabBank Transaction Details` 
				where company='Turacoz Healthcare Solutions Pvt Ltd' and customer not in ('Viatris Centre of Excellence') and date_of_transaction='{0}'""".format(rec.payment_date))
		if data5:
			row['transaction_details'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(float(data5[0][1]),2))
			exact_amount_bank = exact_amount_bank + float(data5[0][1])
			diff1 = round(rec.amount_received,2) - round(float(data5[0][1]),2)
			row['diff'] = "<div><span><center><b>%s</b></center></span></div>" %str(round(diff1,2)) 
			diff_amount = diff_amount + round(diff1,2)

		data.append(row) 

	row={}
	row['month'] = "<div><span><b>Total:</b></span></div>"
	row['raised_amount'] = "<div><span><center><b>%s</b></center></span></div>" %round(payment_received_in_bank,2)
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
				"label": _("Raised Amount as per Invoice Date"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "received_amount",
				"label": _("Received Amount as per Invoice Date"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "balance",
				"label": _("Balance"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "payment_received",
				"label": _("Payment Received as per Bank"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "transaction_details",
				"label": _("Payment Received in Bank"),
				"fieldtype": "Data",
				"width": "200"
			},
			{
				"fieldname": "diff",
				"label": _("Difference"),
				"fieldtype": "Data",
				"width": "200"
			}

		]
			return cols
