// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Challenges', {
	 onload: function(frm) {
		var creator = frm.doc.creator;
		
		var userid =  frappe.session.user;

		if (frm.is_new()) {
			frm.set_value("creator", userid);
			set_record_approver(frm);
			//set_record_creator(frm);	
		}
		
		var challenge_status = frm.doc.challenge_status;
		if(challenge_status == 'Active')
		{
			frm.toggle_display("solutions", false);
			frm.toggle_display("date_of_solution", false);	
		}
		else
		{
			frm.toggle_display("solutions", true);
			frm.toggle_display("date_of_solution", true);	
		}

		set_finacially_records(frm);
	 },

	"challenge_status":function(frm){
		var challenge_status = frm.doc.challenge_status;
		if(challenge_status == "Close")
		{
			frm.set_df_property("date_of_solution", "reqd", 1);
			frm.set_df_property("solutions", "reqd", 1);
			frm.toggle_display("solutions", true);
			frm.toggle_display("date_of_solution", true);	
		}
		else
		{
			frm.set_df_property("date_of_solution", "reqd", 0);
			frm.set_df_property("solutions", "reqd", 0);
			frm.toggle_display("solutions", false);
			frm.toggle_display("date_of_solution", false);	
			
		}	
	}
});

// set employee project detail approver to the one that's currently logged in
const set_record_approver = function(frm) {
	/*let today = new Date().toISOString().slice(0, 10);
	const options = {company_email: frappe.session.user};
	const fields = ['project_detail_approver'];
	frappe.db.get_value('Employee', options, fields).then(({ message }) => {
		if (message) {
			// there is an employee with the currently logged in user_id
			frm.set_value("approver", message.project_detail_approver);
		}
	});*/
	
	frappe.call({
        	method: "tms.turacoz_management_system.doctype.challenges.challenges.getapprover",
		args:{ "company_email": frappe.session.user
		},
		callback:function(res){
			frm.set_value("approver", res.message);	
		}
        })
};

// set employee project detail approver to the one that's currently logged in
const set_record_creator = function(frm) {
	let today = new Date().toISOString().slice(0, 10);
	const options = {company_email: frappe.session.user};
	const fields = ['name'];
	frappe.db.get_value('Employee', options, fields).then(({ message }) => {
		if (message) {
			// there is an employee with the currently logged in user_id
			
			frm.set_value("creator", message.name);
		}
	});
};

// check logged in user financially active or not
const set_finacially_records = function(frm) {
	let today = new Date().toISOString().slice(0, 10);
	let type_of_challenge = frm.doc.type_of_challenge;
	const options = {name: frappe.session.user};
	const fields = ['is_financially_active'];
	frappe.db.get_value('Financially Active', options, fields).then(({ message }) => {
		if (message) {
			if(message.is_financially_active == 0)
			{
				if(type_of_challenge == 'Financial'){
					frm.toggle_display("description_of_challenge", false);
					frm.toggle_display("remark", false);
					frm.toggle_display("solutions", false);			
				}
				else{
					frm.toggle_display("description_of_challenge", true);
					frm.toggle_display("remark", true);
					frm.toggle_display("solutions", true);	
				}
			}
			else{
				frm.toggle_display("description_of_challenge", true);
				frm.toggle_display("remark", true);
				frm.toggle_display("solutions", true);	
			}
		}
	});
};
