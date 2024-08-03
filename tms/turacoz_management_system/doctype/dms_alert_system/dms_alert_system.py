# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe import _, scrub, throw
from frappe.model.naming import set_name_by_naming_series
from frappe.permissions import (
	add_user_permission,
	get_doc_permissions,
	has_permission,
	remove_user_permission,
)
from frappe.utils import add_years, cstr, getdate, today, validate_email_address
from frappe.utils.nestedset import NestedSet

from erpnext.utilities.transaction_base import delete_events
from dateutil.relativedelta import relativedelta
import datetime
import calendar
from datetime import timedelta 
from frappe.model.document import Document

class DMSALERTSYSTEM(Document):
	pass							

def send_alert():
	today = datetime.datetime.now()
	current_month = today.month
	current_day = today.day
	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	weekdays = days[today.weekday()]
		
	getAlertData = frappe.db.sql("""select tdas.name, tdas.owner, 
			employee_name,alert_type,
			frequency,time,description from `tabDMS ALERT SYSTEM` tdas 
			where tdas.alert_status = 'Active'""", as_dict = True)
		
	if getAlertData:
		for rec in getAlertData:
			if rec.alert_type == "DMS":
    # owner = rec.owner
				allocate_to = ''
				employee_name = rec.employee_name
				frequency = rec.frequency
				parent = rec.name
    # todo_name = str(parent)+'-'+str(owner)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
				reference_type = 'DMS ALERT SYSTEM'
				description = rec.description
				if rec.time:
					time = rec.time
				else:
					time = ''	
				
				if rec.frequency == "Monthly":	
					getAlertDates = frappe.db.sql("""select name,parent,month_date,description,allocate_to,allocate_to_name,process_type from `tabMonth Child DMS` 
						where parent = '{1}'
						and month_date='{0}';""".format(current_day,parent), as_dict = True)
					if getAlertDates:
						for rec1 in getAlertDates:
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly upload the respective data i.e. ("+rec1.description+") in ERP DMS on time. Link attached below.</i></p><p><a href='https://erp.turacoz.com/app/document-management-system/new-document-management-system-1' target='_blank'>https://erp.turacoz.com/app/document-management-system/new-document-management-system-1</a></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("DMS Alert for "+parent+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_duedate = today + timedelta(days=1)
							insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
				elif rec.frequency == "Quarterly":
					getAlertDates = frappe.db.sql("""select name,parent,month,day,description,allocate_to,allocate_to_name,process_type from `tabQuarterly DMS` 
						where parent = '{2}' 
						and month = '{0}' 
						and day='{1}';""".format(current_month,current_day,parent), as_dict = True)
					
					if getAlertDates:
						for rec1 in getAlertDates:
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly upload the respective data i.e. ("+rec1.description+") in ERP DMS on time. Link attached below.</i></p><p><a href='https://erp.turacoz.com/app/document-management-system/new-document-management-system-1' target='_blank'>https://erp.turacoz.com/app/document-management-system/new-document-management-system-1</a></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("DMS Alert for "+parent+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_duedate = today + timedelta(days=1)
							insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
				elif rec.frequency == "Half Yearly":
					getAlertDates = frappe.db.sql("""select name,parent,month,day,description,allocate_to,allocate_to_name,process_type from `tabQuarterly DMS` 
						where parent = '{2}' 
						and month = '{0}' 
						and day='{1}';""".format(current_month,current_day,parent), as_dict = True)
					
					if getAlertDates:
						for rec1 in getAlertDates:
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly upload the respective data i.e. ("+rec1.description+") in ERP DMS on time. Link attached below.</i></p><p><a href='https://erp.turacoz.com/app/document-management-system/new-document-management-system-1' target='_blank'>https://erp.turacoz.com/app/document-management-system/new-document-management-system-1</a></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("DMS Alert for "+parent+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_duedate = today + timedelta(days=1)
							insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
				elif rec.frequency == "Yearly":
					getAlertDates = frappe.db.sql("""select name,parent,month,day,description,allocate_to,allocate_to_name,process_type from `tabQuarterly DMS` 
						where parent = '{2}' 
						and month = '{0}' 
						and day='{1}';""".format(current_month,current_day,parent), as_dict = True)
					
					if getAlertDates:
						for rec1 in getAlertDates:
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly upload the respective data i.e. ("+rec1.description+") in ERP DMS on time. Link attached below.</i></p><p><a href='https://erp.turacoz.com/app/document-management-system/new-document-management-system-1' target='_blank'>https://erp.turacoz.com/app/document-management-system/new-document-management-system-1</a></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("DMS Alert for "+parent+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_duedate = today + timedelta(days=1)
							insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
				elif rec.frequency == "Weekly":
					getAlertDates = frappe.db.sql("""select name,parent,day,description,allocate_to,allocate_to_name,process_type from `tabWeekly Child DMS` 
						where parent = '{0}'
						and day = '{1}';""".format(parent,weekdays), as_dict = True)
					
					if getAlertDates:
						for rec1 in getAlertDates:
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly upload the respective data i.e. ("+rec1.description+") in ERP DMS on time. Link attached below.</i></p><p><a href='https://erp.turacoz.com/app/document-management-system/new-document-management-system-1' target='_blank'>https://erp.turacoz.com/app/document-management-system/new-document-management-system-1</a></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("DMS Alert for "+parent+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_duedate = today + timedelta(days=1)
							insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
				elif rec.frequency == "Daily":
					getAlertDates = frappe.db.sql("""select name,parent,description,allocate_to,allocate_to_name,process_type from `tabDaily Child DMS` 
						where parent = '{0}';""".format(parent), as_dict = True)
					
					if getAlertDates:
						for rec1 in getAlertDates:
							if not (weekdays=='Saturday' or weekdays=='Sunday'):
#								recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
#								message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly upload the respective data i.e. ("+rec1.description+") in ERP DMS on time. Link attached below.</i></p><p><a href='https://erp.turacoz.com/app/document-management-system/new-document-management-system-1' target='_blank'>https://erp.turacoz.com/app/document-management-system/new-document-management-system-1</a></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
#								frappe.sendmail(recipients=recepent,
#								subject=_("DMS Alert for "+parent+" for "+rec1.allocate_to_name),
#								message = message,
#								)
								todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
								dt_duedate = today + timedelta(days=1)
								insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
			elif rec.alert_type == "Compliance":
    # owner = rec.owner
				employee_name = rec.employee_name
				frequency = rec.frequency
				parent = rec.name
    # todo_name = str(parent)+'-'+str(owner)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
				reference_type = 'DMS ALERT SYSTEM'
				description = rec.description
				if rec.time:
					time = rec.time
				else:
					time = ''	
				
				if rec.frequency == "Monthly":	
					getAlertDates = frappe.db.sql("""select name,parent,month_date,description,idx,process_type,allocate_to,allocate_to_name from `tabMonth Child DMS` where parent = '{1}' and month_date='{0}';""".format(current_day,parent), as_dict = True)
					
					if getAlertDates:
						desc=''
						id1=''
						for rec1 in getAlertDates:
							desc = rec1.description
							id1 = rec1.process_type
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly complete your compliance i.e. ("+rec1.description+") on time.No pendency of this task will be entertained.</i></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("Compliance Email Alert for "+rec1.description+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_due = frappe.db.sql("""select name,parent,month_date,description,process_type from `tabMonth Child DMS` where description ='{0}' and process_type = 'Deadline Today'""".format(rec1.description),as_dict=True)
							dt=''
							for rec2 in dt_due:
								dt = str(today.year)+'-'+str(today.month)+'-'+str(rec2.month_date)	
							dt_duedate = datetime.datetime.strptime(dt,"%Y-%m-%d")
							if id1 == 'Create Task':
								insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
				elif rec.frequency == "Quarterly":
					getAlertDates = frappe.db.sql("""select name,parent,month,day,description,idx,process_type,allocate_to,allocate_to_name from `tabQuarterly DMS` where parent = '{2}' and month = '{0}' and day='{1}';""".format(current_month,current_day,parent), as_dict = True)
					
					if getAlertDates:
						desc=''
						id1=''
						for rec1 in getAlertDates:
							desc = rec1.description
							id1 = rec1.process_type
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly complete your compliance i.e. ("+rec1.description+") on time.No pendency of this task will be entertained.</i></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("Compliance Email Alert for "+rec1.description+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_due = frappe.db.sql("""select name,parent,month,day,description,process_type from `tabQuarterly DMS` where description ='{0}' and process_type = 'Deadline Today'""".format(rec1.description),as_dict=True)
							dt=''
							for rec2 in dt_due:
								dt = str(today.year)+'-'+str(rec2.month)+'-'+str(rec2.day)	
							dt_duedate = datetime.datetime.strptime(dt,"%Y-%m-%d")
							if id1 == 'Create Task':
								insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
					
				elif rec.frequency == "Half Yearly":
					getAlertDates = frappe.db.sql("""select name,parent,month,day,description,idx,process_type,allocate_to,allocate_to_name from `tabQuarterly DMS` 
						where parent = '{2}' 
						and month = '{0}' 
						and day='{1}';""".format(current_month,current_day,parent), as_dict = True)
					
					if getAlertDates:
						desc=''
						id1=''
						for rec1 in getAlertDates:
							desc = rec1.description
							id1 = rec1.process_type
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly complete your compliance i.e. ("+rec1.description+") on time.No pendency of this task will be entertained.</i></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("Compliance Email Alert for "+rec1.description+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_due = frappe.db.sql("""select name,parent,month,day,description,process_type from `tabQuarterly DMS` where description ='{0}' and process_type = 'Deadline Today'""".format(rec1.description),as_dict=True)
							dt=''
							for rec2 in dt_due:
								dt = str(today.year)+'-'+str(rec2.month)+'-'+str(rec2.day)	
							dt_duedate = datetime.datetime.strptime(dt,"%Y-%m-%d")
							if id1 == 'Create Task':
								insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
				elif rec.frequency == "Yearly":
					getAlertDates = frappe.db.sql("""select name,parent,month,day,description,idx,process_type,allocate_to,allocate_to_name from `tabQuarterly DMS` where parent = '{2}' and month = '{0}' and day='{1}';""".format(current_month,current_day,parent), as_dict = True)
					
					if getAlertDates:
						desc=''
						id1=''
						for rec1 in getAlertDates:
							desc = rec1.description
							id1 = rec1.process_type
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly complete your compliance i.e. ("+rec1.description+") on time.No pendency of this task will be entertained.</i></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("Compliance Email Alert for "+rec1.description+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_due = frappe.db.sql("""select name,parent,month,day,description,process_type from `tabQuarterly DMS` where description ='{0}' and process_type = 'Deadline Today'""".format(rec1.description),as_dict=True)
							dt=''
							for rec2 in dt_due:
								dt = str(today.year)+'-'+str(rec2.month)+'-'+str(rec2.day)	
							dt_duedate = datetime.datetime.strptime(dt,"%Y-%m-%d")
							if id1 == 'Create Task':
								insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
									
				elif rec.frequency == "Weekly":
					getAlertDates = frappe.db.sql("""select name,parent,day,description,idx,process_type,allocate_to,allocate_to_name from `tabWeekly Child DMS` 
						where parent = '{0}'
						and day = '{1}';""".format(parent,weekdays), as_dict = True)
					
					if getAlertDates:
						desc=''
						id1=''
						for rec1 in getAlertDates:
							desc = rec1.description
							id1 = rec1.process_type
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly complete your compliance i.e. ("+rec1.description+") on time.No pendency of this task will be entertained.</i></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("Compliance Email Alert for "+rec1.description+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_duedate = today + timedelta(days=3)
							if id1 == 'Create Task':
								insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
			elif rec.alert_type == "Auto Task With Reminder":
    # owner = rec.owner
				employee_name = rec.employee_name
				frequency = rec.frequency
				parent = rec.name
    # todo_name = str(parent)+'-'+str(owner)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
				reference_type = 'DMS ALERT SYSTEM'
				description = rec.description
				if rec.time:
					time = rec.time
				else:
					time = ''	
				
				if rec.frequency == "Monthly":	
					getAlertDates = frappe.db.sql("""select name,parent,month_date,description,idx,process_type,allocate_to,allocate_to_name from `tabMonth Child DMS` 
						where parent = '{1}'
						and month_date='{0}';""".format(current_day,parent), as_dict = True)
					
					if getAlertDates:
						desc=''
						id1=''
						for rec1 in getAlertDates:
							desc = rec1.description
							id1 = rec1.process_type
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly complete your task i.e. ("+rec1.description+") on time.No pendency of this task will be entertained.</i></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("Task Email Alert for "+rec1.description+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_due = frappe.db.sql("""select name,parent,month_date,description,process_type from `tabMonth Child DMS` where description ='{0}' and process_type = 'Deadline Today'""".format(rec1.description),as_dict=True)
							dt=''
							for rec2 in dt_due:
								dt = str(today.year)+'-'+str(today.month)+'-'+str(rec2.month_date)	
							dt_duedate = datetime.datetime.strptime(dt,"%Y-%m-%d")
							if id1 == 'Create Task':
								insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
				elif rec.frequency == "Quarterly":
					getAlertDates = frappe.db.sql("""select name,parent,month,day,description,idx,process_type,allocate_to,allocate_to_name from `tabQuarterly DMS` 
						where parent = '{2}' 
						and month = '{0}' 
						and day='{1}';""".format(current_month,current_day,parent), as_dict = True)
					
					if getAlertDates:
						desc=''
						id1=''
						for rec1 in getAlertDates:
							desc = rec1.description
							id1 = rec1.process_type
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly complete your task i.e. ("+rec1.description+") on time.No pendency of this task will be entertained.</i></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("Task Email Alert for "+rec1.description+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_due = frappe.db.sql("""select name,parent,month,day,description,process_type from `tabQuarterly DMS` where description ='{0}' and process_type = 'Deadline Today'""".format(rec1.description),as_dict=True)
							dt=''
							for rec2 in dt_due:
								dt = str(today.year)+'-'+str(rec2.month)+'-'+str(rec2.day)	
							dt_duedate = datetime.datetime.strptime(dt,"%Y-%m-%d")
							if id1 == 'Create Task':
								insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
					
				elif rec.frequency == "Half Yearly":
					getAlertDates = frappe.db.sql("""select name,parent,month,day,description,idx,process_type,allocate_to,allocate_to_name from `tabQuarterly DMS` 
						where parent = '{2}' 
						and month = '{0}' 
						and day='{1}';""".format(current_month,current_day,parent), as_dict = True)
					
					if getAlertDates:
						desc=''
						id1=''
						for rec1 in getAlertDates:
							desc = rec1.description
							id1 = rec1.process_type
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly complete your task i.e. ("+rec1.description+") on time.No pendency of this task will be entertained.</i></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("Task Email Alert for "+rec1.description+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_due = frappe.db.sql("""select name,parent,month,day,description,process_type from `tabQuarterly DMS` where description ='{0}' and process_type = 'Deadline Today'""".format(rec1.description),as_dict=True)
							dt=''
							for rec2 in dt_due:
								dt = str(today.year)+'-'+str(rec2.month)+'-'+str(rec2.day)	
							dt_duedate = datetime.datetime.strptime(dt,"%Y-%m-%d")
							if id1 == 'Create Task':
								insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
				elif rec.frequency == "Yearly":
					getAlertDates = frappe.db.sql("""select name,parent,month,day,description,idx,process_type,allocate_to,allocate_to_name from `tabQuarterly DMS` 
						where parent = '{2}' 
						and month = '{0}' 
						and day='{1}';""".format(current_month,current_day,parent), as_dict = True)
					
					if getAlertDates:
						desc=''
						id1=''
						for rec1 in getAlertDates:
							desc = rec1.description
							id1 = rec1.process_type
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly complete your task i.e. ("+rec1.description+") on time.No pendency of this task will be entertained.</i></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("Task Email Alert for "+rec1.description+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_due = frappe.db.sql("""select name,parent,month,day,description,process_type from `tabQuarterly DMS` where description ='{0}' and process_type = 'Deadline Today'""".format(rec1.description),as_dict=True)
							dt=''
							for rec2 in dt_due:
								dt = str(today.year)+'-'+str(rec2.month)+'-'+str(rec2.day)	
							dt_duedate = datetime.datetime.strptime(dt,"%Y-%m-%d")
							if id1 == 'Create Task':
								insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
									
				elif rec.frequency == "Weekly":
					getAlertDates = frappe.db.sql("""select name,parent,day,description,idx,process_type,allocate_to,allocate_to_name from `tabWeekly Child DMS` 
						where parent = '{0}'
						and day = '{1}';""".format(parent,weekdays), as_dict = True)
					
					if getAlertDates:
						desc=''
						id1=''
						for rec1 in getAlertDates:
							desc = rec1.description
							id1 = rec1.process_type
							recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
							message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly complete your task i.e. ("+rec1.description+") on time.No pendency of this task will be entertained.</i></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
							frappe.sendmail(recipients=recepent,
							subject=_("Task Email Alert for "+rec1.description+" for "+rec1.allocate_to_name),
							message = message,
							)
							todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
							dt_duedate = today + timedelta(days=3)
							if id1 == 'Create Task':
								insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
				elif rec.frequency == "Daily":
					getAlertDates = frappe.db.sql("""select name,parent,description,allocate_to,allocate_to_name,process_type from `tabDaily Child DMS` 
						where parent = '{0}';""".format(parent), as_dict = True)
					
					if getAlertDates:
						for rec1 in getAlertDates:
							if not (weekdays=='Saturday' or weekdays=='Sunday'):
#								recepent = [rec1.allocate_to,'rakeshtripathi@turacoz.com','atul.teotia@turacoz.com']
#								message = "<p style='background-color:#D3D3D3;'><i><b>Dear "+ rec1.allocate_to_name +",</b></i></p><p><i>As per the details given by you and subject line, Kindly upload the respective data i.e. ("+rec1.description+") in ERP DMS on time. Link attached below.</i></p><p><a href='https://erp.turacoz.com/app/document-management-system/new-document-management-system-1' target='_blank'>https://erp.turacoz.com/app/document-management-system/new-document-management-system-1</a></p><p style='background-color:#D3D3D3;'><b>Thanks & Regards,</b></p><b><span style='background-color:#D3D3D3;'>Turacoz Group</span></b>"	
#								frappe.sendmail(recipients=recepent,
#								subject=_("Task Email Alert for "+ec1.description+" for "+rec1.allocate_to_name),
#								message = message,
#								)
								todo_name = str(parent)+'-'+str(rec1.allocate_to)+'-'+str(today.year)+'-'+str(today.month)+'-'+str(today.day)
								dt_duedate = today + timedelta(days=1)
								if id1 == 'Create Task':
									insert_todo(rec1.allocate_to,todo_name,rec1.description,today,reference_type,rec1.allocate_to_name,parent,dt_duedate)
			
def insert_todo(owner,todo_name,description,today,reference_type,employee_name,parent,dt_duedate):
	todo_name = todo_name
	creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	modified = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	allocated_by = frappe.session.user
	allocated_to = owner
	allocated_by_name = frappe.session.user
	allocated_to_name = employee_name
	status = 'Open'
	priority = 'High'
	start_date = today
	description = description
	reference_type = reference_type
	reference_name = parent
	hours = 1
 # due_date = today + timedelta(days=1)
	due_date = dt_duedate
	data = frappe.db.sql("""select count(*) as cnt from `tabToDo` where name = '{0}';""".format(todo_name), as_dict = True)
	cnt = data[0]['cnt']
	if cnt == 0:
		data1 = frappe.db.sql("""insert into `tabToDo`(name,creation,modified,
								modified_by,owner,status,
								priority,start_date,date,
								description,reference_type,
								reference_name,assigned_by,
								assigned_by_full_name,
								allocated_to_full_name,hours,allocated_to) values('{0}','{1}','{2}',
								'{3}','{4}','{5}','{6}','{7}','{8}',
								'{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}');""".format(todo_name,creation,modified,allocated_by,allocated_to,status,
												priority,start_date,due_date,description,
												reference_type,reference_name,allocated_by,allocated_by_name,
												allocated_to_name,hours,allocated_to))	
	else:
		modified_by = frappe.session.user
		data1 = frappe.db.sql("""Update `tabToDo` set status='{1}',modified_by='{2}' where name='{0}';""".format(todo_name,status,modified_by))
			
	
	
	
