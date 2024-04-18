// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project New Update', {
	 onload: function(frm) {
		var userid =  frappe.session.user;
		set_finacially_records(frm);

	 },

});

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
				frm.toggle_display("financial_data", false);
			}
			else{
				frm.toggle_display("financial_data", true);
			}
		}
	});
};
