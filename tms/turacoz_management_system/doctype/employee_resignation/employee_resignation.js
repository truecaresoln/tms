// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Resignation', {
	 onload: function(frm) {
		var employee_id = frm.doc.employee;	
		if(frm.is_new()){
			if(employee_id){
				set_employee_related_details(frm,employee_id);
			}
			
			var userid = frappe.session.user
			if(userid){
				if(userid != "Administrator"){
					frappe.call({
						method: "tms.turacoz_management_system.doctype.employee_resignation.employee_resignation.get_empid",
						args:{ "userid":userid
						},
						callback:function(res){
							let a = res.message;
							if(a){
								frm.set_value("employee", a);
							}
						}
					})
				}
			}
		}

	 },

	"employee": function(frm){
		var employee_id = frm.doc.employee;
		if(employee_id){	
			set_employee_related_details(frm,employee_id);
		}
	},
});


// set employee related details
const set_employee_related_details = function(frm,employee_id) {
	
	const options = {name: employee_id};
	const fields = ['user_id','reporting_manager_id','notice_number_of_days','designation'];
	frappe.db.get_value('Employee', options, fields).then(({ message }) => {
		if (message) {
			frm.set_value("owner", message.user_id);
			frm.set_value("reporting_manager", message.reporting_manager_id);
			frm.set_value("notice_number_of_days", message.notice_number_of_days);
			frm.set_value("designation", message.designation);

			/*const days = parseInt(message.notice_number_of_days);
			frm.set_value("relieving_date", frappe.datetime.add_days(frappe.datetime.nowdate(), days));*/
		}
	});
};
