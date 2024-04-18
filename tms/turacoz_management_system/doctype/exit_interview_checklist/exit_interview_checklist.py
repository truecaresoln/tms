# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ExitInterviewChecklist(Document):
	pass

@frappe.whitelist(allow_guest=True)
def get_emp_id(userid):
	if userid:
		getData = frappe.db.sql("""select te.name,te.employee_name,te.designation,td.department_name,te.cell_number,
			tee.employee_name as reporting_to,te.date_of_joining from `tabEmployee` te
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