# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from frappe import _

app_name = "tms"
app_title = "Turacoz Management System"
app_publisher = "RSA"
app_description = "Management System"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "atul.teotia@tuarcoz.com"
app_license = "TMS"

permission_query_conditions = {
    "My Task Allocation": "tms.turacoz_management_system.doctype.my_task_allocation.my_task_allocation.get_permission_query_conditions",
    "Challenges": "tms.turacoz_management_system.doctype.challenges.challenges.get_permission_query_conditions",
    "Document Management": "tms.turacoz_management_system.doctype.document_management.document_management.get_permission_query_conditions",
    "Document Management System": "tms.turacoz_management_system.doctype.document_management_system.document_management_system.get_permission_query_conditions",
    "Challenges and Commitments": "tms.turacoz_management_system.doctype.challenges_and_commitments.challenges_and_commitments.get_permission_query_conditions",
    "Employee Salary Slip": "tms.turacoz_management_system.doctype.employee_salary_slip.employee_salary_slip.get_permission_query_conditions",
    "Ticket Queries and Feedback": "tms.turacoz_management_system.doctype.ticket_queries_and_feedback.ticket_queries_and_feedback.get_permission_query_conditions",
    "Approvals": "tms.turacoz_management_system.doctype.approvals.approvals.get_permission_query_conditions"     
}

has_permission = {
    "My Task Allocation": "tms.turacoz_management_system.doctype.my_task_allocation.my_task_allocation.has_permission",
    "Challenges": "tms.turacoz_management_system.doctype.challenges.challenges.has_permission",
    "Document Management": "tms.turacoz_management_system.doctype.document_management.document_management.has_permission",
    "Document Management System": "tms.turacoz_management_system.doctype.document_management_system.document_management_system.has_permission",
    "Challenges and Commitments": "tms.turacoz_management_system.doctype.challenges_and_commitments.challenges_and_commitments.has_permission",
    "Employee Salary Slip": "tms.turacoz_management_system.doctype.employee_salary_slip.employee_salary_slip.has_permission",
    "Ticket Queries and Feedback": "tms.turacoz_management_system.doctype.ticket_queries_and_feedback.ticket_queries_and_feedback.has_permission",
    "Approvals": "tms.turacoz_management_system.doctype.approvals.approvals.has_permission"
}

doctype_js = {
    "Service Types": "public/js/custom.js",
}#direct me to the js

doc_events = {
     "Project Detail Template": {
         "on_update_after_submit": ["tms.turacoz_management_system.doctype.project_detail_template.project_detail_template.update_project_coordinators","tms.turacoz_management_system.doctype.project_detail_template.project_detail_template.update_coordinators_in_project"],
    },
    "Team Alignment": {
         "on_update_after_submit": ["tms.turacoz_management_system.doctype.team_alignment.team_alignment.todo_after_update","tms.turacoz_management_system.doctype.team_alignment.team_alignment.after_update_freelancer"],
    },
    "Training Data": {
        "on_update_after_submit": ["tms.turacoz_management_system.doctype.training_data.training_data.update_amount_inr"],
    },
    "Published Articles":{
        "on_update_after_submit": ["tms.turacoz_management_system.doctype.published_articles.published_articles.after_update_status"],
    },
    "My Task Allocation":{
        "on_update_after_submit": ["tms.turacoz_management_system.doctype.my_task_allocation.my_task_allocation.update_todo_status"],
    },
    "Project New Update":{
        "on_update_after_submit": ["tms.turacoz_management_system.doctype.project_new_update.project_new_update.wrap_up_call_alert"],
    },
    "Employee Resignation":{
        "on_update_after_submit": ["tms.turacoz_management_system.doctype.employee_resignation.employee_resignation.update_employee_resignation_date","tms.turacoz_management_system.doctype.employee_resignation.employee_resignation.update_employee_relieving_date"],
    },
    "Recruitment":{
        "on_update_after_submit": ["tms.turacoz_management_system.doctype.recruitment.recruitment.send_credentials_notification"],
    },
    "Document Management System":{
        "on_submit": ["tms.turacoz_management_system.doctype.document_management_system.document_management_system.update_todo_status"],
    },
 }

scheduler_events = {
"cron": {        
        "7 10 * * * 44": [
            "tms.turacoz_management_system.doctype.bd_monthly_business.bd_monthly_business.validate_bd_monthly_business"
        ],
        "0 8 * * *":[
		"tms.turacoz_management_system.doctype.dms_alert_system.dms_alert_system.send_alert"
	],
    },
    "daily": [
        "tms.turacoz_management_system.doctype.currency_exchange_rate.currency_exchange_rate.currency_exchange_rate",
        "tms.turacoz_management_system.doctype.my_task_allocation.my_task_allocation.status_overdue_alert"
    ]
}
