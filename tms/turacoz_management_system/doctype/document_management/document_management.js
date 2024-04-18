// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Document Management', {
	// refresh: function(frm) {

	// }

	"document_title": function(frm){
		var document_title = frm.doc.document_title;
		var version = frm.doc.version;
		var department = frm.doc.department;
		var year = frm.doc.year;
		var type = frm.doc.document_title;

		var file_name = '';

		if(document_title){
			var document_title_new = ' - '+document_title;
		}
		else{
			var document_title_new = '';
		}

		if(version){
			var version_new = ' - '+version;
		}
		else{
			var version_new = '';
		}
		
		if(department){
			 var department_new = ' - '+department;
		}
		else{
			var department_new = '';
		}
		
		if(year){
			var year_new = year;
		}
		else{
			var year_new = '';
		}

		if(type){
			var type_new = ' - '+type;
		}
		else{
			var type_new = '';
		}
		
		file_name = year+department_new+type_new+document_title_new+version_new;
		frm.set_value('file', file_name);
	},

	"version": function(frm){
		var document_title = frm.doc.document_title;
		var version = frm.doc.version;
		var department = frm.doc.department;
		var year = frm.doc.year;
		var type = frm.doc.document_title;

		var file_name = '';

		if(document_title){
			var document_title_new = ' - '+document_title;
		}
		else{
			var document_title_new = '';
		}

		if(version){
			var version_new = ' - '+version;
		}
		else{
			var version_new = '';
		}
		
		if(department){
			 var department_new = ' - '+department;
		}
		else{
			var department_new = '';
		}
		
		if(year){
			var year_new = year;
		}
		else{
			var year_new = '';
		}

		if(type){
			var type_new = ' - '+type;
		}
		else{
			var type_new = '';
		}
		
		file_name = year+department_new+type_new+document_title_new+version_new;
		frm.set_value('file', file_name);
	},
	
	"department": function(frm){
		var document_title = frm.doc.document_title;
		var version = frm.doc.version;
		var department = frm.doc.department;
		var year = frm.doc.year;
		var type = frm.doc.document_title;

		var file_name = '';

		if(document_title){
			var document_title_new = ' - '+document_title;
		}
		else{
			var document_title_new = '';
		}

		if(version){
			var version_new = ' - '+version;
		}
		else{
			var version_new = '';
		}
		
		if(department){
			 var department_new = ' - '+department;
		}
		else{
			var department_new = '';
		}
		
		if(year){
			var year_new = year;
		}
		else{
			var year_new = '';
		}

		if(type){
			var type_new = ' - '+type;
		}
		else{
			var type_new = '';
		}
		
		file_name = year+department_new+type_new+document_title_new+version_new;
		frm.set_value('file', file_name);
	},

	"year": function(frm){
		var document_title = frm.doc.document_title;
		var version = frm.doc.version;
		var department = frm.doc.department;
		var year = frm.doc.year;
		var type = frm.doc.document_title;

		var file_name = '';

		if(document_title){
			var document_title_new = ' - '+document_title;
		}
		else{
			var document_title_new = '';
		}

		if(version){
			var version_new = ' - '+version;
		}
		else{
			var version_new = '';
		}
		
		if(department){
			 var department_new = ' - '+department;
		}
		else{
			var department_new = '';
		}
		
		if(year){
			var year_new = year;
		}
		else{
			var year_new = '';
		}

		if(type){
			var type_new = ' - '+type;
		}
		else{
			var type_new = '';
		}
		
		file_name = year+department_new+type_new+document_title_new+version_new;
		frm.set_value('file', file_name);
	},

	"type": function(frm){
		var document_title = frm.doc.document_title;
		var version = frm.doc.version;
		var department = frm.doc.department;
		var year = frm.doc.year;
		var type = frm.doc.document_title;

		var file_name = '';

		if(document_title){
			var document_title_new = ' - '+document_title;
		}
		else{
			var document_title_new = '';
		}

		if(version){
			var version_new = ' - '+version;
		}
		else{
			var version_new = '';
		}
		
		if(department){
			 var department_new = ' - '+department;
		}
		else{
			var department_new = '';
		}
		
		if(year){
			var year_new = year;
		}
		else{
			var year_new = '';
		}

		if(type){
			var type_new = ' - '+type;
		}
		else{
			var type_new = '';
		}
		
		file_name = year+department_new+type_new+document_title_new+version_new;
		frm.set_value('file', file_name);
	}


});
