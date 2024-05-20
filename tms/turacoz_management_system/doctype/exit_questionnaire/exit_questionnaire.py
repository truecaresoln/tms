# Copyright (c) 2024, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from six import iteritems
from email_reply_parser import EmailReplyParser
from frappe.utils import (flt, getdate, get_url, now,
	nowtime, get_time, today, get_datetime, add_days)
from erpnext.controllers.queries import get_filters_cond
from frappe.desk.reportview import get_match_cond
from hrms.hr.doctype.daily_work_summary.daily_work_summary import get_users_email
from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday
from frappe.model.document import Document

class ExitQuestionnaire(Document):
	pass

@frappe.whitelist(allow_guest=True)
def get_emp_id(userid):
	if userid:
		getData = frappe.db.sql("""select te.employee_name,te.designation,td.department_name,te.cell_number,
			tee.employee_name as reporting_to from `tabEmployee` te
			left join `tabDepartment` td on te.department = td.name
			left join `tabEmployee`tee on te.reports_to = tee.name 
			where te.user_id = '{0}';""".format(userid), as_dict = True)
		
		if getData:
			emp_code = getData
		else:
			emp_code = ''
	else:
		emp_code = ''		
	return emp_code
