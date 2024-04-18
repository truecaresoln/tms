# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeesRelievingLetter(Document):
	
	def validate(self):
		self.validate_conditions()
  # self.validate_open_task()
  # self.validate_exit_checklist()
	
	def validate_open_task(self):
		empid = self.employee
		employee_name = self.employee_name
		
		getToDoOpenData = frappe.db.sql("""Select ttd.owner,ttd.description,ttd.status,ttd.role from `tabEmployee` te
			left join `tabToDo` ttd on te.user_id = ttd.owner
			where te.name = '{0}' and ttd.status in ('Open');""".format(empid), as_dict = True)
		openTaskCount = len(getToDoOpenData)
		
		if len(getToDoOpenData) > 0:
			frappe.throw(("You can't create the Relieving Letter. "+ employee_name +" have "+ str(openTaskCount) +" open tasks."))
			
	def validate_exit_checklist(self):
		empid = self.employee
		employee_name = self.employee_name
		
		getExitCheckList = frappe.db.sql("""Select count(teec.name) as employee_exit_checklist from `tabEmployee` te
			left join `tabEmployee Exit Checklist` teec on te.user_id = teec.employee_code
			where te.name = '{0}';""".format(empid), as_dict = True)
		
		exitCount = getExitCheckList[0]['employee_exit_checklist']
		
		if exitCount == 0:
			frappe.throw(("You can't create the Relieving Letter due Software/Hardware exit not find over ERP. Kindly connect with IT Manager"))
	
	def validate_conditions(self):
		empid = self.employee
		employee_name = self.employee_name
		
		getToDoOpenData = frappe.db.sql("""Select ttd.owner,ttd.description,ttd.status,ttd.role from `tabEmployee` te
			left join `tabToDo` ttd on te.user_id = ttd.owner
			where te.name = '{0}' and ttd.status in ('Open');""".format(empid), as_dict = True)
		openTaskCount = len(getToDoOpenData)
		
		if len(getToDoOpenData) > 0:
			strmsgTask = "You can't create the Relieving Letter. "+ employee_name +" have "+ str(openTaskCount) +" open tasks."
		else:
			strmsgTask = ''	
		
		getExitCheckList = frappe.db.sql("""Select count(teec.name) as employee_exit_checklist from `tabEmployee` te
			left join `tabEmployee Exit Checklist` teec on te.user_id = teec.employee_code
			where te.name = '{0}';""".format(empid), as_dict = True)
		
		exitCount = getExitCheckList[0]['employee_exit_checklist']
		
		if exitCount == 0:
			exitmsg = "You can't create the Relieving Letter due Software/Hardware exit is pending over ERP. Kindly connect with IT Manager."
		else:
			exitmsg = ''
			
		getExitInterviewChecklist = frappe.db.sql("""Select count(te.name) as exit_interview_checklist from `tabExit Interview Checklist` te
			where te.name = '{0}';""".format(empid), as_dict = True)
		exitInterviewCount = getExitInterviewChecklist[0]['exit_interview_checklist']
		
		if exitInterviewCount == 0:
			exitInterviewMsg = "You can't create the Relieving Letter due to Exit Interview Checklist is pending over ERP. Kindly connect with Employee."
		else:
			exitInterviewMsg = ''
			
		getEmployeeHandover = frappe.db.sql("""Select count(te.name) as employee_handover from `tabEmployee Handover Form` te
			where te.name = '{0}';""".format(empid), as_dict = True)
		handoverCount = getEmployeeHandover[0]['employee_handover']
		
		if handoverCount == 0:
			handovermsg = "You can't create the Relieving Letter due to Handover Form is pending over ERP. Kindly connect with Employee."
		else:
			handovermsg = ''				
				
		finalStrMsg = strmsgTask+ '<br>' +exitmsg+ '<br>' +exitInterviewMsg+ '<br>' +handovermsg
		
		
		if len(finalStrMsg) > 12:
			frappe.throw((finalStrMsg))
		
				
					
		
				