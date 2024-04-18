from __future__ import unicode_literals
from frappe import _

def get_data():
    return {
        'fieldname': 'project_detail_template',
        'transactions': [
            {
                'label': _('Project'),
                'items': ['Project']
            },
            {
                'label': _('Touchpoints'),
                'items': ['Turacoz and Client Touchpoints']
            },
            {
                'label': _('PUD Technical Input'),
                'items': ['PUD Technical Input']
            },    
        ]
    }