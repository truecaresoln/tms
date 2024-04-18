// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tax Filling Documents', {
	// refresh: function(frm) {

	// }
	"company":function(frm)
	{
			var company = frm.doc.company;
			
			// filter on project
			cur_frm.set_query("company_registration_document", function() {
				return {
					"filters": {
				    	"company": ("=", company)
				   }
				};
			});
	},
});

frappe.ui.form.on("Tax Filling Particulars", {
    "tax_value": function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var tax_value = 0;
        frm.doc.particulars.forEach(function(d) { tax_value += d.tax_value; });
        frm.set_value('total_amount', tax_value);
    },	
});
