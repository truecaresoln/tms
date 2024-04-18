# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
# import frappe
from frappe import _
import frappe
from collections import Counter
from datetime import datetime
# import datetime
from forex_python.converter import CurrencyRates
import math
from dateutil.relativedelta import relativedelta
# import frappe

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
	
	dt = datetime.strptime(from_date,'%Y-%m-%d')
	to_date = datetime.strptime(to_date,'%Y-%m-%d')
 
 # while dt < to_date:
 # 	month = dt.month
 # 	year = dt.year
 # 	month_name = dt.strftime("%B")
 # 	n = 1
 # 	dt = dt + relativedelta(months=n)
	if detailed_view == 1:
		userid = frappe.session.user
		for_type = ''
		if overview_status == "New Projects This Month":
			for_type = "New Projects This Month"
			if to_date:
				while dt < to_date:
					year = dt.year
					month_name = dt.strftime("%B")
					row = {}
					row["months"] = month_name+' '+str(year)
					
					data2 = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
								tso.currency,count(tp.name) as project_count,ter.rate_in_inr * sum(tso.net_total) as total_inr  
								from `tabSales Order` tso 
								left join `tabProject` tp on tso.project = tp.name
								left join `tabCurrency Exchange Rate` ter on tso.currency  = ter.name
								WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
								and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
								and tp.project_current_status not in ('Cancelled') GROUP by tso.currency""".format(month_name,year), as_dict=True)
					
					final_total_amount_inr2 = float()	
					for rec2 in data2:
						final_total_amount_inr2 += float(rec2.total_inr)
						final_total_amount_inr2 = round(final_total_amount_inr2, 2)
						row["project_count"] = rec2.project_count
					row["new_po"] = final_total_amount_inr2
					
					data3 = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
								tso.currency,ter.rate_in_inr * sum(tso.net_total) as total_inr  
								from `tabSales Order` tso 
								left join `tabProject` tp on tso.project = tp.name
								left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
								WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.company = 'Turacoz Healthcare Solutions Pvt Ltd'
								and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
								and tp.project_current_status not in ('Cancelled') GROUP by tso.currency""".format(month_name,year), as_dict=True)
				
					final_total_amount_inr3 = float()	
					for rec3 in data3:
						final_total_amount_inr3 += float(rec3.total_inr)
						final_total_amount_inr3 = round(final_total_amount_inr3, 2)	
					row["ths"] = final_total_amount_inr3
					
					data4 = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
								tso.currency,ter.rate_in_inr * sum(tso.net_total) as total_inr  
								from `tabSales Order` tso 
								left join `tabProject` tp on tso.project = tp.name
								left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
								WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.company = 'Turacoz B.V.'
								and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
								and tp.project_current_status not in ('Cancelled') GROUP by tso.currency""".format(month_name,year), as_dict=True)
					
					final_total_amount_inr4 = float()	
					for rec4 in data4:
						final_total_amount_inr4 += float(rec4.total_inr)
						final_total_amount_inr4 = round(final_total_amount_inr4, 2)
					
					row["tbv"] = final_total_amount_inr4		
						
					data5 = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
								tso.currency,ter.rate_in_inr * sum(tso.net_total) as total_inr  
								from `tabSales Order` tso 
								left join `tabProject` tp on tso.project = tp.name
								left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
								WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.company = 'Turacoz Solutions PTE Ltd.'
								and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
								and tp.project_current_status not in ('Cancelled') GROUP by tso.currency""".format(month_name,year), as_dict=True)

					final_total_amount_inr5 = float()	
					for rec5 in data5:
						final_total_amount_inr5 += float(rec5.total_inr)
						final_total_amount_inr5 = round(final_total_amount_inr5, 2)	
						
					row["tspl"] = final_total_amount_inr5
					
					data6 = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
								tso.currency,ter.rate_in_inr * sum(tso.net_total) as total_inr  
								from `tabSales Order` tso 
								left join `tabProject` tp on tso.project = tp.name
								left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name	
								WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'jeurkar.namrata@turacoz.com'
								and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
								and tp.project_current_status not in ('Cancelled') GROUP by tso.currency""".format(month_name,year), as_dict=True)
					
					final_total_amount_inr6 = float()	
					for rec6 in data6:
						final_total_amount_inr6 += float(rec6.total_inr)
						final_total_amount_inr6 = round(final_total_amount_inr6, 2)	
						
					row["nj"] = final_total_amount_inr6
					
					data7 = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
								tso.currency,ter.rate_in_inr * sum(tso.net_total) as total_inr  
								from `tabSales Order` tso 
								left join `tabProject` tp on tso.project = tp.name
								left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
								WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'chinthana.bhat@turacoz.com'
								and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
								and tp.project_current_status not in ('Cancelled') GROUP by tso.currency""".format(month_name,year), as_dict=True)

					final_total_amount_inr7 = float()	
					for rec7 in data7:
						final_total_amount_inr7 += float(rec7.total_inr)
						final_total_amount_inr7 = round(final_total_amount_inr7, 2)	
						
					row["cb"] = final_total_amount_inr7
					
					data8 = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
								tso.currency,ter.rate_in_inr * sum(tso.net_total) as total_inr  
								from `tabSales Order` tso 
								left join `tabProject` tp on tso.project = tp.name
								left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
								WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'aarushi.sharma@turacoz.com'
								and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
								and tp.project_current_status not in ('Cancelled') GROUP by tso.currency""".format(month_name,year), as_dict=True)
					
					final_total_amount_inr8 = float()	
					for rec8 in data8:
						final_total_amount_inr8 += float(rec8.total_inr)
						final_total_amount_inr8 = round(final_total_amount_inr8, 2)	
						
					row["as"] = final_total_amount_inr8
					
					dataSistla = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
								tso.currency,ter.rate_in_inr * sum(tso.net_total) as total_inr  
								from `tabSales Order` tso 
								left join `tabProject` tp on tso.project = tp.name
								left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
								WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'sistla.goury@turacoz.com'
								and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
								and tp.project_current_status not in ('Cancelled') GROUP by tso.currency""".format(month_name,year), as_dict=True)
					
					final_total_amount_inrSis = float()	
					for recSistla in dataSistla:
						final_total_amount_inrSis += float(recSistla.total_inr)
						final_total_amount_inrSis = round(final_total_amount_inrSis, 2)	
						
					row["sg"] = final_total_amount_inrSis
					
					data9 = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
								tso.currency,ter.rate_in_inr * sum(tso.net_total) as total_inr  
								from `tabSales Order` tso 
								left join `tabProject` tp on tso.project = tp.name
								left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
								WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'gursimran.alagh@turacoz.com'
								and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
								and tp.project_current_status not in ('Cancelled') GROUP by tso.currency""".format(month_name,year), as_dict=True)
					
					final_total_amount_inr9 = float()	
					for rec9 in data9:
						final_total_amount_inr9 += float(rec9.total_inr)
						final_total_amount_inr9 = round(final_total_amount_inr9, 2)	
					
					row["gs"] = final_total_amount_inr9
					row['comment'] = '<button style=''color:white;background-color:blue;'' type=''button'' onClick= ''comment_fn("{0}","{1}","{2}")''>Comment</button>' .format(userid,month_name,year)
					
					dataCommentsNJ = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'jeurkar.namrata@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'New Projects This Month' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
					for njComm in dataCommentsNJ:
						row["nj_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(njComm.name,njComm.comment)
					
					dataCommentsCB = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'chinthana.bhat@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'New Projects This Month' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
					for cbComm in dataCommentsCB:
						row["cb_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(cbComm.name,cbComm.comment)
					
					dataCommentsAS = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'aarushi.sharma@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'New Projects This Month' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
					for asComm in dataCommentsAS:
						row["as_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(asComm.name,asComm.comment)
					
					dataCommentsGS = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'gursimran.alagh@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'New Projects This Month' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
					for gsComm in dataCommentsGS:
						row["gs_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(gsComm.name,gsComm.comment)
					
					dataCommentsSG = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'sistla.goury@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'New Projects This Month' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
					for sgComm in dataCommentsSG:
						row["sg_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(sgComm.name,sgComm.comment)
					
					
						
					data.append(row)
					n = 1
					dt = dt + relativedelta(months=n)
			return data
		
		elif overview_status == "Expected Payments":
			for_type = "Expected Payments"
	  # if to_date:
	  # 	data1 = frappe.db.sql("""select tpr.name, tpr.due_date,MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) as months,
	  # 		YEAR(tpr.due_date) as year,MONTH(tpr.due_date) as mm from `tabPayment Request` tpr 
	  # 		where (tpr.due_date BETWEEN date('{0}') AND date('{1}')) 
	  # 		and tpr.payment_status not in ('Paid','cancelled') and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') group by year,months order by mm""".format(from_date,to_date), as_dict=True)
	  # else:
	  # 	data1 = frappe.db.sql("""select tpr.name, tpr.due_date,MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) as months,
	  # 		YEAR(tpr.due_date) as year,MONTH(tpr.due_date) as mm from `tabPayment Request` tpr 
	  # 		where tpr.payment_status not in ('Paid','cancelled') and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') group by year,months order by mm""", as_dict=True)
	  #
	
			while dt < to_date:
				year = dt.year
				month_name = dt.strftime("%B")
				row = {}
				row["months"] = month_name+' '+str(year)
				
				data2 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name
					WHERE tpr.payment_status not in ('Cancelled') and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr2 = float()	
				for rec1 in data2:
					final_total_amount_inr2 += float(rec1.total_inr)
					final_total_amount_inr2 = round(final_total_amount_inr2, 2)	
				row["expected_payment"]	= final_total_amount_inr2
	   
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
				row["payment_received"]	= final_total_amount_inr_received
				
				paymentReceivedOtherMonths = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' 
					and MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) != MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m'))
					GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_received_other = float()	
				for recReceivedOther in paymentReceivedOtherMonths:
					final_total_amount_inr_received_other += float(recReceivedOther.total_inr)
					final_total_amount_inr_received_other = round(final_total_amount_inr_received_other, 2)	
				row["payment_received_other_months"]	= final_total_amount_inr_received_other
				
				datatobeReceived = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Paid','Cancelled') and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_ToBeReceived = float()	
				for recToBeReceived in datatobeReceived:
					final_total_amount_inr_ToBeReceived += float(recToBeReceived.total_inr)
					final_total_amount_inr_ToBeReceived = round(final_total_amount_inr_ToBeReceived, 2)	
				row["payment_to_be_received"]	= final_total_amount_inr_ToBeReceived
				
				data3 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name
					WHERE tpr.payment_status not in ('Paid','cancelled') and tpr.due_date is not NULL 
					and company = 'Turacoz Healthcare Solutions Pvt Ltd' and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and 
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr3 = float()	
				for rec3 in data3:
					final_total_amount_inr3 += float(rec3.total_inr)
					final_total_amount_inr3 = round(final_total_amount_inr3, 2)	
				row["ths"] = final_total_amount_inr3
				
				dataTHSExpected = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name
					WHERE tpr.payment_status not in ('cancelled') and tpr.due_date is not NULL 
					and company = 'Turacoz Healthcare Solutions Pvt Ltd' 
					and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and 
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_ths_expected = float()	
				for rec_ths_expected in dataTHSExpected:
					final_total_amount_inr_ths_expected += float(rec_ths_expected.total_inr)
					final_total_amount_inr_ths_expected = round(final_total_amount_inr_ths_expected, 2)	
				row["ths_expected"] = final_total_amount_inr_ths_expected
				
				dataTHSReceived = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL
					and tpr.company = 'Turacoz Healthcare Solutions Pvt Ltd'  and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_ths_received = float()	
				for rec_ths_received in dataTHSReceived:
					final_total_amount_inr_ths_received += float(rec_ths_received.total_inr)
					final_total_amount_inr_ths_received = round(final_total_amount_inr_ths_received, 2)	
				row["ths_received"] = final_total_amount_inr_ths_received
				
				data4 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Paid','cancelled') and tpr.due_date is not NULL and company = 'Turacoz B.V.'
					and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr4 = float()	
				for rec4 in data4:
					final_total_amount_inr4 += float(rec4.total_inr)
					final_total_amount_inr4 = round(final_total_amount_inr4, 2)
				
				row["tbv"] = final_total_amount_inr4
				
				dataTBVExpected = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('cancelled') and tpr.due_date is not NULL and company = 'Turacoz B.V.'
					and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_tbv_expected = float()	
				for rec_tbv_expected in dataTBVExpected:
					final_total_amount_inr_tbv_expected += float(rec_tbv_expected.total_inr)
					final_total_amount_inr_tbv_expected = round(final_total_amount_inr_tbv_expected, 2)
				
				row["tbv_expected"] = final_total_amount_inr_tbv_expected
				
				dataTBVReceived = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL
					and tpr.company = 'Turacoz B.V.'  and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_tbv_received = float()	
				for rec_tbv_received in dataTBVReceived:
					final_total_amount_inr_tbv_received += float(rec_tbv_received.total_inr)
					final_total_amount_inr_tbv_received = round(final_total_amount_inr_tbv_received, 2)
				
				row["tbv_received"] = final_total_amount_inr_tbv_received		
					
				data5 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name
					WHERE tpr.payment_status not in ('Paid','cancelled') and tpr.due_date is not NULL 
					and tpr.company = 'Turacoz Solutions PTE Ltd.' and 
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr5 = float()	
				for rec5 in data5:
					final_total_amount_inr5 += float(rec5.total_inr)
					final_total_amount_inr5 = round(final_total_amount_inr5, 2)	
					
				row["tspl"] = final_total_amount_inr5
				
				dataTSPLExpected = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('cancelled') and tpr.due_date is not NULL 
					and tpr.company = 'Turacoz Solutions PTE Ltd.' and 
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_tspl_expected = float()	
				for rec_tspl_expected in dataTSPLExpected:
					final_total_amount_inr_tspl_expected += float(rec_tspl_expected.total_inr)
					final_total_amount_inr_tspl_expected = round(final_total_amount_inr_tspl_expected, 2)	
					
				row["tspl_expected"] = final_total_amount_inr_tspl_expected
				
				dataTSPLReceived = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL
					and tpr.company = 'Turacoz Solutions PTE Ltd.'  and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_tspl_received = float()	
				for rec_tspl_received in dataTSPLReceived:
					final_total_amount_inr_tspl_received += float(rec_tspl_received.total_inr)
					final_total_amount_inr_tspl_received = round(final_total_amount_inr_tspl_received, 2)	
					
				row["tspl_received"] = final_total_amount_inr_tspl_received
				
				data6 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr 
					left join `tabProject` tp on tpr.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Paid','cancelled') and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'jeurkar.namrata@turacoz.com' and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr6 = float()	
				for rec6 in data6:
					final_total_amount_inr6 += float(rec6.total_inr)
					final_total_amount_inr6 = round(final_total_amount_inr6, 2)	
					
				row["nj"] = final_total_amount_inr6
				
				data7 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr 
					left join `tabProject` tp on tpr.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Paid','cancelled') and tpr.due_date is not NULL  and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'chinthana.bhat@turacoz.com' and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr7 = float()	
				for rec7 in data7:
					final_total_amount_inr7 += float(rec7.total_inr)
					final_total_amount_inr7 = round(final_total_amount_inr7, 2)	
					
				row["cb"] = final_total_amount_inr7
				
				data8 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr 
					left join `tabProject` tp on tpr.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Paid','cancelled') and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'aarushi.sharma@turacoz.com' and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr8 = float()	
				for rec8 in data8:
					final_total_amount_inr8 += float(rec8.total_inr)
					final_total_amount_inr8 = round(final_total_amount_inr8, 2)	
					
				row["as"] = final_total_amount_inr8
				
				dataSis = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr 
					left join `tabProject` tp on tpr.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Paid','cancelled') and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'sistla.goury@turacoz.com' and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inrSis = float()	
				for recSis in dataSis:
					final_total_amount_inrSis += float(recSis.total_inr)
					final_total_amount_inrSis = round(final_total_amount_inrSis, 2)	
					
				row["sg"] = final_total_amount_inrSis
				
				data9 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr 
					left join `tabProject` tp on tpr.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Paid','cancelled') and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'gursimran.alagh@turacoz.com' and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr9 = float()	
				for rec9 in data9:
					final_total_amount_inr9 += float(rec9.total_inr)
					final_total_amount_inr9 = round(final_total_amount_inr9, 2)	
					
				row["gs"] = final_total_amount_inr9
				row['comment'] = '<button style=''color:white;background-color:blue;'' type=''button'' onClick= ''comment_fn("{0}","{1}","{2}")''>Comment</button>' .format(userid,month_name,year)
				
				dataCommentsNJ = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'jeurkar.namrata@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Expected Payments' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for njComm in dataCommentsNJ:
					row["nj_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(njComm.name,njComm.comment)
					
				dataCommentsCB = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'chinthana.bhat@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Expected Payments' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for cbComm in dataCommentsCB:
					row["cb_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(cbComm.name,cbComm.comment)
					
				dataCommentsAS = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'aarushi.sharma@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Expected Payments' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for asComm in dataCommentsAS:
					row["as_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(asComm.name,asComm.comment)
				dataCommentsGS = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'gursimran.alagh@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Expected Payments' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for gsComm in dataCommentsGS:
					row["gs_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(gsComm.name,gsComm.comment)
					
				dataCommentsSG = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'sistla.goury@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Expected Payments' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for sgComm in dataCommentsSG:
					row["sg_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(sgComm.name,sgComm.comment)
					
						
				n = 1
				dt = dt + relativedelta(months=n)
				data.append(row)
			
		elif overview_status == "Invoice to be Raised":
			for_type="Invoice to be Raised"	
	  # if to_date: 
	  # 	data1 = frappe.db.sql("""select MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) as months,
	  # 		YEAR(tps.due_date) as year from `tabSales Invoice` tsi 
	  # 		left join `tabPayment Schedule` tps on tsi.name = tps.parent 
	  # 		where tsi.status not in ('Paid','Cancelled') and tps.invoice_status='Unraised' 
	  # 		and (tps.due_date BETWEEN date('{0}') AND date('{1}'))
	  # 		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') group by year,months""".format(from_date,to_date), as_dict=True)
	  # else:	
	  # 	data1 = frappe.db.sql("""select MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) as months,
	  # 		YEAR(tps.due_date) as year from `tabSales Invoice` tsi 
	  # 		left join `tabPayment Schedule` tps on tsi.name = tps.parent 
	  # 		where tsi.status not in ('Paid','Cancelled') and tps.invoice_status='Unraised' 
	  # 		and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') group by year,months""", as_dict=True)
			
			while dt < to_date:
				year = dt.year
				month_name = dt.strftime("%B")
				row = {}
				row["months"] = month_name+' '+str(year)
				
				dataUraised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
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
				row["invoice_unraised"]	= final_total_amount_inr_unraised
				
				dataRaised = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
						tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
						from `tabPayment Request` tpr
						left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name 
						WHERE tpr.payment_status not in ('Cancelled')
						and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
						and MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_raised = float()	
				for recRaised in dataRaised:
					final_total_amount_inr_raised += float(recRaised.total_inr)
					final_total_amount_inr_raised = round(final_total_amount_inr_raised, 2)	
				row["invoice_raised"]	= final_total_amount_inr_raised
				
				data2 = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr2 = float()	
				for rec1 in data2:
					final_total_amount_inr2 += float(rec1.total_inr)
					final_total_amount_inr2 = round(final_total_amount_inr2, 2)	
				row["invoice_to_be_raised"]	= final_total_amount_inr2
				
				data3 = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tsi.company = 'Turacoz Healthcare Solutions Pvt Ltd'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr3 = float()	
				for rec3 in data3:
					final_total_amount_inr3 += float(rec3.total_inr)
					final_total_amount_inr3 = round(final_total_amount_inr3, 2)	
				row["ths"] = final_total_amount_inr3
				
				dataTHSUnraised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tsi.company = 'Turacoz Healthcare Solutions Pvt Ltd'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_ths_unraised = float()	
				for rec_ths_unraised in dataTHSUnraised:
					final_total_amount_inr_ths_unraised += float(rec_ths_unraised.total_inr)
					final_total_amount_inr_ths_unraised = round(final_total_amount_inr_ths_unraised, 2)	
				row["ths_unraised"] = final_total_amount_inr_ths_unraised
				
				dataTHSraised = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
						tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
						from `tabPayment Request` tpr
						left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name 
						WHERE tpr.payment_status not in ('Cancelled')
						and tpr.company = 'Turacoz Healthcare Solutions Pvt Ltd'
						and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
						and MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				to_currency_ths_raised = "INR"
				final_total_amount_inr_ths_raised = float()	
				for rec_ths_raised in dataTHSraised:
					final_total_amount_inr_ths_raised += float(rec_ths_raised.total_inr)
					final_total_amount_inr_ths_raised = round(final_total_amount_inr_ths_raised, 2)	
				row["ths_raised"] = final_total_amount_inr_ths_raised
				
				data4 = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tsi.company = 'Turacoz B.V.'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr4 = float()	
				for rec4 in data4:
					final_total_amount_inr4 += float(rec4.total_inr)
					final_total_amount_inr4 = round(final_total_amount_inr4, 2)
				
				row["tbv"] = final_total_amount_inr4
				
				dataTBVUnraised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tsi.company = 'Turacoz B.V.'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_tbv_unraised = float()	
				for rec_tbv_unraised in dataTBVUnraised:
					final_total_amount_inr_tbv_unraised += float(rec_tbv_unraised.total_inr)
					final_total_amount_inr_tbv_unraised = round(final_total_amount_inr_tbv_unraised, 2)
				
				row["tbv_unraised"] = final_total_amount_inr_tbv_unraised
				
				dataTBVraised = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
						tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
						from `tabPayment Request` tpr
						left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name 
						WHERE tpr.payment_status not in ('Cancelled')
						and tpr.company = 'Turacoz B.V.'
						and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
						and MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				to_currency_tbv_raise = "INR"
				final_total_amount_inr_tbv_raised = float()	
				for rec_tbv_raised in dataTBVraised:
					final_total_amount_inr_tbv_raised += float(rec_tbv_raised.total_inr)
					final_total_amount_inr_tbv_raised = round(final_total_amount_inr_tbv_raised, 2)
				
				row["tbv_raised"] = final_total_amount_inr_tbv_raised			
					
				data5 = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tsi.company = 'Turacoz Solutions PTE Ltd.'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr5 = float()	
				for rec5 in data5:
					final_total_amount_inr5 += float(rec5.total_inr)
					final_total_amount_inr5 = round(final_total_amount_inr5, 2)	
					
				row["tspl"] = final_total_amount_inr5
				
				dataTSPLUnraised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tsi.company = 'Turacoz Solutions PTE Ltd.'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_tspl_unraised = float()	
				for rec_tspl_unraised in dataTSPLUnraised:
					final_total_amount_inr_tspl_unraised += float(rec_tspl_unraised.total_inr)
					final_total_amount_inr_tspl_unraised = round(final_total_amount_inr_tspl_unraised, 2)	
					
				row["tspl_unraised"] = final_total_amount_inr_tspl_unraised
				
				dataTSPlRaised = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
						tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
						from `tabPayment Request` tpr
						left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name 
						WHERE tpr.payment_status not in ('Cancelled')
						and tpr.company = 'Turacoz Solutions PTE Ltd.'
						and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
						and MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_tspl_raised = float()	
				for rec_tspl_raised in dataTSPlRaised:
					final_total_amount_inr_tspl_raised += float(rec_tspl_raised.total_inr)
					final_total_amount_inr_tspl_raised = round(final_total_amount_inr_tspl_raised, 2)	
					
				row["tspl_raised"] = final_total_amount_inr_tspl_raised
				
				dataNJUraised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tp.project_manager = 'jeurkar.namrata@turacoz.com'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)

				final_total_amount_inr_unraised = float()	
				for recUnraised in dataNJUraised:
					final_total_amount_inr_unraised += float(recUnraised.total_inr)
					final_total_amount_inr_unraised = round(final_total_amount_inr_unraised, 2)	
				row["nj"]	= "Total Invoices: ₹{0}".format(final_total_amount_inr_unraised)
				
				row1={}
				row2={}
				
				dataNJRaised = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
						tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
						from `tabPayment Request` tpr
						left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name 
						left join `tabProject` tp on tpr.project = tp.name
						WHERE tpr.payment_status not in ('Cancelled')
						and tp.project_manager = 'jeurkar.namrata@turacoz.com'
						and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
						and MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_raised = float()	
				for recRaised in dataNJRaised:
					final_total_amount_inr_raised += float(recRaised.total_inr)
					final_total_amount_inr_raised = round(final_total_amount_inr_raised, 2)	
				row1["nj"]	= "Raised Invoices: ₹{0}".format(final_total_amount_inr_raised)

				data6 = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tp.project_manager = 'jeurkar.namrata@turacoz.com'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr6 = float()	
				for rec6 in data6:
					final_total_amount_inr6 += float(rec6.total_inr)
					final_total_amount_inr6 = round(final_total_amount_inr6, 2)	
					
				row2["nj"] = "Unraised Invoices: ₹{0}".format(final_total_amount_inr6)
				
				dataCBUraised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tp.project_manager = 'chinthana.bhat@turacoz.com'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)

				final_total_amount_inr_unraised = float()	
				for recUnraised in dataCBUraised:
					final_total_amount_inr_unraised += float(recUnraised.total_inr)
					final_total_amount_inr_unraised = round(final_total_amount_inr_unraised, 2)	
				row["cb"]	= "Total Invoices: ₹{0}".format(final_total_amount_inr_unraised)
				
				dataCBRaised = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
						tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
						from `tabPayment Request` tpr
						left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name 
						left join `tabProject` tp on tpr.project = tp.name
						WHERE tpr.payment_status not in ('Cancelled')
						and tp.project_manager = 'chinthana.bhat@turacoz.com'
						and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
						and MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_raised = float()	
				for recRaised in dataCBRaised:
					final_total_amount_inr_raised += float(recRaised.total_inr)
					final_total_amount_inr_raised = round(final_total_amount_inr_raised, 2)	
				row1["cb"]	= "Raised Invoices: ₹{0}".format(final_total_amount_inr_raised)

				data7 = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tp.project_manager = 'chinthana.bhat@turacoz.com'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr7 = float()	
				for rec7 in data7:
					final_total_amount_inr7 += float(rec7.total_inr)
					final_total_amount_inr7 = round(final_total_amount_inr7, 2)	
					
				row2["cb"] = "Unraised Invoices: ₹{0}".format(final_total_amount_inr7)
				
				dataASUraised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tp.project_manager = 'aarushi.sharma@turacoz.com'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)

				final_total_amount_inr_unraised = float()	
				for recUnraised in dataASUraised:
					final_total_amount_inr_unraised += float(recUnraised.total_inr)
					final_total_amount_inr_unraised = round(final_total_amount_inr_unraised, 2)	
				row["as"]	= "Total Invoices: ₹{0}".format(final_total_amount_inr_unraised)
				
		
				dataASRaised = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
						tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
						from `tabPayment Request` tpr
						left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name 
						left join `tabProject` tp on tpr.project = tp.name
						WHERE tpr.payment_status not in ('Cancelled')
						and tp.project_manager = 'aarushi.sharma@turacoz.com'
						and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
						and MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_raised = float()	
				for recRaised in dataASRaised:
					final_total_amount_inr_raised += float(recRaised.total_inr)
					final_total_amount_inr_raised = round(final_total_amount_inr_raised, 2)	
				row1["as"]	= "Raised Invoices: ₹{0}".format(final_total_amount_inr_raised)

				data8 = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tp.project_manager = 'aarushi.sharma@turacoz.com'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr8 = float()	
				for rec8 in data8:
					final_total_amount_inr8 += float(rec8.total_inr)
					final_total_amount_inr8 = round(final_total_amount_inr8, 2)	
					
				row2["as"] = "Unraised Invoices: ₹{0}".format(final_total_amount_inr8)
				
				dataSGUraised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tp.project_manager = 'sistla.goury@turacoz.com'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)

				final_total_amount_inr_unraised_sg = float()	
				for recUnraisedSG in dataSGUraised:
					final_total_amount_inr_unraised_sg += float(recUnraisedSG.total_inr)
					final_total_amount_inr_unraised_sg = round(final_total_amount_inr_unraised_sg, 2)	
				row["sg"]	= "Total Invoices: ₹{0}".format(final_total_amount_inr_unraised_sg)
				
		
				dataSGRaised = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
						tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
						from `tabPayment Request` tpr
						left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name 
						left join `tabProject` tp on tpr.project = tp.name
						WHERE tpr.payment_status not in ('Cancelled')
						and tp.project_manager = 'sistla.goury@turacoz.com'
						and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
						and MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_raised_sg = float()	
				for recRaisedSG in dataSGRaised:
					final_total_amount_inr_raised_sg += float(recRaisedSG.total_inr)
					final_total_amount_inr_raised_sg = round(final_total_amount_inr_raised_sg, 2)	
				row1["sg"]	= "Raised Invoices: ₹{0}".format(final_total_amount_inr_raised_sg)

				dataSG = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tp.project_manager = 'sistla.goury@turacoz.com'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_sg = float()	
				for recSG in dataSG:
					final_total_amount_inr_sg += float(recSG.total_inr)
					final_total_amount_inr_sg = round(final_total_amount_inr_sg, 2)	
					
				row2["sg"] = "Unraised Invoices: ₹{0}".format(final_total_amount_inr_sg)
				
				dataGSUraised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tp.project_manager = 'gursimran.alagh@turacoz.com'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)

				final_total_amount_inr_unraised = float()	
				for recUnraised in dataGSUraised:
					final_total_amount_inr_unraised += float(recUnraised.total_inr)
					final_total_amount_inr_unraised = round(final_total_amount_inr_unraised, 2)	
				row["gs"]	= "Total Invoices: ₹{0}".format(final_total_amount_inr_unraised)
				
		
				dataGSRaised = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
						tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
						from `tabPayment Request` tpr
						left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name 
						left join `tabProject` tp on tpr.project = tp.name
						WHERE tpr.payment_status not in ('Cancelled')
						and tp.project_manager = 'gursimran.alagh@turacoz.com'
						and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
						and MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_raised = float()	
				for recRaised in dataGSRaised:
					final_total_amount_inr_raised += float(recRaised.total_inr)
					final_total_amount_inr_raised = round(final_total_amount_inr_raised, 2)	
				row1["gs"]	= "Raised Invoices: ₹{0}".format(final_total_amount_inr_raised)

				data9 = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tp.project_manager = 'gursimran.alagh@turacoz.com'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr9 = float()	
				for rec9 in data9:
					final_total_amount_inr9 += float(rec9.total_inr)
					final_total_amount_inr9 = round(final_total_amount_inr9, 2)	
				
				row2["gs"] = "Unraised Invoices: ₹{0}".format(final_total_amount_inr9)
				row['comment'] = '<button style=''color:white;background-color:blue;'' type=''button'' onClick= ''comment_fn("{0}","{1}","{2}")''>Comment</button>' .format(userid,month_name,year)
				
				dataCommentsNJ = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'jeurkar.namrata@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Invoice to be Raised' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for njComm in dataCommentsNJ:
					row["nj_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(njComm.name,njComm.comment)
					
				dataCommentsCB = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'chinthana.bhat@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Invoice to be Raised' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for cbComm in dataCommentsCB:
					row["cb_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(cbComm.name,cbComm.comment)
					
				dataCommentsAS = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'aarushi.sharma@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Invoice to be Raised' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for asComm in dataCommentsAS:
					row["as_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(asComm.name,asComm.comment)
				
				dataCommentsSG = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'sistla.goury@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Invoice to be Raised' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for sgComm in dataCommentsSG:
					row["sg_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(sgComm.name,sgComm.comment)
				
				
				dataCommentsGS = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'gursimran.alagh@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Invoice to be Raised' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for gsComm in dataCommentsGS:
					row["gs_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(gsComm.name,gsComm.comment)
				
				n = 1
				dt = dt + relativedelta(months=n)
				data.append(row)
				data.append(row1)
				data.append(row2)
				
		elif overview_status=="Received Payment":
			for_type = "Received Payment"
	  # if to_date: 
	  # 	data1 = frappe.db.sql("""select MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) as months,
	  # 		YEAR(tpr.payment_date) as year from `tabPayment Request` tpr 
	  # 		where tpr.payment_status in ('Paid') and (tpr.payment_date BETWEEN date('{0}') AND date('{1}'))
	  # 		and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') group by year,months""".format(from_date,to_date), as_dict=True)
	  # else:	
	  # 	data1 = frappe.db.sql("""select MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) as months,
	  # 		YEAR(tpr.payment_date) as year from `tabPayment Request` tpr 
	  # 		where tpr.payment_status in ('Paid')
	  # 		and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') group by year,months""", as_dict=True)
	  # months = ''
	  # year = ''
			while dt < to_date:
				year = dt.year
				month_name = dt.strftime("%B")
				row = {}
				row["months"] = month_name+' '+str(year)
				
				data2 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.payment_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr2 = float()	
				for rec1 in data2:
					final_total_amount_inr2 += float(rec1.total_inr)
					final_total_amount_inr2 = round(final_total_amount_inr2, 2)	
				row["payment_received"]	= final_total_amount_inr2
				
				data3 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.payment_date is not NULL 
					and company = 'Turacoz Healthcare Solutions Pvt Ltd' and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and 
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr3 = float()	
				for rec3 in data3:
					final_total_amount_inr3 += float(rec3.total_inr)
					final_total_amount_inr3 = round(final_total_amount_inr3, 2)	
				row["ths"] = final_total_amount_inr3
				
				data4 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.payment_date is not NULL and company = 'Turacoz B.V.'
					and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				to_currency4 = "INR"
				final_total_amount_inr4 = float()	
				for rec4 in data4:
					final_total_amount_inr4 += float(rec4.total_inr)
					final_total_amount_inr4 = round(final_total_amount_inr4, 2)
				
				row["tbv"] = final_total_amount_inr4		
					
				data5 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.payment_date is not NULL 
					and tpr.company = 'Turacoz Solutions PTE Ltd.' and 
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				to_currency5 = "INR"
				final_total_amount_inr5 = float()	
				for rec5 in data5:
					final_total_amount_inr5 += float(rec5.total_inr)
					final_total_amount_inr5 = round(final_total_amount_inr5, 2)	
					
				row["tspl"] = final_total_amount_inr5
				
				data6 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr 
					left join `tabProject` tp on tpr.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.payment_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'jeurkar.namrata@turacoz.com' and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				to_currency6 = "INR"
				final_total_amount_inr6 = float()	
				for rec6 in data6:
					final_total_amount_inr6 += float(rec6.total_inr)
					final_total_amount_inr6 = round(final_total_amount_inr6, 2)	
					
				row["nj"] = final_total_amount_inr6
				
				data7 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr 
					left join `tabProject` tp on tpr.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.payment_date is not NULL  and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'chinthana.bhat@turacoz.com' and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				to_currency7 = "INR"
				final_total_amount_inr7 = float()	
				for rec7 in data7:
					final_total_amount_inr7 += float(rec7.total_inr)
					final_total_amount_inr7 = round(final_total_amount_inr7, 2)	
					
				row["cb"] = final_total_amount_inr7
				
				data8 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr 
					left join `tabProject` tp on tpr.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.payment_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'aarushi.sharma@turacoz.com' and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr8 = float()	
				for rec8 in data8:
					final_total_amount_inr8 += float(rec8.total_inr)
					final_total_amount_inr8 = round(final_total_amount_inr8, 2)	
					
				row["as"] = final_total_amount_inr8
				
				dataSG = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr 
					left join `tabProject` tp on tpr.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.payment_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'sistla.goury@turacoz.com' and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_sg = float()	
				for recSG in dataSG:
					final_total_amount_inr_sg += float(recSG.total_inr)
					final_total_amount_inr_sg = round(final_total_amount_inr_sg, 2)	
					
				row["sg"] = final_total_amount_inr_sg
				
				data9 = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr 
					left join `tabProject` tp on tpr.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency  = ter.name 
					WHERE tpr.payment_status in ('Paid') and tpr.payment_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tp.project_manager = 'gursimran.alagh@turacoz.com' and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr9 = float()	
				for rec9 in data9:
					final_total_amount_inr9 += float(rec9.total_inr)
					final_total_amount_inr9 = round(final_total_amount_inr9, 2)	
					
				row["gs"] = final_total_amount_inr9
				row['comment'] = '<button style=''color:white;background-color:blue;'' type=''button'' onClick= ''comment_fn("{0}","{1}","{2}")''>Comment</button>' .format(userid,month_name,year)
				
				dataCommentsNJ = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'jeurkar.namrata@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Received Payment' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for njComm in dataCommentsNJ:
					row["nj_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(njComm.name,njComm.comment)
					
				dataCommentsCB = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'chinthana.bhat@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Received Payment' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for cbComm in dataCommentsCB:
					row["cb_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(cbComm.name,cbComm.comment)
					
				dataCommentsAS = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'aarushi.sharma@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Received Payment' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for asComm in dataCommentsAS:
					row["as_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(asComm.name,asComm.comment)
				
				dataCommentsSG = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'sistla.goury@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Received Payment' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for sgComm in dataCommentsSG:
					row["sg_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(sgComm.name,sgComm.comment)
				
				
				dataCommentsGS = frappe.db.sql("""select tfoc.name,tfoc.comment from `tabFinancial Overview Comments` tfoc WHERE  tfoc.employee = 'gursimran.alagh@turacoz.com'
								and tfoc.month = '{0}' and tfoc.year='{1}' and tfoc.for_type = 'Received Payment' order by tfoc.name DESC limit 1""".format(month_name,year), as_dict=True)
					
				for gsComm in dataCommentsGS:
					row["gs_comment"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_comment_fn("{0}")''>''{1}''</a>' .format(gsComm.name,gsComm.comment)
				
				n = 1
				dt = dt + relativedelta(months=n)
				data.append(row)	
		
		return data
	else:
		if excluding_viatris == 1:
			type = ''
			balance_unraised = float()
			received_balance = float()
			while dt < to_date:
				year = dt.year
				month_name = dt.strftime("%B")
				print(month_name)
				row = {}
				row["months"] = month_name+' '+str(year)
									
				dataNewPo = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
					tso.currency,count(tp.name) as project_count,ter.rate_in_inr * sum(tso.net_total) as total_inr  from `tabSales Order` tso 
					left join `tabProject` tp on tso.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tso.currency  = ter.name 
					WHERE tp.customer  not in ('Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
					and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
					and tp.project_current_status not in ('Cancelled') GROUP by tso.currency""".format(month_name,year), as_dict=True)
						
				type = "New_Po"
				final_total_amount_inrNewPo = float()	
				for recNewPo in dataNewPo:					
					final_total_amount_inrNewPo += float(recNewPo.total_inr)
					final_total_amount_inrNewPo = round(final_total_amount_inrNewPo, 2)
				row["new_po"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inrNewPo,excluding_viatris)
				
				dataUraised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
					ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
					from `tabSales Invoice` tsi 
					left join `tabPayment Schedule` tps on tsi.name = tps.parent
					left join `tabProject` tp on tsi.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tsi.currency  = ter.name 
					WHERE tsi.status not in ('Paid','Cancelled')
					and tsi.customer not in ('Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
					
				type = "Monthly_Invoice_Due" 
				final_total_amount_inr_unraised = float()	
				for recUnraised in dataUraised:
					final_total_amount_inr_unraised += float(recUnraised.total_inr)
					final_total_amount_inr_unraised = round(final_total_amount_inr_unraised, 2)	
				row["invoice_unraised"]	= '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inr_unraised,excluding_viatris)
					
				dataRaised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,tsi.currency,
					ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
					from `tabSales Invoice` tsi 
					left join `tabPayment Schedule` tps on tsi.name = tps.parent
					left join `tabProject` tp on tsi.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
					WHERE tsi.status not in ('Paid','Cancelled') and tps.invoice_status='Raised'
					and tsi.customer not in ('Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
					
				type = "Invoice_Raised_Till_Date"
				final_total_amount_inr_raised = float()	
				for recRaised in dataRaised:
					final_total_amount_inr_raised += float(recRaised.total_inr)
					final_total_amount_inr_raised = round(final_total_amount_inr_raised, 2)	
				row["invoice_raised"]	= '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inr_raised,excluding_viatris)
				
				cumuRaised = frappe.db.sql("""select tpr.invoice_currency as currency,
						sum(tpr.grand_total) as total_amount, ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
						from `tabPayment Request` tpr
						left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name where 
						MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' and YEAR(tpr.invoice_date) = '{1}'
						and tpr.status not in ('Cancelled') and tpr.payment_status not in ('Cancelled') 
						and tpr.party not in ('Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
						GROUP by tpr.currency""".format(month_name,year), as_dict=True)

				type = "Cumu_nvoice_Raised_Till_Date"
				final_total_amount_inr_raised_cumu = float()
				for cumuRaised in cumuRaised:
					final_total_amount_inr_raised_cumu += float(cumuRaised.total_inr)
					final_total_amount_inr_raised_cumu = round(final_total_amount_inr_raised_cumu, 2)
				row["cumulative_invoice_raised"] = final_total_amount_inr_raised_cumu
				
				dataInvoiceTobeRaised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
					tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
					from `tabSales Invoice` tsi 
					left join `tabPayment Schedule` tps on tsi.name = tps.parent
					left join `tabProject` tp on tsi.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name 
					WHERE tsi.status not in ('Paid','Cancelled')
					and tsi.customer not in ('Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
					MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
				type = "Monthly_Balance_Invoice"
				final_total_amount_inr_invoice_to_be_raised = float()	
				for recInvoiceToBeRaised in dataInvoiceTobeRaised:
					final_total_amount_inr_invoice_to_be_raised += float(recInvoiceToBeRaised.total_inr)
					final_total_amount_inr_invoice_to_be_raised = round(final_total_amount_inr_invoice_to_be_raised, 2)	
				row["invoice_to_be_raised"]	= '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inr_invoice_to_be_raised,excluding_viatris)
				balance_unraised += final_total_amount_inr_invoice_to_be_raised
				row["balance_unraised"] = balance_unraised
					
				dataExpected = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr 
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Cancelled') and tpr.due_date is not NULL and
					tpr.party not in ('Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				type = "Monthly_Payment_Due"
				final_total_amount_inr_expected = float()	
				for recExpected in dataExpected:
					final_total_amount_inr_expected += float(recExpected.total_inr)
					final_total_amount_inr_expected = round(final_total_amount_inr_expected, 2)	
				row["expected_payment"]	= '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inr_expected,excluding_viatris)
		   
				dataReceived = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr 
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name 
					WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL and
					tpr.party not in ('Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				type = "Payment_Received_Till_Date"
				final_total_amount_inr_received = float()	
				for recReceived in dataReceived:
					final_total_amount_inr_received += float(recReceived.total_inr)
					final_total_amount_inr_received = round(final_total_amount_inr_received, 2)	
				row["payment_received"]	= '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inr_received,excluding_viatris)
							
				datatobeReceived = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency, ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name 
					WHERE tpr.payment_status not in ('Paid','Cancelled') and tpr.due_date is not NULL and
					tpr.party not in ('Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				type = "Monthly_Balance_Due"
				final_total_amount_inr_ToBeReceived = float()	
				for recToBeReceived in datatobeReceived:
					final_total_amount_inr_ToBeReceived += float(recToBeReceived.total_inr)
					final_total_amount_inr_ToBeReceived = round(final_total_amount_inr_ToBeReceived, 2)
					
	    # row["payment_to_be_received"] = final_total_amount_inr_ToBeReceived
				row["payment_to_be_received"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inr_ToBeReceived,excluding_viatris)
				received_balance += final_total_amount_inr_ToBeReceived
				row["received_balance"] = received_balance
				
				cumulativeReceived = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
					tpr.invoice_currency, ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
			    	from `tabPayment Request` tpr
			    	left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
			    	WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL and
			    	tpr.party not in ('Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
			    	MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				type = "Cumulative_Payment_Received_Till_Date"
				final_total_amount_inr_received_cumu = float()
				for cumuReceived in cumulativeReceived:
					final_total_amount_inr_received_cumu += float(cumuReceived.total_inr)
					final_total_amount_inr_received_cumu = round(final_total_amount_inr_received_cumu, 2)	
				row["cumulative_received_balance"]	= final_total_amount_inr_received_cumu
				
				
				n = 1
				dt = dt + relativedelta(months=n)
				data.append(row)
			return data	
		else:
			type = ''
			balance_unraised = float()
			received_balance = float()
			while dt < to_date:
				year = dt.year
				month_name = dt.strftime("%B")
				row = {}
				row["months"] = month_name+' '+str(year)
										
				dataNewPo = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
					tso.currency,count(tp.name) as project_count,
					ter.rate_in_inr * sum(tso.net_total) as total_inr from `tabSales Order` tso 
					left join `tabProject` tp on tso.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
					WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
					and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
					and tp.project_current_status not in ('Cancelled') GROUP by tso.currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inrNewPo1 = ''
				type = "New_Po"
				final_total_amount_inrNewPo = float()	
				for recNewPo in dataNewPo:
					final_total_amount_inrNewPo += float(recNewPo.total_inr)
					final_total_amount_inrNewPo = round(final_total_amount_inrNewPo, 2)
				final_total_amount_inrNewPo1 = '₹'+str(final_total_amount_inrNewPo)
				row["new_po"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inrNewPo,excluding_viatris)
					
				dataUraised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
					tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
					from `tabSales Invoice` tsi 
					left join `tabPayment Schedule` tps on tsi.name = tps.parent
					left join `tabProject` tp on tsi.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
					WHERE tsi.status not in ('Paid','Cancelled')
					and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
					
				final_total_amount_inr_unraised1 = ''
				type = "Monthly_Invoice_Due" 
				final_total_amount_inr_unraised = float()	
				for recUnraised in dataUraised:
					final_total_amount_inr_unraised += float(recUnraised.total_inr)
					final_total_amount_inr_unraised = round(final_total_amount_inr_unraised, 2)	
				final_total_amount_inr_unraised1 = '₹'+str(final_total_amount_inr_unraised)
				row["invoice_unraised"]	= '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inr_unraised1,excluding_viatris)
					
				dataRaised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
					tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
					from `tabSales Invoice` tsi 
					left join `tabPayment Schedule` tps on tsi.name = tps.parent
					left join `tabProject` tp on tsi.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
					WHERE tsi.status not in ('Paid','Cancelled') and tps.invoice_status='Raised'
					and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
					
				final_total_amount_inr_raised1 = ''
				type = "Invoice_Raised_Till_Date"
				final_total_amount_inr_raised = float()	
				for recRaised in dataRaised:
					final_total_amount_inr_raised += float(recRaised.total_inr)
					final_total_amount_inr_raised = round(final_total_amount_inr_raised, 2)	
				final_total_amount_inr_raised1 = '₹'+str(final_total_amount_inr_raised)
				row["invoice_raised"]	= '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inr_raised1,excluding_viatris)
				
				cumuRaised = frappe.db.sql("""select tpr.invoice_currency as currency,
						sum(tpr.grand_total) as total_amount,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
						from `tabPayment Request` tpr
						left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name where 
						MONTHNAME(STR_TO_DATE(MONTH(tpr.invoice_date),'%m')) = '{0}' 
						and YEAR(tpr.invoice_date) = '{1}'
						and tpr.status not in ('Cancelled') 
						and tpr.payment_status not in ('Cancelled') 
						and tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
						GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
					
				type = "Cumu_nvoice_Raised_Till_Date"
				final_total_amount_inr_raised_cumu = float()	
				for cumuRaised in cumuRaised:
					final_total_amount_inr_raised_cumu += float(cumuRaised.total_inr)
					final_total_amount_inr_raised_cumu = round(final_total_amount_inr_raised_cumu, 2)	
				row["cumulative_invoice_raised"] = final_total_amount_inr_raised_cumu
					
				dataInvoiceTobeRaised = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
					tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
					from `tabSales Invoice` tsi 
					left join `tabPayment Schedule` tps on tsi.name = tps.parent
					left join `tabProject` tp on tsi.project = tp.name
					left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
					WHERE tsi.status not in ('Paid','Cancelled')
					and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
					MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
					
				final_total_amount_inr_invoice_to_be_raised1 = ''
				type = "Monthly_Balance_Invoice"
				final_total_amount_inr_invoice_to_be_raised = float()	
				for recInvoiceToBeRaised in dataInvoiceTobeRaised:
					final_total_amount_inr_invoice_to_be_raised += float(recInvoiceToBeRaised.total_inr)
					final_total_amount_inr_invoice_to_be_raised = round(final_total_amount_inr_invoice_to_be_raised, 2)	
				final_total_amount_inr_invoice_to_be_raised1 = '₹'+str(final_total_amount_inr_invoice_to_be_raised)
				row["invoice_to_be_raised"]	= '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inr_invoice_to_be_raised1,excluding_viatris)
				balance_unraised += final_total_amount_inr_invoice_to_be_raised
				row["balance_unraised"] = balance_unraised
					
				dataExpected = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name 
					WHERE tpr.payment_status not in ('Cancelled') and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_expected1 = ''
				type = "Monthly_Payment_Due"
				final_total_amount_inr_expected = float()	
				for recExpected in dataExpected:
					final_total_amount_inr_expected += float(recExpected.total_inr)
					final_total_amount_inr_expected = round(final_total_amount_inr_expected, 2)	
				final_total_amount_inr_expected1 = '₹'+str(final_total_amount_inr_expected)
				row["expected_payment"]	= '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inr_expected1,excluding_viatris)
		   
				dataReceived = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name   
					WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_received1 = ''
				type = "Payment_Received_Till_Date"
				final_total_amount_inr_received = float()	
				for recReceived in dataReceived:
					final_total_amount_inr_received += float(recReceived.total_inr)
					final_total_amount_inr_received = round(final_total_amount_inr_received, 2)	
				final_total_amount_inr_received1 = '₹'+str(final_total_amount_inr_received)
				row["payment_received"]	= '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inr_received1,excluding_viatris)
							
				datatobeReceived = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name 
					WHERE tpr.payment_status not in ('Paid','Cancelled') and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				type = "Monthly_Balance_Due"
				final_total_amount_inr_ToBeReceived1 = ''
				final_total_amount_inr_ToBeReceived = float()	
				for recToBeReceived in datatobeReceived:
					final_total_amount_inr_ToBeReceived += float(recToBeReceived.total_inr)
					final_total_amount_inr_ToBeReceived = round(final_total_amount_inr_ToBeReceived, 2)
				final_total_amount_inr_ToBeReceived1 = '₹'+str(final_total_amount_inr_ToBeReceived)
	    # row["payment_to_be_received"] = final_total_amount_inr_ToBeReceived
				row["payment_to_be_received"] = '<a style=''color:blue;'' type=''button'' onClick= ''get_data("{0}","{1}","{2}","{4}")''>''{3}''</a>' .format(month_name,year,type,final_total_amount_inr_ToBeReceived1,excluding_viatris)
				received_balance += final_total_amount_inr_ToBeReceived
				row["received_balance"] = received_balance
				
				cumulativeReceived = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
					tpr.invoice_currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr  
					from `tabPayment Request` tpr
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status in ('Paid') and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.payment_date),'%m')) = '{0}' and YEAR(tpr.payment_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
				final_total_amount_inr_received_cumu = ''
				type = "Cumulative_Payment_Received_Till_Date"
				final_total_amount_inr_received_cumu = float()	
				for cumuReceived in cumulativeReceived:
					final_total_amount_inr_received_cumu += float(cumuReceived.total_inr)
					final_total_amount_inr_received_cumu = round(final_total_amount_inr_received_cumu, 2)	
				
				row["cumulative_received_balance"]	= final_total_amount_inr_received_cumu
				
				n = 1
				dt = dt + relativedelta(months=n)
				data.append(row)			
		
			return data
	
def get_columns(filters):
	detailed_view = filters.get("detailed_view")
	overview_status = filters.get("overview_status")
	cols = []
	if detailed_view == 1:
		if overview_status == "New Projects This Month":
			cols = [
					{
						"fieldname": "months",
						"label": _("Months"),
						"fieldtype": "Data",
						"width": "200"
					},
					{
						"fieldname": "project_count",
						"label": _("Total Projects"),
						"fieldtype": "Data",
						"width": "140"
					},
					{
						"fieldname": "new_po",
						"label": _("New PO"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "ths",
						"label": _("THS"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tbv",
						"label": _("TBV"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tspl",
						"label": _("TSPL"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "nj",
						"label": _("NJ"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "cb",
						"label": _("CB"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "as",
						"label": _("AS"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "sg",
						"label": _("Sistla"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "gs",
						"label": _("GS"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "nj_comment",
						"label": _("NJ Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "cb_comment",
						"label": _("CB Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "as_comment",
						"label": _("AS Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "sg_comment",
						"label": _("Sistla Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "gs_comment",
						"label": _("GS Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "comment",
						"label": _("Comment"),
						"fieldtype": "Button",
						"width": "120"
					},
			]
		
		elif overview_status == "Expected Payments":
			cols = [
					{
						"fieldname": "months",
						"label": _("Months"),
						"fieldtype": "Data",
						"width": "200"
					},
					{
						"fieldname": "expected_payment",
						"label": _("Expected payment (Invoice Raised)"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "payment_received",
						"label": _("Payment Received"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "payment_received_other_months",
						"label": _("Payment Received of Other Months"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "payment_to_be_received",
						"label": _("Payment to be Received"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "ths_expected",
						"label": _("THS Expected"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "ths_received",
						"label": _("THS Received"),
						"fieldtype": "Currency",
						"width": "200"
					},			
					{
						"fieldname": "ths",
						"label": _("THS to be received"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tbv_expected",
						"label": _("TBV Expected"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tbv_received",
						"label": _("TBV Received"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tbv",
						"label": _("TBV to be received"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tspl_expected",
						"label": _("TSPL Expected"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tspl_received",
						"label": _("TSPL Received"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tspl",
						"label": _("TSPL to be received"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "nj",
						"label": _("NJ"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "cb",
						"label": _("CB"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "as",
						"label": _("AS"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "sg",
						"label": _("Sistla"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "gs",
						"label": _("GS"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "nj_comment",
						"label": _("NJ Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "cb_comment",
						"label": _("CB Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "as_comment",
						"label": _("AS Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "sg_comment",
						"label": _("Sistla Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "gs_comment",
						"label": _("GS Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "comment",
						"label": _("Comment"),
						"fieldtype": "Button",
						"width": "120"
					},
			]
		
		elif overview_status == "Invoice to be Raised":
			cols = [
					{
						"fieldname": "months",
						"label": _("Months"),
						"fieldtype": "Data",
						"width": "200"
					},
					{
						"fieldname": "invoice_unraised",
						"label": _("Invoice Unraised"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "invoice_raised",
						"label": _("Invoice Raised"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "invoice_to_be_raised",
						"label": _("Invoice to be raised (Unraised)"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "ths_unraised",
						"label": _("THS (Unraised))"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "ths_raised",
						"label": _("THS (Raised))"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "ths",
						"label": _("THS (to be raised)"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tbv_unraised",
						"label": _("TBV (Unraised)"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tbv_raised",
						"label": _("TBV Raised"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tbv",
						"label": _("TBV (to be Raised)"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tspl_unraised",
						"label": _("TSPL Unraised"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tspl_raised",
						"label": _("TSPL Raised"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tspl",
						"label": _("TSPL (to be raised)"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "nj",
						"label": _("NJ"),
						"fieldtype": "Data",
						"width": "200"
					},
					{
						"fieldname": "cb",
						"label": _("CB"),
						"fieldtype": "Data",
						"width": "200"
					},
					{
						"fieldname": "as",
						"label": _("AS"),
						"fieldtype": "Data",
						"width": "200"
					},
					{
						"fieldname": "sg",
						"label": _("Sistla"),
						"fieldtype": "Data",
						"width": "200"
					},
					{
						"fieldname": "gs",
						"label": _("GS"),
						"fieldtype": "Data",
						"width": "200"
					},
					{
						"fieldname": "nj_comment",
						"label": _("NJ Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "cb_comment",
						"label": _("CB Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "as_comment",
						"label": _("AS Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "sg_comment",
						"label": _("Sistla Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "gs_comment",
						"label": _("GS Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "comment",
						"label": _("Comment"),
						"fieldtype": "Button",
						"width": "120"
					},
			]		
		
		elif overview_status == "Received Payment":
			cols = [
					{
						"fieldname": "months",
						"label": _("Months"),
						"fieldtype": "Data",
						"width": "200"
					},
					{
						"fieldname": "payment_received",
						"label": _("Payment Received"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "ths",
						"label": _("THS"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tbv",
						"label": _("TBV"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "tspl",
						"label": _("TSPL"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "nj",
						"label": _("NJ"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "cb",
						"label": _("CB"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "as",
						"label": _("AS"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "sg",
						"label": _("Sistla"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "gs",
						"label": _("GS"),
						"fieldtype": "Currency",
						"width": "200"
					},
					{
						"fieldname": "nj_comment",
						"label": _("NJ Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "cb_comment",
						"label": _("CB Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "as_comment",
						"label": _("AS Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "sg_comment",
						"label": _("Sistla Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "gs_comment",
						"label": _("GS Comment"),
						"fieldtype": "Small Text",
						"width": "200"
					},
					{
						"fieldname": "comment",
						"label": _("Comment"),
						"fieldtype": "Button",
						"width": "120"
					},
			]
	else:
		cols = [
			{
				"fieldname": "months",
				"label": _("Months"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "new_po",
				"label": _("New PO"),
				"fieldtype": "Button",
				"width": "120"
			},
			{
				"fieldname": "invoice_unraised",
				"label": _("Monthly Invoice Due"),
				"fieldtype": "Button",
				"width": "180"
			},
			{
				"fieldname": "invoice_raised",
				"label": _("Monthly Invoice Raised Till Date"),
				"fieldtype": "Button",
				"width": "120"
			},
			{
				"fieldname": "invoice_to_be_raised",
				"label": _("Monthly Balance Invoice"),
				"fieldtype": "Button",
				"width": "180"
			},
			{
				"fieldname": "balance_unraised",
				"label": _("Cumulative Invoice Due"),
				"fieldtype": "Currency",
				"width": "120"
			},
			{
				"fieldname": "cumulative_invoice_raised",
				"label": _("Actual Invoice Raised"),
				"fieldtype": "Currency",
				"width": "120"
			},
			{
				"fieldname": "expected_payment",
				"label": _("Monthly Payment Due"),
				"fieldtype": "Button",
				"width": "180"
			},
			{
				"fieldname": "payment_received",
				"label": _("Monthly Payment Received till date"),
				"fieldtype": "Button",
				"width": "180"
			},
			{
				"fieldname": "payment_to_be_received",
				"label": _("Monthly Balance Due"),
				"fieldtype": "Button",
				"width": "180"
			},
			{
				"fieldname": "received_balance",
				"label": _("Cumulative Balance Due"),
				"fieldtype": "Currency",
				"width": "140"
			},
			{
				"fieldname": "cumulative_received_balance",
				"label": _("Cumulative Payment Received"),
				"fieldtype": "Currency",
				"width": "140"
			},
		]	
		
	return cols	

@frappe.whitelist()
def submit_comment(userid,comment,month,year,fortype):
	creation = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	modified = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	modified_by = frappe.session.user
	docstatus = 0
	if userid:
		data = frappe.db.sql("""insert into `tabFinancial Overview Comments`(creation,modified,modified_by,owner,docstatus,month,employee,comment,year,for_type)
values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')""".format(creation,modified,modified_by,modified_by,docstatus,month,userid,comment,year,fortype))
		a = 1
	else:
		a = 0;
		
	return a

@frappe.whitelist()
def get_comments(comment_id):
	
	data = frappe.db.sql("""select comment from `tabFinancial Overview Comments` where name = '{0}'""".format(comment_id), as_dict=True)
	for rec in data:
		comm = rec.comment
	return comm

@frappe.whitelist()
def get_finance_data(month_name,year,type,excluding_viatris):
	final_total_amount_inr_unraisedTHS1 = ''
	final_total_amount_inr_unraisedTBV1 = ''
	final_total_amount_inr_unraisedTSPL1 = ''
	final_total_amount_inr_unraisedViatris1 = ''
	if type == 'Monthly_Invoice_Due':
		dataUraisedTHS = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
						WHERE tsi.status not in ('Paid','Cancelled') and 
						tsi.company = 'Turacoz Healthcare Solutions Pvt Ltd'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
		final_total_amount_inr_unraisedTHS = float()	
		for recUnraisedTHS in dataUraisedTHS:
			final_total_amount_inr_unraisedTHS += float(recUnraisedTHS.total_inr)
			final_total_amount_inr_unraisedTHS = round(final_total_amount_inr_unraisedTHS, 2)
		final_total_amount_inr_unraisedTHS1 = '₹'+str(final_total_amount_inr_unraisedTHS)
			
		dataUraisedTBV = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr   
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
						WHERE tsi.status not in ('Paid','Cancelled') and 
						tsi.company = 'Turacoz B.V.'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
		final_total_amount_inr_unraisedTBV = float()	
		for recUnraisedTBV in dataUraisedTBV:
			final_total_amount_inr_unraisedTBV += float(recUnraisedTBV.total_inr)
			final_total_amount_inr_unraisedTBV = round(final_total_amount_inr_unraisedTBV, 2)
		final_total_amount_inr_unraisedTBV1 = '₹'+str(final_total_amount_inr_unraisedTBV)
			
		dataUraisedTSPL = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency, ter.rate_in_inr * sum(tps.payment_amount) as total_inr 
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
						WHERE tsi.status not in ('Paid','Cancelled') and 
						tsi.company = 'Turacoz Solutions PTE Ltd.'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTSPL = float()	
		for recUnraisedTSPL in dataUraisedTSPL:
			final_total_amount_inr_unraisedTSPL += float(recUnraisedTSPL.total_inr)
			final_total_amount_inr_unraisedTSPL = round(final_total_amount_inr_unraisedTSPL, 2)
		final_total_amount_inr_unraisedTSPL1 = '₹'+str(final_total_amount_inr_unraisedTSPL)
		
		if excluding_viatris == '1':
			
			dataUraisedViatris = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
						WHERE tsi.status not in ('Paid','Cancelled') and 
						tsi.customer in ('Viatris Centre of Excellence') and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
			final_total_amount_inr_unraisedViatris = float()	
			for recUnraisedViatris in dataUraisedViatris:
				final_total_amount_inr_unraisedViatris += float(recUnraisedViatris.total_inr)
				final_total_amount_inr_unraisedViatris = round(final_total_amount_inr_unraisedViatris, 2)
			final_total_amount_inr_unraisedViatris1 = '₹'+str(final_total_amount_inr_unraisedViatris)	
		else:
			final_total_amount_inr_unraisedViatris1 = '₹0.0'				
			
	elif type == 'Monthly_Balance_Invoice':			
		dataUraisedTHS = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
						WHERE tsi.status not in ('Paid','Cancelled') and 
						tsi.company = 'Turacoz Healthcare Solutions Pvt Ltd'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
		final_total_amount_inr_unraisedTHS = float()	
		for recUnraisedTHS in dataUraisedTHS:
			final_total_amount_inr_unraisedTHS += float(recUnraisedTHS.total_inr)
			final_total_amount_inr_unraisedTHS = round(final_total_amount_inr_unraisedTHS, 2)
		final_total_amount_inr_unraisedTHS1 = '₹'+str(final_total_amount_inr_unraisedTHS)
			
		dataUraisedTBV = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
						WHERE tsi.status not in ('Paid','Cancelled') and 
						tsi.company = 'Turacoz B.V.'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTBV = float()	
		for recUnraisedTBV in dataUraisedTBV:
			final_total_amount_inr_unraisedTBV += float(recUnraisedTBV.total_inr)
			final_total_amount_inr_unraisedTBV = round(final_total_amount_inr_unraisedTBV, 2)
		final_total_amount_inr_unraisedTBV1 = '₹'+str(final_total_amount_inr_unraisedTBV)
			
		dataUraisedTSPL = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
						WHERE tsi.status not in ('Paid','Cancelled') and 
						tsi.company = 'Turacoz Solutions PTE Ltd.'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTSPL = float()	
		for recUnraisedTSPL in dataUraisedTSPL:
			final_total_amount_inr_unraisedTSPL += float(recUnraisedTSPL.total_inr)
			final_total_amount_inr_unraisedTSPL = round(final_total_amount_inr_unraisedTSPL, 2)
		final_total_amount_inr_unraisedTSPL1 = '₹'+str(final_total_amount_inr_unraisedTSPL)
			
		if excluding_viatris == '1':
			dataUraisedViatris = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
						WHERE tsi.status not in ('Paid','Cancelled')
						and tsi.customer in ('Viatris Centre of Excellence') and tps.invoice_status='Unraised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
				
			final_total_amount_inr_unraisedViatris = float()	
			for recUnraisedViatris in dataUraisedViatris:
				final_total_amount_inr_unraisedViatris += float(recUnraisedViatris.total_inr)
				final_total_amount_inr_unraisedViatris = round(final_total_amount_inr_unraisedViatris, 2)
			final_total_amount_inr_unraisedViatris1 = '₹'+str(final_total_amount_inr_unraisedViatris)	
		else:
			final_total_amount_inr_unraisedViatris1 = '₹0.0'
			
	elif type == 'Invoice_Raised_Till_Date':
		dataUraisedTHS = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
						WHERE tsi.status not in ('Paid','Cancelled') and 
						tsi.company = 'Turacoz Healthcare Solutions Pvt Ltd'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Raised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTHS = float()	
		for recUnraisedTHS in dataUraisedTHS:
			final_total_amount_inr_unraisedTHS += float(recUnraisedTHS.total_inr)
			final_total_amount_inr_unraisedTHS = round(final_total_amount_inr_unraisedTHS, 2)
		final_total_amount_inr_unraisedTHS1 = '₹'+str(final_total_amount_inr_unraisedTHS)
			
		dataUraisedTBV = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
						WHERE tsi.status not in ('Paid','Cancelled') and 
						tsi.company = 'Turacoz B.V.'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Raised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTBV = float()	
		for recUnraisedTBV in dataUraisedTBV:
			final_total_amount_inr_unraisedTBV += float(recUnraisedTBV.total_inr)
			final_total_amount_inr_unraisedTBV = round(final_total_amount_inr_unraisedTBV, 2)
		final_total_amount_inr_unraisedTBV1 = '₹'+str(final_total_amount_inr_unraisedTBV)
			
		dataUraisedTSPL = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
						tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
						from `tabSales Invoice` tsi 
						left join `tabPayment Schedule` tps on tsi.name = tps.parent
						left join `tabProject` tp on tsi.project = tp.name
						left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
						WHERE tsi.status not in ('Paid','Cancelled') and 
						tsi.company = 'Turacoz Solutions PTE Ltd.'
						and tsi.customer not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and tps.invoice_status='Raised' and
						MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTSPL = float()	
		for recUnraisedTSPL in dataUraisedTSPL:
			final_total_amount_inr_unraisedTSPL += float(recUnraisedTSPL.total_inr)
			final_total_amount_inr_unraisedTSPL = round(final_total_amount_inr_unraisedTSPL, 2)
		final_total_amount_inr_unraisedTSPL1 = '₹'+str(final_total_amount_inr_unraisedTSPL)
			
		if excluding_viatris == '1':
			dataUraisedViatris = frappe.db.sql("""select sum(tps.payment_amount) as total_amount,
				tsi.currency,ter.rate_in_inr * sum(tps.payment_amount) as total_inr  
				from `tabSales Invoice` tsi 
				left join `tabPayment Schedule` tps on tsi.name = tps.parent
				left join `tabProject` tp on tsi.project = tp.name
				left join `tabCurrency Exchange Rate` ter on tsi.currency = ter.name
				WHERE tsi.status not in ('Paid','Cancelled')
				and tsi.customer in ('Viatris Centre of Excellence') and tps.invoice_status='Raised' and
				MONTHNAME(STR_TO_DATE(MONTH(tps.due_date),'%m')) = '{0}' and YEAR(tps.due_date) = '{1}' GROUP by tsi.currency""".format(month_name,year), as_dict=True)
			
			final_total_amount_inr_unraisedViatris = float()	
			for recUnraisedViatris in dataUraisedViatris:
				final_total_amount_inr_unraisedViatris += float(recUnraisedViatris.total_inr)
				final_total_amount_inr_unraisedViatris = round(final_total_amount_inr_unraisedViatris, 2)
			final_total_amount_inr_unraisedViatris1 = '₹'+str(final_total_amount_inr_unraisedViatris)	
		else:
			final_total_amount_inr_unraisedViatris1 = '₹0.0'	
			
	elif type == 'Monthly_Payment_Due':
		dataUraisedTHS = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
					tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Cancelled') and 
					tpr.company = 'Turacoz Healthcare Solutions Pvt Ltd'
					and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTHS = float()	
		for recUnraisedTHS in dataUraisedTHS:
			final_total_amount_inr_unraisedTHS += float(recUnraisedTHS.total_inr)
			final_total_amount_inr_unraisedTHS = round(final_total_amount_inr_unraisedTHS, 2)
		final_total_amount_inr_unraisedTHS1 = '₹'+str(final_total_amount_inr_unraisedTHS)
			
		dataUraisedTBV = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
					tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Cancelled') and 
					tpr.company = 'Turacoz B.V.'
					and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTBV = float()	
		for recUnraisedTBV in dataUraisedTBV:
			final_total_amount_inr_unraisedTBV += float(recUnraisedTBV.total_inr)
			final_total_amount_inr_unraisedTBV = round(final_total_amount_inr_unraisedTBV, 2)
		final_total_amount_inr_unraisedTBV1 = '₹'+str(final_total_amount_inr_unraisedTBV)
			
		dataUraisedTSPL = frappe.db.sql("""select sum(tpr.grand_total) as total_amount,
					tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Cancelled') and 
					tpr.company = 'Turacoz Solutions PTE Ltd.'
					and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
		
		final_total_amount_inr_unraisedTSPL = float()	
		for recUnraisedTSPL in dataUraisedTSPL:
			final_total_amount_inr_unraisedTSPL += float(recUnraisedTSPL.total_inr)
			final_total_amount_inr_unraisedTSPL = round(final_total_amount_inr_unraisedTSPL, 2)
		final_total_amount_inr_unraisedTSPL1 = '₹'+str(final_total_amount_inr_unraisedTSPL)
			
		if excluding_viatris == '1':
			dataUraisedViatris = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Cancelled')
					and tpr.due_date is not NULL and
					tpr.party in ('Viatris Centre of Excellence') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
			final_total_amount_inr_unraisedViatris = float()	
			for recUnraisedViatris in dataUraisedViatris:
				final_total_amount_inr_unraisedViatris += float(recUnraisedViatris.total_inr)
				final_total_amount_inr_unraisedViatris = round(final_total_amount_inr_unraisedViatris, 2)
			final_total_amount_inr_unraisedViatris1 = '₹'+str(final_total_amount_inr_unraisedViatris)	
		else:
			final_total_amount_inr_unraisedViatris1 = '₹0.0'	
			
	elif type =='Payment_Received_Till_Date':
		dataUraisedTHS = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name  
					WHERE tpr.payment_status in ('Paid') and 
					tpr.company = 'Turacoz Healthcare Solutions Pvt Ltd' and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
		
		final_total_amount_inr_unraisedTHS = float()	
		for recUnraisedTHS in dataUraisedTHS:
			final_total_amount_inr_unraisedTHS += float(recUnraisedTHS.total_inr)
			final_total_amount_inr_unraisedTHS = round(final_total_amount_inr_unraisedTHS, 2)
		final_total_amount_inr_unraisedTHS1 = '₹'+str(final_total_amount_inr_unraisedTHS)
			
		dataUraisedTBV = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name 
					WHERE tpr.payment_status in ('Paid') and 
					tpr.company = 'Turacoz B.V.'
					and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTBV = float()	
		for recUnraisedTBV in dataUraisedTBV:
			final_total_amount_inr_unraisedTBV += float(recUnraisedTBV.total_inr)
			final_total_amount_inr_unraisedTBV = round(final_total_amount_inr_unraisedTBV, 2)
		final_total_amount_inr_unraisedTBV1 = '₹'+str(final_total_amount_inr_unraisedTBV)
			
		dataUraisedTSPL = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name 
					WHERE tpr.payment_status in ('Paid') and 
					tpr.company = 'Turacoz Solutions PTE Ltd.'
					and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTSPL = float()	
		for recUnraisedTSPL in dataUraisedTSPL:
			final_total_amount_inr_unraisedTSPL += float(recUnraisedTSPL.total_inr)
			final_total_amount_inr_unraisedTSPL = round(final_total_amount_inr_unraisedTSPL, 2)
		final_total_amount_inr_unraisedTSPL1 = '₹'+str(final_total_amount_inr_unraisedTSPL)
			
		if excluding_viatris == '1':
			dataUraisedViatris = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status in ('Paid')
					and tpr.due_date is not NULL and
					tpr.party in ('Viatris Centre of Excellence') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
			
			final_total_amount_inr_unraisedViatris = float()	
			for recUnraisedViatris in dataUraisedViatris:
				final_total_amount_inr_unraisedViatris += float(recUnraisedViatris.total_inr)
				final_total_amount_inr_unraisedViatris = round(final_total_amount_inr_unraisedViatris, 2)
			final_total_amount_inr_unraisedViatris1 = '₹'+str(final_total_amount_inr_unraisedViatris)	
		else:
			final_total_amount_inr_unraisedViatris1 = '₹0.0'		
			
	elif type == 'Monthly_Balance_Due':
		dataUraisedTHS = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Paid','Cancelled') and 
					tpr.company = 'Turacoz Healthcare Solutions Pvt Ltd'
					and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTHS = float()	
		for recUnraisedTHS in dataUraisedTHS:
			final_total_amount_inr_unraisedTHS += float(recUnraisedTHS.total_inr)
			final_total_amount_inr_unraisedTHS = round(final_total_amount_inr_unraisedTHS, 2)
		final_total_amount_inr_unraisedTHS1 = '₹'+str(final_total_amount_inr_unraisedTHS)
			
		dataUraisedTBV = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Paid','Cancelled') and 
					tpr.company = 'Turacoz B.V.'
					and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTBV = float()	
		for recUnraisedTBV in dataUraisedTBV:
			final_total_amount_inr_unraisedTBV += float(recUnraisedTBV.total_inr)
			final_total_amount_inr_unraisedTBV = round(final_total_amount_inr_unraisedTBV, 2)
		final_total_amount_inr_unraisedTBV1 = '₹'+str(final_total_amount_inr_unraisedTBV)
			
		dataUraisedTSPL = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Paid','Cancelled') and 
					tpr.company = 'Turacoz Solutions PTE Ltd.'
					and tpr.due_date is not NULL and
					tpr.party not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
				
		final_total_amount_inr_unraisedTSPL = float()	
		for recUnraisedTSPL in dataUraisedTSPL:
			final_total_amount_inr_unraisedTSPL += float(recUnraisedTSPL.total_inr)
			final_total_amount_inr_unraisedTSPL = round(final_total_amount_inr_unraisedTSPL, 2)
		final_total_amount_inr_unraisedTSPL1 = '₹'+str(final_total_amount_inr_unraisedTSPL)
			
		if excluding_viatris == '1':
			dataUraisedViatris = frappe.db.sql("""select sum(tpr.grand_total) as total_amount, 
					tpr.invoice_currency as currency,ter.rate_in_inr * sum(tpr.grand_total) as total_inr 
					from `tabPayment Request` tpr  
					left join `tabCurrency Exchange Rate` ter on tpr.invoice_currency = ter.name
					WHERE tpr.payment_status not in ('Paid','Cancelled')
					and tpr.due_date is not NULL and
					tpr.party in ('Viatris Centre of Excellence') and
					MONTHNAME(STR_TO_DATE(MONTH(tpr.due_date),'%m')) = '{0}' and YEAR(tpr.due_date) = '{1}' GROUP by tpr.invoice_currency""".format(month_name,year), as_dict=True)
			
			final_total_amount_inr_unraisedViatris = float()	
			for recUnraisedViatris in dataUraisedViatris:
				final_total_amount_inr_unraisedViatris += float(recUnraisedViatris.total_inr)
				final_total_amount_inr_unraisedViatris = round(final_total_amount_inr_unraisedViatris, 2)
			final_total_amount_inr_unraisedViatris1 = '₹'+str(final_total_amount_inr_unraisedViatris)	
		else:
			final_total_amount_inr_unraisedViatris1 = '₹0.0'
							
	elif type == 'New_Po':
		
		dataUraisedTHS = frappe.db.sql("""select sum(tso.net_total) as total_amount ,tso.currency,
								count(tp.name) as project_count,ter.rate_in_inr * sum(tso.net_total) as total_inr
								from `tabSales Order` tso 
								left join `tabProject` tp on tso.project = tp.name
								left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
								WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
								and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
								and tp.project_current_status not in ('Cancelled') and 
								tso.company='Turacoz Healthcare Solutions Pvt Ltd' GROUP by tso.currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTHS = float()	
		for recUnraisedTHS in dataUraisedTHS:
			final_total_amount_inr_unraisedTHS += float(recUnraisedTHS.total_inr)
			final_total_amount_inr_unraisedTHS = round(final_total_amount_inr_unraisedTHS, 2)
		final_total_amount_inr_unraisedTHS1 = '₹'+str(final_total_amount_inr_unraisedTHS)
			
		dataUraisedTBV = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
								tso.currency,count(tp.name) as project_count,
								ter.rate_in_inr * sum(tso.net_total) as total_inr
								from `tabSales Order` tso 
								left join `tabProject` tp on tso.project = tp.name
								left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
								WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
								and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
								and tp.project_current_status not in ('Cancelled') and 
								tso.company='Turacoz B.V.' GROUP by tso.currency""".format(month_name,year), as_dict=True)
			
		final_total_amount_inr_unraisedTBV = float()	
		for recUnraisedTBV in dataUraisedTBV:
			final_total_amount_inr_unraisedTBV += float(recUnraisedTBV.total_inr)
			final_total_amount_inr_unraisedTBV = round(final_total_amount_inr_unraisedTBV, 2)
		final_total_amount_inr_unraisedTBV1 = '₹'+str(final_total_amount_inr_unraisedTBV)
			
		dataUraisedTSPL = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
								tso.currency,count(tp.name) as project_count,
								ter.rate_in_inr * sum(tso.net_total) as total_inr  
								from `tabSales Order` tso 
								left join `tabProject` tp on tso.project = tp.name
								left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
								WHERE tp.customer  not in ('Viatris Centre of Excellence','Turacoz Solutions LLC','Turacoz Solutions PTE Ltd','Turacoz Healthcare Solution Pvt Ltd')
								and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
								and tp.project_current_status not in ('Cancelled') and 
								tso.company='Turacoz Solutions PTE Ltd.' GROUP by tso.currency""".format(month_name,year), as_dict=True)
				
		final_total_amount_inr_unraisedTSPL = float()	
		for recUnraisedTSPL in dataUraisedTSPL:
			final_total_amount_inr_unraisedTSPL += float(recUnraisedTSPL.total_inr)
			final_total_amount_inr_unraisedTSPL = round(final_total_amount_inr_unraisedTSPL, 2)									
		final_total_amount_inr_unraisedTSPL1 = '₹'+str(final_total_amount_inr_unraisedTSPL)
		
		if excluding_viatris == 1:
			dataUraisedViatris = frappe.db.sql("""select sum(tso.net_total) as total_amount ,
				tso.currency,count(tp.name) as project_count  
				ter.rate_in_inr * sum(tso.net_total) as total_inr 
				from `tabSales Order` tso 
				left join `tabProject` tp on tso.project = tp.name
				left join `tabCurrency Exchange Rate` ter on tso.currency = ter.name
				WHERE tp.customer in ('Viatris Centre of Excellence')
				and MONTHNAME(STR_TO_DATE(MONTH(tp.creation),'%m')) = '{0}' and YEAR(tp.creation) = '{1}' 
				and tp.project_current_status not in ('Cancelled')
				GROUP by tso.currency""".format(month_name,year), as_dict=True)
			
			final_total_amount_inr_unraisedViatris = float()	
			for recUnraisedViatris in dataUraisedViatris:
				final_total_amount_inr_unraisedViatris += float(recUnraisedViatris.total_inr)
				final_total_amount_inr_unraisedViatris = round(final_total_amount_inr_unraisedViatris, 2)
			final_total_amount_inr_unraisedViatris1 = '₹'+str(final_total_amount_inr_unraisedViatris)	
		else:
			final_total_amount_inr_unraisedViatris1 = '₹0.0'										
	
	if excluding_viatris == '1':		
		message="<table width='100%' border='1'><thead style='background-color:green; color:white;'><th>THS "+type+"</th><th>TBV "+type+"</th><th>TSPL "+type+"</th><th>Viatris "+type+"</th></thead><tr><td>"+str(final_total_amount_inr_unraisedTHS1)+"</td><td>"+str(final_total_amount_inr_unraisedTBV1)+"</td><td>"+str(final_total_amount_inr_unraisedTSPL1)+"</td><td>"+str(final_total_amount_inr_unraisedViatris1)+"</td></tr></table>"
	else:
		message="<table width='100%' border='1'><thead style='background-color:green; color:white;'><th>THS "+type+"</th><th>TBV "+type+"</th><th>TSPL "+type+"</th></thead><tr><td>"+str(final_total_amount_inr_unraisedTHS1)+"</td><td>"+str(final_total_amount_inr_unraisedTBV1)+"</td><td>"+str(final_total_amount_inr_unraisedTSPL1)+"</td></tr></table>"	
	return message
	
	
