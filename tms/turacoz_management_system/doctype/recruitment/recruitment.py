# -*- coding: utf-8 -*-
# Copyright (c) 2021, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from six import iteritems
from email_reply_parser import EmailReplyParser
from frappe.utils import (flt, getdate, get_url, now,
	nowtime, get_time, today, get_datetime, add_days)
from erpnext.controllers.queries import get_filters_cond
from frappe.desk.reportview import get_match_cond
from erpnext.hr.doctype.daily_work_summary.daily_work_summary import get_users_email
from erpnext.hr.doctype.holiday_list.holiday_list import is_holiday
from frappe.model.document import Document
import datetime
import calendar

class Recruitment(Document):
	pass

@frappe.whitelist(allow_guest=True)
def send_credentials_notification(self,method=None):
	lms_credentials_check = self.lms_credentials_generated
	user_email = self.email
	user_id = self.user_id
	password = self.password
	assignment_link = self.assignment_link 
	candidate_name = self.candidate_name
	date = str(self.date)
	time = str(self.time)
	
	if lms_credentials_check == 1:
		if user_email:
			messages = "<p><b>Dear "+candidate_name+" ,</b></p><p>As discussed, your assignment has been scheduled for "+date+", "+time+"</p><p>Please go through with the user guide and login with the shared credential before assignment starts. Do let us know in case you find any difficulty while login.</p><p><b> LMS login credentials:</b></p><li><b>Module URL link: </b><a href='"+assignment_link+"'>"+assignment_link+"</a></li><li><b>User ID : </b>"+user_id+"</li><li><b>Password : </b>"+password+"</li><p> In case of any further query, do let me know. Would be happy to assist.</p><p> Good Luck </p><p><b>Note : Acknowledge once you receive and start your assignment.</b></p><p><b>Thanks & Best Regards,</b></p>"
			subject_fn = "Link and Credentials of the assignment"
			mylist = [user_email,'atul.teotia@turacoz.com','sapna.rajpoot@turacoz.com']
			frappe.sendmail(recipients=mylist,
						subject=_(subject_fn),
						message = messages,
						)
		
	
	
