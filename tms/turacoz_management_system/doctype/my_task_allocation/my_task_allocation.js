// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('My Task Allocation', {
	refresh: function(frm) {
		var status = frm.doc.status;
		if(status == "Cancelled"){
			frm.set_df_property("status", "read_only", 1);
			frm.set_df_property("follow_up", "read_only", 1);
			frm.set_df_property("task_updates", "read_only", 1);
		}
		else if(status == "Close"){
			frm.set_df_property("status", "read_only", 1);
			frm.set_df_property("follow_up", "read_only", 1);
			frm.set_df_property("task_updates", "read_only", 1);
		}
	},

	"contact_detail": function(frm){
		var contact_detail = frm.doc.contact_detail;
		if(contact_detail){
			frappe.call({
				method: "tms.turacoz_management_system.doctype.my_task_allocation.my_task_allocation.get_contact_detail",
				args:{ "contact_detail":contact_detail
				},
				callback:function(res){
					let a = res.message;
					if (a){
						frm.set_value('contact_display', a);
					}
				}
			})
		}
	},
	
});
