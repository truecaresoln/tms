// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Freelancer Alignment Report"] = {
	"filters": [
	
		{
			"fieldname": "freelancer",
			"label": __("Freelancer"),
			"fieldtype": "Link",
			"options": "Freelancer"
		},
		{
			"fieldname": "task_status",
			"label": __("Task Status"),
			"fieldtype": "Select",
			"options": ['Open','Close','Cancelled','All'],
			"default": "Open",
			"reqd": 1
		},


	]
};

function consoleerp_hi(freelance_project_table_id,project,start_date,end_date,status,actual_close_date) {
	
	var d = new frappe.ui.Dialog({
	    'fields': [
		{'fieldname': 'proje_id', 'fieldtype': 'Int', 'placeholder': 'Project Table ID'},
		{'fieldname': 'project', 'fieldtype': 'Data', 'label': 'Project','placeholder': 'Project'},
		{'fieldname': 'status', 'fieldtype': 'Select', 'placeholder': 'Status', 'label': 'Task Status', 'options':['Open','Close','Cancelled']},
		{'fieldname': 'start_date', 'fieldtype': 'Date', 'placeholder': 'Start Date', 'label': 'Align Start Date'},
		{'fieldname': 'end_date', 'fieldtype': 'Date', 'placeholder': 'End Date', 'label': 'Align End Date'},
		{'fieldname': 'actual_close_date', 'fieldtype': 'Date', 'placeholder': 'Actual Close Date', 'label': 'Actual Close Date'}
	    ],
	    primary_action: function(frm){
		d.hide();
		//show_alert(d.get_values());
		
	    }
	});
	if(start_date){
		s_date = start_date;
	}
	else{
		s_date = convert.ToDateTime('01-01-1900');
	}
	
	if(end_date){
		e_date = end_date;
	}
	else{
		e_date = '1900-01-01';
	}
	if(actual_close_date){
		ac_date = actual_close_date;
	}
	else{
		ac_date = '1900-01-01';
	}
	d.fields_dict.proje_id.set_value(freelance_project_table_id);
	d.fields_dict.project.set_value(project);	
	d.fields_dict.status.set_value(status);
	d.fields_dict.start_date.set_value(s_date);
	d.fields_dict.end_date.set_value(e_date);	
	d.fields_dict.actual_close_date.set_value(ac_date);	
	d.show();
	
	d.set_primary_action(__("Submit"), function() {
		var values = d.get_values();
		if(values.actual_close_date){
			var actual_close_date1 = values.actual_close_date;
		}
		else{
			var actual_close_date1 = '';
		}

	
		frappe.call({
				method: "tms.turacoz_management_system.report.freelancer_alignment_report.freelancer_alignment_report.update_planned",
				args:{ "proje_id":values.proje_id,"status":values.status,"actual_close_date":actual_close_date1
			},
			callback:function(res){
				let a = res.message; 
				if (a!=0){
					show_alert("Task Status Successfully Updated")
				}
				else{
					show_alert("Plan inserted for this task")
				}
			}
		})
	})
}	
