// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('PCD Student', {
	// refresh: function(frm) {

	// }
	
	"project_contract_template": function(frm){
	
		var std_pcd_template = frm.doc.note;
		
		if(std_pcd_template)
		{
			frm.set_value("note1", std_pcd_template);
			frm.set_value("letter_head", "PCD Letter Head");
		}
	}
});
