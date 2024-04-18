// Copyright (c) 2023, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Performance Feedback', {
	 
	 "employee":function(frm)
	 {
	 	var emp = frm.doc.employee;
	 	frappe.call({
			method: "tms.turacoz_management_system.doctype.employee_performance_feedback.employee_performance_feedback.get_param",
			args:{"employee":emp},
			callback:function(res){
				cur_frm.clear_table("performance_rating");
				cur_frm.refresh_fields();
				for(var i=0; i<res.message.length; i++)
				{
					var childTable = cur_frm.add_child("performance_rating");
					childTable.feedback_area = res.message[i].name;
					
				}
				cur_frm.refresh_fields("performance_rating");
			}
        	})
	 },
});


