// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Laptop Requisition Form', {
	 onload: function(frm) {
	 
	 	var userid = frappe.session.user;
	 
	 	frappe.call({
			method: "tms.turacoz_management_system.doctype.laptop_requisition_form.laptop_requisition_form.get_template_detail",
			args:{ "userid":userid
			},
			callback:function(res){
				let a = res.message;
				if(a){
					frm.set_value("declaration_cum_undertaking", a);
				}
			}
		})

	 },
});
