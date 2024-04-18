// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Email Data Verification', {
/*	 onload: function(frm) {
		
		var user_id = frm.doc.user_id;
		if(user_id)
		{
			set_employee_id(frm,user_id);
		}	
	 },

	"user_id":function(frm){
		var user_id = frm.doc.user_id;
		if(user_id)
		{
			set_employee_id(frm,user_id);
		}
	},	
*/
});

// set employee id on create
const set_employee_id = function(frm,user_id) {
	
	const options = {company_email: user_id};
	const fields = ['name'];
	frappe.db.get_value('Employee', options, fields).then(({ message }) => {
		if (message) {
			frm.set_value("employee", message.name);
			
		}
	});
};
