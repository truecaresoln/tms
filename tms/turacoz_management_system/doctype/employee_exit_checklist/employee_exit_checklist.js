// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Exit Checklist', {
	 onload: function(frm) {
		var userid = frappe.session.user;
	 },
	 
	 "employee_code": function(frm){
	 	var user_id = frm.doc.employee_code;
	 		frappe.call({
				method: "tms.turacoz_management_system.doctype.employee_exit_checklist.employee_exit_checklist.get_emp_id",
				args:{ "userid":user_id
				},
				callback:function(res){
					if(res.message[0]['employee_name']){
						frm.set_value("employee_name", res.message[0]['employee_name']);
					}
					
					if(res.message[0]['designation']){
						frm.set_value("designation", res.message[0]['designation']);
					}
					
					if(res.message[0]['department_name']){
						frm.set_value("department", res.message[0]['department_name']);
					}
					
					if(res.message[0]['reporting_to']){
						frm.set_value("reporting_to", res.message[0]['reporting_to']);
					}
					
					if(res.message[0]['cell_number']){
						frm.set_value("contact", res.message[0]['cell_number']);
					}
				}
			})
	 },
	 
});
