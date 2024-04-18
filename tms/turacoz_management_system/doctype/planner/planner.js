// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Planner', {
	onload: function(frm) {
		if(frm.is_new()){
			var owner = frm.doc.owner;
			fetch_details_department(owner);
			fetch_details_designation(owner);
			cur_frm.set_value("owner", '');
			frm.toggle_display("department", false);
			frm.toggle_display("designation", false);
			frm.toggle_display("allocated_to_name", false);
		}
	},

	"owner":function(frm){
		var owner = frm.doc.owner;
		fetch_details_department(owner);
		fetch_details_designation(owner);
		frm.toggle_display("department", true);
		frm.toggle_display("designation", true);
		frm.toggle_display("allocated_to_name", true);
	},
	/*"frequency":function(frm){
		var frequency = frm.doc.frequency;
		if(frequency == 'Weekly'){
			frm.toggle_display("day", true);
			frm.set_df_property("day", "reqd", 1);	
		}
		else if(frequency == 'Monthly'){
			frm.toggle_display("day", false);
			frm.set_df_property("day", "reqd", 0);
			frm.toggle_display("start_date", true);
			frm.set_df_property("start_date", "reqd", 1);	
			frm.toggle_display("end_date", true);
			frm.set_df_property("end_date", "reqd", 1);		
		}
		else if(frequency == 'Quarterly'){
			frm.toggle_display("day", false);
			frm.set_df_property("day", "reqd", 0);
			frm.toggle_display("start_date", true);
			frm.set_df_property("start_date", "reqd", 1);	
			frm.toggle_display("end_date", true);
			frm.set_df_property("end_date", "reqd", 1);
		}
		else if(frequency == 'Yearly'){
			frm.toggle_display("day", false);
			frm.set_df_property("day", "reqd", 0);
			frm.toggle_display("start_date", true);
			frm.set_df_property("start_date", "reqd", 1);	
			frm.toggle_display("end_date", true);
			frm.set_df_property("end_date", "reqd", 1);
		}
		else if(frequency == 'Ad Hoc'){
			frm.toggle_display("day", false);
			frm.set_df_property("day", "reqd", 0);
			frm.toggle_display("start_date", true);
			frm.set_df_property("start_date", "reqd", 1);	
			frm.toggle_display("end_date", true);
			frm.set_df_property("end_date", "reqd", 1);
		}
	},*/
});

// set information hide and show section
const fetch_details_department = function(user_id) {
	frappe.call({
        	method: "tms.turacoz_management_system.doctype.planner.planner.fetch_details_department",
		args:{ 
			"userid":user_id
		},
		callback:function(res){
			cur_frm.set_value("department", res.message);
			cur_frm.toggle_display("department", true);
			cur_frm.toggle_display("allocated_to_name", true);
		}
        })

};

// set information hide and show section
const fetch_details_designation = function(user_id) {
	frappe.call({
        	method: "tms.turacoz_management_system.doctype.planner.planner.fetch_details_designation",
		args:{ 
			"userid":user_id
		},
		callback:function(res){
			cur_frm.set_value("designation", res.message);
			cur_frm.toggle_display("designation", true);
			cur_frm.toggle_display("allocated_to_name", true);
		}
        })

};
