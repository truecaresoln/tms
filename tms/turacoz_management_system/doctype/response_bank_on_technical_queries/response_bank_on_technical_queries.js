// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Response Bank on Technical Queries', {
	 onload: function(frm) {
		var userid = frappe.session.user;
		frm.set_value("bd_poc",userid);

		cur_frm.set_query("contact", function(){
            	if(frm.doc.customer) {
                	return {
                    		query: "frappe.contacts.doctype.contact.contact.contact_query",
                    		filters: { link_doctype: "Customer", link_name: cur_frm.doc.customer }
                		};
          		}
        	});
        	
	},


	"service":function(frm)
	{
		var service = frm.doc.service;
		cur_frm.set_query("service_types", function() {
			return {
				"filters": {
			    	"service": ("=", service)
			   }
			};
		});
	}
});
