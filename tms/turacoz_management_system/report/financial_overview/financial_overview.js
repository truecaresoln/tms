// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Financial Overview"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": dateutil.month_start(),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": dateutil.month_end(),
			"reqd": 1
		},
		{
			"fieldname":"overview_status",
			"label": __("Overview Status"),
			"fieldtype": "Select",
			"options": ['New Projects This Month','Expected Payments','Invoice to be Raised','Received Payment'],
			"default": "New Projects This Month",
			"reqd": 0
		},
		{
			"fieldname":"detailed_view",
			"label": __("Detailed View PM Wise"),
			"fieldtype": "Check",
			"default": 1,
			"reqd": 0
		},
		{
			"fieldname":"excluding_viatris",
			"label": __("Including/Excluding Viatris"),
			"fieldtype": "Check",
			"default": 1,
			"reqd": 0
		},
	]
};

function comment_fn(user,month,year){
	var d = new frappe.ui.Dialog({
	    'fields': [
		{'fieldname': 'userid', 'label': 'User ID', 'fieldtype': 'Link', 'options': 'User','placeholder': 'User ID'},
		{'fieldname': 'month', 'fieldtype': 'Data', 'label': 'Month', 'placeholder': 'Month','required': '1'},
		{'fieldname': 'year', 'fieldtype': 'Data','label': 'Year', 'placeholder': 'Year'},
		{'fieldname': 'fortype', 'fieldtype': 'Select','label': 'For Type', 'placeholder': 'For Type', 'options':['', 'New Projects This Month','Invoice to be Raised','Expected Payments','Received Payment'], 'required':'1'},
		{'fieldname': 'comment', 'fieldtype': 'Small Text', 'label': 'Comment','placeholder': 'Comment'}
	    ],
	    primary_action: function(frm){
		d.hide();
		//show_alert(d.get_values());
		
	    }
	});
	d.fields_dict.userid.set_value(user);
	d.fields_dict.month.set_value(month);
	d.fields_dict.year.set_value(year);
	d.show();
	
	d.set_primary_action(__("Save"), function() {
		var values = d.get_values();
		if(values.comment){
			var comm = values.comment
		}
		else{
			var comm = '';
		}
		if(values.userid){
			var userid = values.userid
		}
		else{
			var userid = '';
		}
		if(values.month){
			var month = values.month
		}
		else{
			var month = '';
		}
		if(values.year){
			var year = values.year
		}
		else{
			var year = '';
		}
		if(values.fortype){
			var fortype = values.fortype
		}
		else{
			var fortype = '';
		}
		
		frappe.call({
				method: "tms.turacoz_management_system.report.financial_overview.financial_overview.submit_comment",
				args:{ "userid":userid,"comment":comm,"month":month,"year":year,"fortype":fortype
			},
			callback:function(res){
				let a = res.message; 
				if (a!=0){
					show_alert("Comment Added Successfully")
				}
				else{
					show_alert("Comment Added Successfully")
				}
			}
		})
				
	})	
}

function get_comment_fn(comment_id){
	frappe.call({
			method: "tms.turacoz_management_system.report.financial_overview.financial_overview.get_comments",
			args:{ "comment_id":comment_id
			},
			callback:function(res){
				let a = res.message; 
				
				var d = new frappe.ui.Dialog({
				    'fields': [
					{'fieldname': 'comment', 'fieldtype': 'Small Text', 'label': 'Comment','placeholder': 'Comment', 'read_only':'1'}
				    ],
				    primary_action: function(frm){
					d.hide();
					//show_alert(d.get_values());
					
				    }
				});
				d.fields_dict.comment.set_value(a);
				d.show();
				
				d.set_primary_action(__("Close"), function() {
					var values = d.hide();
							
				})
				
			}
		})
}

function get_data(month_name,year,type,excluding_viatris)
{	
	frappe.call({
			method: "tms.turacoz_management_system.report.financial_overview.financial_overview.get_finance_data",
			args:{ "month_name":month_name, "year":year, "type":type, "excluding_viatris":excluding_viatris
			},
			callback:function(res){
				let a = res.message; 
				
				var d = new frappe.ui.Dialog({
				    'fields': [
					{'fieldname': 'ht', 'fieldtype': 'HTML'}
				    ],
				    primary_action: function(frm){
					d.hide();
					//show_alert(d.get_values());
					
				    }
				});
				d.fields_dict.ht.set_value(a);
				d.show();
				d.$wrapper.find('.modal-dialog').css("width","1000px");
				d.set_primary_action(__("Close"), function() {
					var values = d.hide();
										
				})
				
			}
		})
}




