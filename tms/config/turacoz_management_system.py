from __future__ import unicode_literals
import frappe
from frappe import _

def get_data():
    return[
        {
            "label": ("Staff Management"),
            "items": [                
                {
                    "type": "doctype",
                    "name": "Employee",
                    "onboard": 1,
                    "label": _("Employee"),
                    "description": _("Employee"),
                },
                {
                    "type": "doctype",
                    "name": "Department",
                    "onboard": 1,
                    "label": _("Department"),
                    "description": _("Department"),
                },
                {
                    "type": "doctype",
                    "name": "Designation",
                    "onboard": 1,
                    "label": _("Designation"),
                    "description": _("Designation"),
                },
                {
                    "type": "doctype",
                    "name": "Regions",
                    "onboard": 1,
                    "label": _("Regions"),
                    "description": _("Regions"),
                }, 
                {
                    "type": "doctype",
                    "name": "Country",
                    "onboard": 1,
                    "label": _("Country"),
                    "description": _("Country"),
                }, 
                {
                    "type": "doctype",
                    "name": "Holiday List",
                    "onboard": 1,
                    "label": _("Holiday List"),
                    "description": _("Holiday List"),
                },                                 
            ]
        },
        {
            "label": ("Business Development"),
            "items": [                
                {
                    "type": "doctype",
                    "name": "Lead",
                    "onboard": 1,
                    "label": _("Lead"),
                    "description": _("Lead"),
                },
                {
                    "type": "doctype",
                    "name": "Opportunity",
                    "onboard": 1,
                    "label": _("Opportunity"),
                    "description": _("Opportunity"),
                },
                {
                    "type": "doctype",
                    "name": "Quotation",
                    "onboard": 1,
                    "label": _("Quotation"),
                    "description": _("Quotation"),
                },
                {
                    "type": "doctype",
                    "name": "Customer",
                    "onboard": 1,
                    "label": _("Customer"),
                    "description": _("Customer"),
                },
                {
                    "type": "doctype",
                    "name": "Lead Source",
                    "onboard": 1,
                    "label": _("Lead Source"),
                    "description": _("Lead Source"),
                },
                {
                    "type": "doctype",
                    "name": "Lead Type",
                    "onboard": 1,
                    "label": _("Lead Type"),
                    "description": _("Lead Type"),
                },
                {
                    "type": "doctype",
                    "name": "Request Type",
                    "onboard": 1,
                    "label": _("Request Type"),
                    "description": _("Request Type"),
                },
                {
                    "type": "doctype",
                    "name": "Opportunity Type",
                    "onboard": 1,
                    "label": _("Opportunity Type"),
                    "description": _("Opportunity Type"),
                },                
            ]
        },
        {
            "label": ("Project Management"),
            "items": [
                      
                {
                    "type": "doctype",
                    "name": "Project",
                    "onboard": 1,
                    "label": _("Project"),
                    "description": _("Project"),
                },
                {
                    "type": "doctype",
                    "name": "Therapeutic Area",
                    "onboard": 1,
                    "label": _("Therapeutic Area"),
                    "description": _("Therapeutic Area"),
                },
                {
                    "type": "doctype",
                    "name": "Product Line",
                    "onboard": 1,
                    "label": _("Product Line"),
                    "description": _("Product Line"),
                },
                 {
                    "type": "doctype",
                    "name": "Services",
                    "onboard": 1,
                    "label": _("Services"),
                    "description": _("Services"),
                },
                 {
                    "type": "doctype",
                    "name": "Service Types",
                    "onboard": 1,
                    "label": _("Service Types"),
                    "description": _("Service Types"),
                },
                 {
                    "type": "doctype",
                    "name": "Deliverable",
                    "onboard": 1,
                    "label": _("Deliverable"),
                    "description": _("Deliverable"),
                }, 
                {
                    "type": "doctype",
                    "name": "Activity Type",
                    "onboard": 1,
                    "label": _("Activity Type"),
                    "description": _("Activity Type"),
                },
                {
                    "type": "doctype",
                    "name": "Main Task",
                    "onboard": 1,
                    "label": _("Main Task"),
                    "description": _("Main Task"),
                },
                {
                    "type": "doctype",
                    "name": "Project Status List",
                    "onboard": 1,
                    "label": _("Project Status List"),
                    "description": _("Project Status List"),
                },
                {
                    "type": "doctype",
                    "name": "Project Type",
                    "onboard": 1,
                    "label": _("Project Type"),
                    "description": _("Project Type"),
                },               
            ]
        },
        {
            "label": ("Financial Management"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Sales Order",
                    "onboard": 1,
                    "label": _("Sales Order"),
                    "description": _("Sales Order"),
                },
                {
                    "type": "doctype",
                    "name": "Sales Invoice",
                    "onboard": 1,
                    "label": _("Sales Invoice"),
                    "description": _("Sales Invoice"),
                },
                {
                    "type": "doctype",
                    "name": "Financial Session",
                    "onboard": 1,
                    "label": _("Financial Session"),
                    "description": _("Financial Session"),
                },
                {
                    "type": "doctype",
                    "name": "Company",
                    "onboard": 1,
                    "label": _("Company"),
                    "description": _("Company"),
                },
                {
                    "type": "doctype",
                    "name": "Bank",
                    "onboard": 1,
                    "label": _("Bank"),
                    "description": _("Bank"),
                },
                {
                    "type": "doctype",
                    "name": "Price List",
                    "onboard": 1,
                    "label": _("Price List"),
                    "description": _("Price List"),
                },
                {
                    "type": "doctype",
                    "name": "Sales Taxes and Charges Template",
                    "onboard": 1,
                    "label": _("Sales Taxes and Charges Template"),
                    "description": _("Sales Taxes and Charges Template"),
                },                
            ]
        },
        {
            "label": ("Products"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Item",
                    "onboard": 1,
                    "label": _("Item"),
                    "description": _("Item"),
                },
                {
                    "type": "doctype",
                    "name": "Item Price",
                    "onboard": 1,
                    "label": _("Item Price"),
                    "description": _("Item Price"),
                },
                {
                    "type": "doctype",
                    "name": "Item Group",
                    "onboard": 1,
                    "label": _("Item Group"),
                    "description": _("Item Group"),
                },
                {
                    "type": "doctype",
                    "name": "Dashboard",
                    "onboard": 1,
                    "label": _("Dashboard"),
                    "description": _("Dashboard"),
                },
                {
                    "type": "doctype",
                    "name": "UOM",
                    "onboard": 1,
                    "label": _("UOM"),
                    "description": _("UOM"),
                },
            ]
        },
    ]
        
        