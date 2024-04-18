# -*- coding: utf-8 -*-
# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from dateutil.relativedelta import relativedelta
import datetime

class EmployeeResignation(Document):
	
	def validate(self):
		self.validate_resignation_date()
		self.validate_relieving_date()
		
		if self._action == "submit":
			if self.status != "Approved":
				frappe.throw(("Please select 'Approved' in status field before Approve the resignation."))
	
	def validate_resignation_date(self):
		empid = self.employee
		resignation_date = self.effective_date
		
		date_time_obj = datetime.datetime.strptime(resignation_date, '%Y-%m-%d')		
		three_mon_rel = relativedelta(months=3)
		fndate = date_time_obj + three_mon_rel
		nfdate = fndate.strftime('%Y-%m-%d')
		fn_reliving_date = nfdate
		
		frappe.msgprint(fn_reliving_date)
			
		
		if empid:
			if self.effective_date:
				data = frappe.db.sql("""update `tabEmployee` set resignation_letter_date = '{0}', relieving_date='{2}' where name = '{1}';""".format(resignation_date,empid,fn_reliving_date))
				
	def validate_relieving_date(self):
		empid = self.employee
		relieving_date = self.relieving_date
		
		if empid:
			if self.relieving_date:
				data = frappe.db.sql("""update `tabEmployee` set relieving_date = '{0}' where name = '{1}';""".format(relieving_date,empid))
		
					
	
@frappe.whitelist(allow_guest=True)
def update_employee_resignation_date(self,method=None):
	empid = self.employee
	resignation_date = self.effective_date
	
	if empid:
		data = frappe.db.sql("""update `tabEmployee` set resignation_letter_date = '{0}' where name = '{1}';""".format(resignation_date,empid))
	
@frappe.whitelist(allow_guest=True)
def update_employee_relieving_date(self,method=None):
	empid = self.employee
	relieving_date = self.relieving_date
	
	if empid:
		data = frappe.db.sql("""update `tabEmployee` set relieving_date = '{0}' where name = '{1}';""".format(relieving_date,empid))
	

@frappe.whitelist(allow_guest=True)	
def get_empid(userid):
	if userid:
		getData = frappe.db.sql("""select name from `tabEmployee` where user_id = '{0}';""".format(userid), as_dict = True)
		if getData:
			empid = getData[0]['name']
		else:
			empid = ''
	else:
		empid = ''		
	return empid		
