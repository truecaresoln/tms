# -*- coding: utf-8 -*-
# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tms.utils.approvals import insert_approvals

class EmployeeResignation(Document):
	
	def validate(self):
		self.validate_resignation_date()
		self.validate_relieving_date()
		self.update_approval()
		if self._action == "submit":
			if self.status != "Approved":
				frappe.throw(("Please select 'Approved' in status field before Approve the resignation."))
	
	
	def update_approval(self):
		document = "Employee Resignation"
		if(self.workflow_state == 'Draft'):
			employee = frappe.db.sql("""select user_id as name from `tabEmployee` where name='{0}';""".format(self.employee),as_dict = True)
			insert_approvals(document,self.name,self.reporting_manager,self.reporting_manager_name,employee[0]["name"],self.employee_name,self.workflow_state)
		elif(self.workflow_state == 'Accepted'):
			approver = frappe.db.sql("""select thr.parent,thr.role,tu.full_name from `tabHas Role` thr
					left join `tabUser` tu on thr.parent=tu.name
					where thr.role='Employee Resignation' limit 1""",as_dict = True)
			employee = frappe.db.sql("""select user_id as name from `tabEmployee` where name='{0}';""".format(self.employee),as_dict = True)
			reporting_manager_id = approver[0]['parent']
			full_name = approver[0]['full_name']
			insert_approvals(document,self.name,reporting_manager_id,full_name,employee[0]["name"],self.employee_name,self.workflow_state)

	def validate_resignation_date(self):
		empid = self.employee
		resignation_date = self.effective_date
		fn_reliving_date = self.dm_relieving_date
		
		# date_time_obj = datetime.datetime.strftime(resignation_date, '%Y-%m-%d')
		# dt = self.effective_date
		# date_time_obj = datetime.strptime(dt,'%Y-%m-%d').date()		
		# three_mon_rel = relativedelta(months=3)
		# fndate = date_time_obj + three_mon_rel
		# nfdate = fndate.strftime('%Y-%m-%d')
		# fn_reliving_date = nfdate
		
		# frappe.msgprint(fn_reliving_date)
			
		
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
