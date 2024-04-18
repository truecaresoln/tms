// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Contract Document', {
	// refresh: function(frm) {

	// }
	onload: function(frm){
		if(frm.is_new()){
			var company = frm.doc.company;

			if(company == 'Turacoz Healthcare Solutions Pvt Ltd')
			{
				frm.set_value('naming','THS-PCD-2024-25');
			}
			else if(company == 'Turacoz Solutions LLC')
			{
				frm.set_value('naming','TSLLC-PCD-2024-25');
			}
			else if(company == 'Turacoz Solutions PTE Ltd.')
			{
				frm.set_value('naming','TSPL-PCD-2024-25');
			}
			else if(company == 'Turacoz B.V.')
			{
				frm.set_value('naming','TBV-PCD-2024-25');
			}
			else if(company == 'Turacoz Canada Inc')
			{
				frm.set_value('naming','TCI-PCD-2024-25');
			}
		}
	},

	"company":function(frm)
	{
		var company = frm.doc.company;

		if(company == 'Turacoz Healthcare Solutions Pvt Ltd')
		{
			frm.set_value('naming','THS-PCD-2024-25');
		}
		else if(company == 'Turacoz Solutions LLC')
		{
			frm.set_value('naming','TSLLC-PCD-2024-25');
		}
		else if(company == 'Turacoz Solutions PTE Ltd.')
		{
			frm.set_value('naming','TSPL-PCD-2024-25');
		}
		else if(company == 'Turacoz B.V.')
		{
			frm.set_value('naming','TBV-PCD-2024-25');
		}
		else if(company == 'Turacoz Canada Inc')
		{
			frm.set_value('naming','TCI-PCD-2024-25');
		}
	},
	
	"project_contract_template":function(frm)
	{
		var note = frm.doc.note;
		frm.set_value('note1',note);
	}
});



