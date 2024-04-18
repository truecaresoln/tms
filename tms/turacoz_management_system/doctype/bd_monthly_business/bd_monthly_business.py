# Copyright (c) 2023, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date, datetime, timedelta

class BDMonthlyBusiness(Document):
	pass

def validate_bd_monthly_business():
	today = datetime.today()
	year = today.year
	month = today.month
	first_date = get_first_date_of_current_month(year,month)
	last_date = get_last_date_of_month(year, month)
		
	dataEmployee  = frappe.db.sql("""select name,user_id,employee_name from `tabEmployee` te 
	where te.status = 'Active' and te.department in ('Business Development - THS','Marketing & Sales - THS');""", as_dict = True)
	
	if dataEmployee:
		for rec1 in dataEmployee:
			total_business = 0
			userid = rec1.user_id
			empid = rec1.name
			employee_name = rec1.employee_name
			
			data = frappe.db.sql("""SELECT tp.name,tp.bd_name, tp.bd_person, tso.grand_total, 
				tso.currency,tcer.rate_in_inr,(tso.grand_total*tcer.rate_in_inr) as final_rate_in_inr from `tabProject` tp
				left join `tabSales Order` tso on tp.name = tso.project
				left join `tabCurrency Exchange Rate` tcer on tso.currency = tcer.name 
				where tp.project_current_status not in ('Cancelled') 
				and tp.status not in ('Cancelled') and tp.bd_person='{0}' 
				and tp.expected_start_date BETWEEN '{1}' and '{2}';""".format(userid,first_date,last_date), as_dict=True)
	
			if data:
				for rec in data:
					total_business += rec.final_rate_in_inr
				
				set_monthly_bd_business(empid,employee_name,total_business,year)	
	
def get_last_date_of_month(year, month):
	if month == 12:
		last_date = datetime(year, month, 31)
	else:
		last_date = datetime(year, month + 1, 1) + timedelta(days=-1)
	
	return last_date.strftime("%Y-%m-%d")

def get_first_date_of_current_month(year, month):
	first_date = datetime(year, month, 1)
	return first_date.strftime("%Y-%m-%d")

def set_monthly_bd_business(empid,employee_name,total_business,year):
	from datetime import date
	from dateutil.relativedelta import relativedelta
	
	modified_by = frappe.session.user
	owner = frappe.session.user
	
	todays_date = date.today()
	month_name = todays_date.strftime("%B")
	
	name = empid+'-'+month_name+'-'+str(year)
	
	dataGetMonthlyTarget = frappe.db.sql("""select tmd.employee,tmdp.amount from `tabMonthly Distribution` tmd 
		left join `tabMonthly Distribution Percentage` tmdp on tmd.name = tmdp.parent 
		where tmd.employee = '{0}' and tmdp.`month` = '{1}' and tmdp.`year` = '{2}';""".format(empid,month_name,year), as_dict=True)
	if dataGetMonthlyTarget:
		monthly_target = dataGetMonthlyTarget[0]['amount']
	else:
		monthly_target = ''	
	
	if monthly_target:
		mt = monthly_target
	else:
		mt = 0
		
	if total_business:
		tb = total_business
	else:
		tb = 0			
	
	target_rest = mt-tb
	
	dataGet = frappe.db.sql("""Select * from `tabBD Monthly Business` where name = '{0}';""".format(name), as_dict=True)
	if dataGet:
		dataSet = frappe.db.sql("""Update `tabBD Monthly Business` set total_business_in_inr='{1}',modified='{2}',targeted_amount='{3}',pending_target='{4}' where name='{0}';""".format(name,total_business,todays_date,mt,target_rest))
	else:
		dataSet = frappe.db.sql("""insert into `tabBD Monthly Business`(name,creation,modified,
			modified_by,owner,bd_person,
			bd_person_name,month,total_business_in_inr,year,targeted_amount,pending_target) 
			values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}');""".format(name,todays_date,todays_date,modified_by,owner,empid,employee_name,month_name,total_business,year,mt,target_rest))










