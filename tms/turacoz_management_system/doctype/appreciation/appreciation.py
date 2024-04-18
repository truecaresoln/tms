# -*- coding: utf-8 -*-
# Copyright (c) 2022, RSA and contributors
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
from erpnext.hr.doctype.daily_work_summary.daily_work_summary import get_users_email
from erpnext.hr.doctype.holiday_list.holiday_list import is_holiday
from frappe.model.document import Document

class Appreciation(Document):
	
	def validate(self):
		self.send_welcome_email()
		
		
	def send_welcome_email(self):
		if self.deliverable:
			deliverable = self.deliverable
		else:
			deliverable	= ''
		sub = "You Appreciated by Client for deliverable "+str(deliverable)+" for project "+str(self.project)
# 		msg = """
# 		<p><b>Dear </b></p>
# 		"""
# 		
# 		url = "http://erp.turacoz.com:8000/desk#Form/Project/{0}".format(self.project)
# 		messages = (
# 			_("You got the new project: {0}".format(self.project)),
# 			url,
# 			_("Join")
# 		)
# 
# 		content = """
# 		<p>{0}.</p>
# 		<p><a href="{1}">{2}</a></p>
# 		"""

		for user in self.involve_team:
			
			msg = """
			<p><b>Dear {0},</b></p>
			<p>You have been appreciated by the client for <b>{1}</b> for project <b>{2}</b>.</p>
			<p><b>Client Feedback: </b>{3}</p>
			<p>Thank You for your effort.</p>
			<p><b>Thanks,</b></p></br>
			<b>Turacoz Group</b>
			""".format(user.employee_name,deliverable,self.project,self.client_feedback)
			
			url = "http://erp.turacoz.com:8000/desk#Form/Project/{0}".format(self.project)
			messages = (
				_(msg),
				url,
				_("Join")
			)
	
			content = """
			<p>{0}.</p>
			<p><a href="{1}">{2}</a></p>
			"""
			
			if user.email_sent == 0:
				frappe.sendmail(user.involve_team_member, subject=_(sub),
								content=content.format(*messages))
				user.email_sent = 1	
	
	pass
	
