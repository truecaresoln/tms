// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Exit Interview Checklist', {
	 onload: function(frm) {
	 
	 	var userid = frappe.session.user;
		if(frm.is_new()){
			if(userid != "Administrator"){
				frappe.call({
					method: "tms.turacoz_management_system.doctype.employee_handover_form.employee_handover_form.get_emp_id",
					args:{ "userid":userid
					},
					callback:function(res){						
						if(res){
							if(res.message[0]['name']){
								frm.set_value("employee_code", res.message[0]['name']);
							}
							if(res.message[0]['employee_name']){
								frm.set_value("employee_name", res.message[0]['employee_name']);
							}
							if(res.message[0]['designation']){
								frm.set_value("designation", res.message[0]['designation']);
							}
							if(res.message[0]['resignation_letter_date']){
								frm.set_value("date_of_resignation", res.message[0]['resignation_letter_date']);
							}
							if(res.message[0]['relieving_date']){
								frm.set_value("last_working_day", res.message[0]['relieving_date']);
							}
							if(res.message[0]['date_of_joining']){
								frm.set_value("date_of_joining", res.message[0]['date_of_joining']);
							}
							if(res.message[0]['reporting_to']){
								frm.set_value("reporting_manager", res.message[0]['reporting_to']);
							}
						}
					}
				})
			}
		}
		
		cur_frm.set_query("emp_code", function() {
			return {
				"filters": {
					"status": ("=", "Active")
				}
			};
		});
	 }
});
