// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('IT Issues and Concerns', {
	onload: function(frm) {
		if(frm.is_new()){
			var user_id = frappe.session.user;
			if(user_id)
			{
				frm.set_value("creator", user_id);
			}
		}

		var ticket_status = frm.doc.ticket_status;
		if(ticket_status!='Open'){
			cur_frm.toggle_display("solution", true);
			frm.set_df_property("solution", "reqd", 1);
		}
		
		var solution = frm.doc.solution;
		if(solution!=''){
			frm.set_df_property("solution", "read_only", 1);
		} 
	},

	"ticket_status":function(frm){
		var ticket_status = frm.doc.ticket_status;
alert("ticket_status");
		if(ticket_status!='Open'){
			cur_frm.toggle_display("solution", true);
			frm.set_df_property("solution", "reqd", 1);
			frm.set_df_property("solution", "read_only", 0);
		}
		else{
			cur_frm.toggle_display("solution", false);
			frm.set_df_property("solution", "reqd", 0);
		}
	},
});


