// Copyright (c) 2016, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Weekly Planner"] = {
	"filters":[
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"reqd": 1,
			get_query: () => {
				var user = frappe.session.user;
				const options = {company_email: user};
				const fields = ['department'];	
				frappe.db.get_value('Employee', options, fields).then(({ message }) => {
				if (message) {
					frappe.query_report.set_filter_value("department", message.department);
					}
				});
			}
		},
		{
			"fieldname": "team",
			"label": __("Team"),
			"fieldtype": "Link",
			"options": "Teams",
			"reqd": 0,
			get_query: () => {
				var reporting_manager = frappe.session.user;
				var parent = frappe.query_report.get_filter_value('department');
				return {
					filters:{
						'department': parent,
						'status' : 'Active',
						'reporting_manager': reporting_manager
						}
				}
			}
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": ['All','Open','Closed','Overdue','Disable'],
			"default": "All",
			"reqd": 0
		},
		{
			"fieldname": "week",
			"label": __("Week"),
			"fieldtype": "Select",
			"options": ['Previous','Current','Next'],
			"default": "Current",
			"reqd": 0
		},
		{
			"fieldname": "view_plan",
			"label": __("View Weekly Plan"),
			"fieldtype": "Check",
			"default": 0,
			"reqd": 0
		},
	],
	
	"formatter":function (value, row, column, data, default_formatter) {
		value = default_formatter(value,row,column,data);
	   /*if (column.id == 'challenge_status' && data.challenge_status == 'Active') {
		value = "<b style='color:green;'>" + value + "</b>";
	   }*/
		let today = new Date().toISOString().slice(0, 10)
		//let today = new Date().toISOString().replace(/T.*/,'').split('-').reverse().join('-')
	
		if (column.id =='status' && data.status=='Open') {
			value = "<b style='color:red;'>" + value + "</b>";
	   	}
	   	if (column.id =='status' && data.status=='Closed') {
			value = "<b style='color:green;'>" + value + "</b>";
	   	}
	   	if (column.id =='status' && data.status=='Disable') {
			value = "<b style='color:gray;'>" + value + "</b>";
	   	}
	   	
	   	if (column.id =='status' && data.status=='Overdue') {
			value = "<b style='color:red;'>" + value + "</b>";
	   	}		
			
	
	   return value;
	}
};

function consoleerp_hi(userid,todo_id,priority,status) {
	
	var d = new frappe.ui.Dialog({
	    'fields': [
		{'fieldname': 'todo_id', 'fieldtype': 'Int', 'placeholder': 'ToDo ID', 'hidden': 1},
		{'fieldname': 'user_id', 'fieldtype': 'Data', 'label': 'User ID','placeholder': 'User ID', 'hidden': 1},
		{'fieldname': 'priority', 'fieldtype': 'Select', 'placeholder': 'Priority', 'label': 'Priority', 'options':['High','Medium','Low']},
		{'fieldname': 'status', 'fieldtype': 'Select', 'placeholder': 'Status', 'label': 'Status', 'options':['Open','Closed','Cancelled','Overdue','Disable']},
		{'fieldname': 'week_date', 'fieldtype': 'Date', 'label': 'Select Week Date','placeholder': 'Week'},
		{'fieldname': 'estimated_hour_day', 'fieldtype': 'Float', 'label': 'Estimated Hour for the Day','placeholder': 'Estimated Hour'},
		{'fieldname': 'description', 'fieldtype': 'Small Text', 'label': 'Description','placeholder': 'Description'}
	    ],
	    primary_action: function(frm){
		d.hide();
		//show_alert(d.get_values());
		
	    }
	});
	d.fields_dict.todo_id.set_value(todo_id);
	d.fields_dict.user_id.set_value(userid);	
	d.fields_dict.priority.set_value(priority);
	d.fields_dict.status.set_value(status);	
	d.show();
	
	d.set_primary_action(__("Submit"), function() {
		var values = d.get_values();
		if(values.week_date){
			var week_date1 = values.week_date;
		}
		else{
			var week_date1 = '';
		}

		if(values.estimated_hour_day){
			var estimated_hour_day1 = values.estimated_hour_day;
		}
		else{
			var estimated_hour_day1 = '';
		}
		
		if(values.description){
			var des = values.description
		}
		else{
			var des = '';
		}
		
		frappe.call({
				method: "tms.turacoz_management_system.report.weekly_planner.weekly_planner.submit_week_planned",
				args:{ "todo_id":values.todo_id,"priority":values.priority,"status":values.status,"week_date":week_date1,"estimated_hour_day":estimated_hour_day1,"user_id":values.user_id,"description":des
			},
			callback:function(res){
				let a = res.message; 
				if (a!=0){
					show_alert("Plan updated for this task")
				}
				else{
					show_alert("Plan inserted for this task")
				}
			}
		})
	})	
	
}

function delete_scheduled_plan(todo_id,week_date,employee_user_id){
	
	frappe.call({
				method: "tms.turacoz_management_system.report.weekly_planner.weekly_planner.delete_weekly_planned",
				args:{ "todo_id":todo_id,"week_date":week_date,"employee_user_id":employee_user_id
			},
			callback:function(res){
				let a = res.message; 
				if (a!=0){
					show_alert("This Plan Deleted")
					frappe.query_report.refresh();	
				}
				else{
					show_alert("Oops something went wrong, Try again!")
				}
			}
		})
}

function comment_fn(todo_id){
	var d = new frappe.ui.Dialog({
	    'fields': [
		{'fieldname': 'todo_id', 'fieldtype': 'Int', 'placeholder': 'ToDo ID', 'hidden': 1},
		{'fieldname': 'comment', 'fieldtype': 'Small Text', 'label': 'Comment','placeholder': 'Comment'}
	    ],
	    primary_action: function(frm){
		d.hide();
		//show_alert(d.get_values());
		
	    }
	});
	d.fields_dict.todo_id.set_value(todo_id);
	d.show();
	
	d.set_primary_action(__("Save"), function() {
		var values = d.get_values();
				
		if(values.comment){
			var comm = values.comment
		}
		else{
			var comm = '';
		}
		
		frappe.call({
				method: "tms.turacoz_management_system.report.weekly_planner.weekly_planner.submit_comment",
				args:{ "todo_id":values.todo_id,"comment":comm
			},
			callback:function(res){
				let a = res.message; 
				if (a!=0){
					show_alert("Comment edited for this task")
				}
				else{
					show_alert("Comment edited for this task")
				}
			}
		})
	})	
}



