# Copyright (c) 2013, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe
from datetime import datetime
from datetime import timedelta
import calendar
import pendulum
import datetime



def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	chart = get_chart(filters)
	return columns, data, None, chart
# CONCAT('<button type=''button'' data=''', `tabToDo`.name ,''' onClick=''consoleerp_hi(this.getAttribute("data"))''>Button</button>') as "action"

def get_chart(filters):
	department = filters.get("department")
	team = filters.get("team")
	dt_range = filters.get("week")
	view_plan = filters.get("view_plan")
	
	if team:
		emp = " and owner = '%s'" %team
	else:
		emp = ""
		

	chart = {}
	label = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	datasets1 = []
	datasets2 = []
	
	today = pendulum.now()
	if dt_range == "Current":
		today = pendulum.now()
		start = today.start_of('week').date()	
		end = today.end_of('week').date()
	elif dt_range == "Next":
		today = pendulum.now()
		next = today + timedelta(days=7)
		start = next.start_of('week').date()
		end = next.end_of('week').date()
	elif dt_range == "Previous":
		today = pendulum.now()
		next = today - timedelta(days=7)
		start = next.start_of('week').date()	
		end = next.end_of('week').date()
	if view_plan==1:	
		for l in label:
			
			dt = frappe.db.sql("""select week_day,sum(estimated_hour_for_wee) tot,sum(spent_hour) tot_spent from `tabWeekly Estimated Plan` where date(week_date) between '{2}' and '{3}' and owner='{0}' and week_day='{1}' group by week_day;""".format(team,l,start,end), as_dict = True)		
			
			if dt:
				for d in dt:
	 				datasets1.append(d.tot)
	 				datasets2.append(d.tot_spent)
			else:
				datasets1.append(0)	
				datasets2.append(0)	
		
		chart = {
				"data": {
					'labels': label,
					'datasets': [{'name': 'Allocated Hours','values': datasets1},{'name': 'Spent Hours','values': datasets2}]
					}
		}
		chart["type"] = "bar"
		chart["colors"] = ["green","orange"]	
			
		return chart
		
def get_data(filters):
	department = filters.get("department")
	team = filters.get("team")
	status = filters.get("status")
	view_plan = filters.get("view_plan")
	dt_range = filters.get("week")	
	user = ""
	data = []
	if view_plan==1:
		if team:
			emp = " and twep.employee_user_id = '%s'" %team
		else:
			emp = ""
			
		today = pendulum.now()
		if dt_range == "Current":
			today = pendulum.now()
			start = today.start_of('week').date()	
			end = today.end_of('week').date()
		elif dt_range == "Next":
			today = pendulum.now()
			next = today + timedelta(days=7)
			start = next.start_of('week').date()
			end = next.end_of('week').date()
		elif dt_range == "Previous":
			today = pendulum.now()
			next = today - timedelta(days=7)
			start = next.start_of('week').date()	
			end = next.end_of('week').date()
		if not user: user = frappe.session.user
		if "System Manager" in frappe.get_roles(user) or "Project Management Associate" in frappe.get_roles(user):		
			data1 = frappe.db.sql("""select ttd.name,ttd.owner,twep.todo_id,ttd.description,ttd.allocated_to_full_name as full_name,
				twep.estimated_hour_for_wee,twep.week_day,twep.week_date,ttd.project,ttd.priority,
				ttd.status,twep.spent_hour,twep.employee_user_id,tp.project_current_status,ttd.date as due_date,tp.manager_name,twep.description 
				from `tabUser` tue
				left join `tabWeekly Estimated Plan` twep on tue.email = twep.employee_user_id
				left join `tabToDo` ttd on twep.todo_id = ttd.todo_id
				left join `tabProject` tp on ttd.project = tp.name
				where ttd.status not in ('Cancelled','Disable') and tue.department ='{0}' and twep.week_date between '{2}' and '{3}' {1} order by tue.full_name,twep.week_day;""".format(department,emp,start,end), as_dict = True)
		else:
			data1 = frappe.db.sql("""select ttd.name,ttd.owner,twep.todo_id,ttd.description,ttd.allocated_to_full_name as full_name,
				twep.estimated_hour_for_wee,twep.week_day,twep.week_date,ttd.project,ttd.priority,
				ttd.status,twep.spent_hour,twep.employee_user_id,tp.project_current_status,ttd.date as due_date,tp.manager_name,twep.description 
				from `tabUser` tue
				left join `tabWeekly Estimated Plan` twep on tue.email = twep.employee_user_id
				left join `tabToDo` ttd on twep.todo_id = ttd.todo_id
				left join `tabProject` tp on ttd.project = tp.name
				where ttd.status not in ('Cancelled','Disable') and tue.department ='{0}' and twep.week_date between '{2}' and '{3}' 
				and twep.employee_user_id in (select tu.name from `tabUser` tu where tu.enabled='1' and tu.reporting_manager='{1}' or name='{1}') order by tue.full_name,twep.week_day;""".format(department,user,start,end), as_dict = True)	
		
		spent_total_hrs = 0
		estimate_total_hrs = 0
		for rec in data1:
			row={}
			
			dataSpentHours = frappe.db.sql("""select sum(ttd.hours) spent_hours from `tabTimesheet` tt 
					left join `tabTimesheet Detail` ttd on tt.name = ttd.parent
					left join `tabToDo` tod on ttd.todo  = tod.name 
					where tt.start_date ='{0}' and tod.todo_id = '{1}'""".format(rec.week_date,rec.todo_id), as_dict=True)
			for recSpent in dataSpentHours:
				if recSpent.spent_hours is None:
					row['spent_hour'] = 0
					spent_total_hrs += 0
				else:
					row['spent_hour'] = recSpent.spent_hours
					spent_total_hrs += recSpent.spent_hours	
								
			row['name'] = rec.name
			row['employee_name'] = rec.full_name
			row['task_description'] = rec.description
			row['priority'] = rec.priority
			row['status'] = rec.status
			row["project_current_status"] = rec.project_current_status
			row['estimated_hour_for_week'] = rec.estimated_hour_for_wee
			estimate_total_hrs += rec.estimated_hour_for_wee
			row['project'] = rec.project
			row['week_date'] = rec.week_date
			row['week_day'] = rec.week_day
			row['project_manager'] = rec.manager_name
			row["description"] = rec.description
			row['action'] = '<button style=''color:white;background-color:red;'' type=''button'' onClick= ''delete_scheduled_plan("{0}","{1}","{2}")''>Delete</button>' .format(rec.todo_id,rec.week_date,rec.employee_user_id)
			
			data.append(row)
		if team:
			if data1:	
				row = {}
				row['employee_name'] = "Total Hours"
				row['spent_hour'] = spent_total_hrs
				row['estimated_hour_for_week'] = estimate_total_hrs
				data.append(row)
				row = {}
				data.append(row)
		
		
		return data
	else:
		if team:
			emp = " and ttd.owner = '%s'" %team
		else:
			emp = ""
		
		if status == "All":
			if not user: user = frappe.session.user
			if "System Manager" in frappe.get_roles(user) or "Project Management Associate" in frappe.get_roles(user):
				if department == 'Project Management - THS':
					data1 = frappe.db.sql("""select ttd.name,ttd.owner,ttd.todo_id,ttd.description,ttd.allocated_to_full_name as full_name,ttd.hours,
						ttd.project,ttd.priority,ttd.status, sum(td.hours) as spent_hours,tp.project_current_status,ttd.date as due_date,tp.manager_name
						from `tabUser` tue
						left join `tabToDo` ttd on tue.email = ttd.owner
						left join `tabTimesheet Detail` td on ttd.name = td.todo
						left join `tabProject` tp on ttd.project = tp.name
						where ttd.status not in('Cancelled','Disable') and tue.department ='{0}'
						and ttd.owner in (select tu.name from `tabUser` tu where tu.enabled='1' and tu.reporting_manager='{1}' or name='{1}')
						group by ttd.name order by tue.full_name;""".format(department,user), as_dict = True)	
				else:				
					data1 = frappe.db.sql("""select ttd.name,ttd.owner,ttd.todo_id,ttd.description,ttd.allocated_to_full_name as full_name,ttd.hours,
						ttd.project,ttd.priority,ttd.status, sum(td.hours) as spent_hours,tp.project_current_status,ttd.date as due_date,tp.manager_name
						from `tabUser` tue
						left join `tabToDo` ttd on tue.email = ttd.owner
						left join `tabTimesheet Detail` td on ttd.name = td.todo
						left join `tabProject` tp on ttd.project = tp.name
						where ttd.status not in('Cancelled','Disable') and tue.enabled='1' and tue.department ='{0}' {1} group by ttd.name order by tue.full_name;""".format(department,emp), as_dict = True)
			else:
				if emp=='':
					data1 = frappe.db.sql("""select ttd.name,ttd.owner,ttd.todo_id,ttd.description,ttd.allocated_to_full_name as full_name,ttd.hours,
						ttd.project,ttd.priority,ttd.status, sum(td.hours) as spent_hours,tp.project_current_status,ttd.date as due_date,tp.manager_name
						from `tabUser` tue
						left join `tabToDo` ttd on tue.email = ttd.owner
						left join `tabTimesheet Detail` td on ttd.name = td.todo
						left join `tabProject` tp on ttd.project = tp.name
						where ttd.status not in('Cancelled','Disable') and tue.department ='{0}'
						and ttd.owner in (select tu.name from `tabUser` tu where tu.enabled='1' and tu.reporting_manager='{1}' or name='{1}')
						group by ttd.name order by tue.full_name;""".format(department,user), as_dict = True)	
				else:
					data1 = frappe.db.sql("""select ttd.name,ttd.owner,ttd.todo_id,ttd.description,ttd.allocated_to_full_name as full_name,ttd.hours,
						ttd.project,ttd.priority,ttd.status, sum(td.hours) as spent_hours,tp.project_current_status,ttd.date as due_date,tp.manager_name
						from `tabUser` tue
						left join `tabToDo` ttd on tue.email = ttd.owner
						left join `tabTimesheet Detail` td on ttd.name = td.todo
						left join `tabProject` tp on ttd.project = tp.name
						where ttd.status not in('Cancelled','Disable') and tue.enabled='1' and tue.department ='{0}' {1} 
						group by ttd.name order by tue.full_name;""".format(department,emp), as_dict = True)
		else:
			if not user: user = frappe.session.user
			if "System Manager" in frappe.get_roles(user) or "Project Management Associate" in frappe.get_roles(user):
				if department == 'Project Management - THS':
					data1 = frappe.db.sql("""select ttd.name,ttd.owner,ttd.todo_id,ttd.description,ttd.allocated_to_full_name as full_name,ttd.hours,
						ttd.project,ttd.priority,ttd.status, sum(td.hours) as spent_hours,tp.project_current_status,ttd.date as due_date,tp.manager_name
						from `tabUser` tue
						left join `tabToDo` ttd on tue.email = ttd.owner
						left join `tabTimesheet Detail` td on ttd.name = td.todo
						left join `tabProject` tp on ttd.project = tp.name
						where ttd.status not in('Cancelled','Disable') and ttd.status='{2}' and tue.department ='{0}'
						and ttd.owner in (select tu.name from `tabUser` tu where tu.enabled='1' and tu.reporting_manager='{1}' or name='{1}')
						group by ttd.name order by tue.full_name;""".format(department,user,status), as_dict = True)	
				else:				
					data1 = frappe.db.sql("""select ttd.name,ttd.owner,ttd.todo_id,ttd.description,ttd.allocated_to_full_name as full_name,ttd.hours,
						ttd.project,ttd.priority,ttd.status, sum(td.hours) as spent_hours,tp.project_current_status,ttd.date as due_date,tp.manager_name
						from `tabUser` tue
						left join `tabToDo` ttd on tue.email = ttd.owner
						left join `tabTimesheet Detail` td on ttd.name = td.todo
						left join `tabProject` tp on ttd.project = tp.name
						where ttd.status not in('Cancelled','Disable') and tue.enabled='1' and ttd.status='{2}' and tue.department ='{0}' {1} 
						group by ttd.name order by tue.full_name;""".format(department,emp,status), as_dict = True)
			else:
				if emp=='':
					data1 = frappe.db.sql("""select ttd.name,ttd.owner,ttd.todo_id,ttd.description,ttd.allocated_to_full_name as full_name,ttd.hours,
						ttd.project,ttd.priority,ttd.status, sum(td.hours) as spent_hours,tp.project_current_status,ttd.date as due_date,tp.manager_name
						from `tabUser` tue
						left join `tabToDo` ttd on tue.email = ttd.owner
						left join `tabTimesheet Detail` td on ttd.name = td.todo
						left join `tabProject` tp on ttd.project = tp.name
						where ttd.status not in('Cancelled','Disable') and ttd.status='{2}' and tue.department ='{0}'
						and ttd.owner in (select tu.name from `tabUser` tu where tu.enabled='1' and tu.reporting_manager='{1}' or name='{1}')
						group by ttd.name order by tue.full_name;""".format(department,user,status), as_dict = True)	
				else:
					data1 = frappe.db.sql("""select ttd.name,ttd.owner,ttd.todo_id,ttd.description,ttd.allocated_to_full_name as full_name,ttd.hours,
						ttd.project,ttd.priority,ttd.status, sum(td.hours) as spent_hours,tp.project_current_status,ttd.date as due_date,tp.manager_name
						from `tabUser` tue
						left join `tabToDo` ttd on tue.email = ttd.owner
						left join `tabTimesheet Detail` td on ttd.name = td.todo
						left join `tabProject` tp on ttd.project = tp.name
						where ttd.status not in('Cancelled','Disable') and tue.enabled='1' and ttd.status='{2}' and tue.department ='{0}' {1} 
						group by ttd.name order by tue.full_name;""".format(department,emp,status), as_dict = True)

		for rec in data1:
			row={}
					
			row['name'] = rec.name
			row['owner'] = rec.owner
			row['employee_name'] = rec.full_name
			row['task_description'] = rec.description
			row['priority'] = rec.priority
			row['status'] = rec.status
			row["project_current_status"] = rec.project_current_status
			row['allocated_hours'] = rec.hours
			row['project'] = rec.project
			row['spent_hours'] = rec.spent_hours
			row['due_date'] = rec.due_date
			row['project_manager'] = rec.manager_name
			if rec.status=='Open' or rec.status=='Overdue':
				row['action'] = '<button style=''color:white;background-color:green;'' type=''button'' onClick= ''consoleerp_hi("{0}","{1}","{2}","{3}")''>Weekly Schedule</button>' .format(rec.owner,rec.todo_id,rec.priority,rec.status)
				row['comment'] = '<button style=''color:white;background-color:blue;'' type=''button'' onClick= ''comment_fn("{0}")''>Comment</button>' .format(rec.todo_id)
			else:
				row['action'] = ''
				row['comment'] = ''
			
			data.append(row)
		
		return data
		

	
def get_columns(filters):
	view_plan = filters.get("view_plan")
	cols = []
	if view_plan==1:
		cols=[
			{
				"fieldname": "name",
				"label": ("Name"),
				"fieldtype": "Data",
				"width": "150",
				"hidden": "true"
			},
			{
				"fieldname": "employee_name",
				"label": ("Employee Name"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "task_description",
				"label": ("Task"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "project",
				"label": ("Project"),
				"fieldtype": "Link",
				"options": "Project",
				"width": "130"
			},
			{
				"fieldname": "priority",
				"label": ("Priority"),
				"fieldtype": "Data",
				"width": "70"
			},
			{
				"fieldname": "status",
				"label": ("Status"),
				"fieldtype": "Data",
				"width": "70"
			},
			{
				"fieldname": "project_current_status",
				"label": ("Project Current Status"),
				"fieldtype": "Data",
				"width": "80"
			},
			{
				"fieldname": "estimated_hour_for_week",
				"label": ("Estimated Hour"),
				"fieldtype": "Data",
				"width": "100"
			},
			{
				"fieldname": "spent_hour",
				"label": ("Spent Hour"),
				"fieldtype": "Data",
				"width": "70"
			},
			{
				"fieldname": "week_date",
				"label": ("Date"),
				"fieldtype": "Date",
				"width": "80"
			},
			{
				"fieldname": "week_day",
				"label": ("Week Day"),
				"fieldtype": "Data",
				"width": "80"
			},
			{
				"fieldname": "project_manager",
				"label": ("Manager Name"),
				"fieldtype": "Data",
				"width": "120"
			},
			{
				"fieldname": "description",
				"label": ("Description"),
				"fieldtype": "Small Text",
				"width": "200"
			},
			{
				"fieldname": "action",
				"label": ("Action"),
				"fieldtype": "Button",
				"width": "150"
			}
		]
		return cols
	else:
		cols = [
			{
				"fieldname": "name",
				"label": ("Name"),
				"fieldtype": "Data",
				"width": "150",
				"hidden": "true"
			},
			{
				"fieldname": "owner",
				"label": ("Owner"),
				"fieldtype": "Data",
				"width": "150",
				"hidden": "true"
			},
			{
				"fieldname": "employee_name",
				"label": ("Employee Name"),
				"fieldtype": "Data",
				"width": "150"
			},
			{
				"fieldname": "task_description",
				"label": ("Task"),
				"fieldtype": "Data",
				"width": "250"
			},
			{
				"fieldname": "project",
				"label": ("Project"),
				"fieldtype": "Link",
				"options": "Project",
				"width": "150"
			},
			{
				"fieldname": "priority",
				"label": ("Priority"),
				"fieldtype": "Data",
				"width": "70"
			},
			{
				"fieldname": "status",
				"label": ("Task Status"),
				"fieldtype": "Data",
				"width": "80"
			},
			{
				"fieldname": "project_current_status",
				"label": ("Project Current Status"),
				"fieldtype": "Data",
				"width": "80"
			},
			{
				"fieldname": "allocated_hours",
				"label": ("Allocated Hours"),
				"fieldtype": "Data",
				"width": "120"
			},
			{
				"fieldname": "spent_hours",
				"label": ("Spent Hours"),
				"fieldtype": "Data",
				"width": "80"
			},
			{
				"fieldname": "due_date",
				"label": ("Due Date"),
				"fieldtype": "Date",
				"width": "80"
			},
			{
				"fieldname": "project_manager",
				"label": ("Manager Name"),
				"fieldtype": "Data",
				"width": "120"
			},
			{
				"fieldname": "action",
				"label": ("Action"),
				"fieldtype": "Button",
				"width": "150"
			},
			{
				"fieldname": "comment",
				"label": ("Comment"),
				"fieldtype": "Button",
				"width": "150"
			}
		]	
		return cols 

@frappe.whitelist()
def submit_week_planned(todo_id,priority,status,week_date,estimated_hour_day,user_id,description):
	
	modified_by = frappe.session.user
	owner = user_id
	todo_id = todo_id
	week_date = week_date
	estimated_hour_for_week = estimated_hour_day
	creation_date = datetime.datetime.today().strftime('%Y-%m-%d')
	employee_user_id = user_id
	priority = priority
	status = status
	description = description
	
	creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	modified = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	
	curr_date = datetime.datetime.strptime(week_date, '%Y-%m-%d')
	week_day = calendar.day_name[curr_date.weekday()]
	
	data = frappe.db.sql("""Select * from `tabToDo` where todo_id='{0}';""".format(todo_id), as_dict=True)
	for rec in data:
		todo_name = rec['name']
		task_description = rec['description']
		
		if(rec['project']):
			project = rec['project']
		else:
			project = ''	
		
		if(rec['role']):
			role = rec['role']
		else:
			role = ''
		
	data1 = frappe.db.sql("""Select * from `tabEmployee` where user_id='{0}';""".format(user_id), as_dict = True)
	for rec1 in data1:
		employee_name = rec1['employee_name']	
	pname = employee_name+'-'+todo_id+'-'+datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")
	
	data3 = frappe.db.sql("""Select * from `tabWeekly Estimated Plan` where todo_id='{0}' and week_date='{1}';""".format(todo_id,week_date),as_dict = True)
	if data3:
		data2 = frappe.db.sql("""Update `tabWeekly Estimated Plan` set estimated_hour_for_wee='{0}' where todo_id='{1}' and week_date='{2}';""".format(estimated_hour_for_week,todo_id,week_date))
		a = 1
	else:
		data2 = frappe.db.sql("""insert into `tabWeekly Estimated Plan`(modified_by, owner, todo_id, todo_name, task_description, 
			week_date, week_day, estimated_hour_for_wee, creation_date, employee_user_id, employee_name, project, priority, status, role, creation, modified,name,description)
		 	values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}')""".format(modified_by,owner,todo_id,todo_name,task_description,week_date,week_day,estimated_hour_for_week,creation_date,owner,employee_name,project,priority,status,role,creation,modified,pname,description))
		a = 0
	return a

@frappe.whitelist()
def delete_weekly_planned(todo_id,week_date,employee_user_id):
	if employee_user_id:
		if todo_id:
			if week_date:
				data = frappe.db.sql("""Delete from `tabWeekly Estimated Plan` where todo_id='{0}' and week_date='{1}' and employee_user_id='{2}';""".format(todo_id,week_date,employee_user_id))
				a = 1
			else:
				a=0
		else:
			a=0
	else:
		a=0
	
	return a

@frappe.whitelist()
def submit_comment(todo_id,comment):
	creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	modified = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	modified_by = frappe.session.user
	if todo_id:						
		data = frappe.db.sql("""Insert into `tabToDo Comments`(todo_id,comment,creation, modified, modified_by, owner) values('{0}','{1}','{2}','{3}','{4}','{5}')""".format(todo_id,comment,creation,modified,modified_by,modified_by))
		a = 1
	else:
		a = 0;
		
	return a

		
