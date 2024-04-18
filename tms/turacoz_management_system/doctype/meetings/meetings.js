// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Meetings', {
	onload: function(frm) {
		if(frm.is_new()){
			frm.toggle_display("projectcall_brief_and_understandings_section", false);
			frm.toggle_display("projectcall_brief_and_understandings", false);

			frm.toggle_display("client_response_section", false);
			frm.toggle_display("client_response", false);

			frm.toggle_display("information_to_be_provided_to_the_client_section", false);
			frm.toggle_display("information_to_be_provided_to_the_client", false);

			frm.toggle_display("queries_to_the_client_section", false);
			frm.toggle_display("queries_to_the_client", false);

			frm.toggle_display("timeline_section", false);
			frm.toggle_display("timeline", false);

			frm.toggle_display("information_to_be_provided_by_the_client_section", false);
			frm.toggle_display("information_to_be_provided_by_the_client", false);

			frm.toggle_display("client_queries_section", false);
			frm.toggle_display("client_queries", false);

			frm.toggle_display("turacoz_response_section", false);
			frm.toggle_display("turacoz_response", false);

			frm.toggle_display("customer", false);
			frm.toggle_display("turacoz_representatives", false);
		}
	},

	"meeting_category": function(frm){
		var meeting_category = frm.doc.meeting_category;
		if(meeting_category=="Client"){
			frm.toggle_display("projectcall_brief_and_understandings_section", true);
			frm.toggle_display("projectcall_brief_and_understandings", true);

			frm.toggle_display("client_response_section", true);
			frm.toggle_display("client_response", true);

			frm.toggle_display("information_to_be_provided_to_the_client_section", true);
			cur_frm.toggle_display("information_to_be_provided_to_the_client", true);
			
			frm.toggle_display("queries_to_the_client_section", true);
			cur_frm.toggle_display("queries_to_the_client", true);

			frm.toggle_display("timeline_section", true);
			cur_frm.toggle_display("timeline", true);

			frm.toggle_display("information_to_be_provided_by_the_client_section", true);
			frm.toggle_display("information_to_be_provided_by_the_client", true);

			frm.toggle_display("client_queries_section", true);
			frm.toggle_display("client_queries", true);

			frm.toggle_display("turacoz_response_section", true);
			frm.toggle_display("turacoz_response", true);

			frm.toggle_display("customer", true);
			frm.toggle_display("turacoz_representatives", true);
			
		}
		else{
			frm.toggle_display("projectcall_brief_and_understandings_section", false);
			frm.toggle_display("projectcall_brief_and_understandings", false);

			frm.toggle_display("client_response_section", false);
			frm.toggle_display("client_response", false);

			frm.toggle_display("information_to_be_provided_to_the_client_section", false);
			cur_frm.toggle_display("information_to_be_provided_to_the_client", false);
			
			frm.toggle_display("queries_to_the_client_section", false);
			cur_frm.toggle_display("queries_to_the_client", false);

			frm.toggle_display("timeline_section", false);
			cur_frm.toggle_display("timeline", false);

			frm.toggle_display("information_to_be_provided_by_the_client_section", false);
			frm.toggle_display("information_to_be_provided_by_the_client", false);

			frm.toggle_display("client_queries_section", false);
			frm.toggle_display("client_queries", false);

			frm.toggle_display("turacoz_response_section", false);
			frm.toggle_display("turacoz_response", false);

			frm.toggle_display("customer", false);
			frm.toggle_display("turacoz_representatives", false);

		}
	},
	
	"organizer": function(frm){
		var user = frm.doc.organizer;
		if(user){
			set_company_representative(frm,user);
		}
	},
});


// set customer Link from Invoice
const set_company_representative = function(frm,user) {
	
	const options = {email: user};
	const fields = ['full_name'];
	frappe.db.get_value('User', options, fields).then(({ message }) => {
		if (message) {
			frm.set_value('turacoz_representatives',message.full_name);			
		}
	});
};
