// Copyright (c) 2023, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Document Management System', {
	onload: function(frm){
		var user = frappe.session.user;
		frm.set_query("task_allocated", function() {
			return {
				"filters": {
			    	"reference_type": ("=", "DMS ALERT SYSTEM"),
			    	"owner": ("=", user)
			   }
			};
		});
		
		if(frm.is_new())
		{
			var user = frappe.session.user;
			var roles = '';
			frappe.call({
        	method: "tms.turacoz_management_system.doctype.document_management_system.document_management_system.getroles",
		args:{ "user":user
		},
		callback:function(res){
			roles = res.message;
			}
			});
				
			frm.set_query("department", function() {
			return {
				"filters": [
			    	['DMS Assign Role', 'role', 'in', roles]
			   ]
			};
		});
		
		}
	},
	
	// refresh: function(frm) {
	"department": function(frm) {
		var ab = frm.doc.department;
		cur_frm.set_query("category", function() {
			return {
				"filters": {
			    	"department": ("=", ab)
			   }
			};
		});
	},
	"category": function(frm) {
		var ab = frm.doc.category;
		cur_frm.set_query("sub_category", function() {
			return {
				"filters": {
			    	"category": ("=", ab)
			   }
			};
		});
	},
	
		
	
	"document_attachment": function(frm){
		var document_attachment = frm.doc.document_attachment;
		var fileExt = document_attachment.split('.').pop();
		var file_link = "https://erp.turacoz.com"+document_attachment;
		frm.set_value('file_type', fileExt);
		frm.set_value('file_link',file_link);
	},

	// }
});











