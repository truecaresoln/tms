// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Turacoz and Client Touchpoints', {
	 onload: function(frm) {
/*			var customer = frm.doc.customer;
			
			// filter on project
			cur_frm.set_query("project", function() {
				return {
					"filters": {
				    	"customer": ("=", customer)
				   }
				};
			});
			
			// filter on project detail template
			cur_frm.set_query("project_detail_template", function() {
				return {
					"filters": {
				    	"customer": ("=", customer)
				   }
				};
			});

			// filter on customer
			var project_detail_template = frm.doc.project_detail_template
			
			cur_frm.set_query("customer", function() {
				return {
					"filters": {
				    	"project_detail_template": ("=", project_detail_template)
				   }
				};
			});*/
	 },

	"customer":function(frm)
	{
		var customer = frm.doc.customer;
			
		// filter on project
		cur_frm.set_query("project", function() {
			return {
				"filters": {
			    	"customer": ("=", customer)
			   }
			};
		});
			
		// filter on project detail template
		cur_frm.set_query("project_detail_template", function() {
			return {
				"filters": {
			    	"customer": ("=", customer)
			   }
			};
		});
	},
	

	"project_detail_template":function(frm)
	{
		var project_detail_template = frm.doc.project_detail_template;
		var customer = frm.doc.customer;
		var project = frm.doc.project;
		if(customer && project){
		}
		else{	
			const options = {name: project_detail_template};
			const fields = ['customer','project'];
			frappe.db.get_value('Project Detail Template', options, fields).then(({ message }) => {
			if (message) {
				frm.set_value("customer", message.customer);
				frm.set_value("project", message.project);
			}
			});
		}
	},	

	"project":function(frm)
	{
		var project = frm.doc.project;
			
		const options = {name: project};
		const fields = ['customer','project_detail_template'];
		frappe.db.get_value('Project', options, fields).then(({ message }) => {
		if (message) {
			frm.set_value("customer", message.customer);
			frm.set_value("project_detail_template", message.project_detail_template);
		}
		});
	},
});
