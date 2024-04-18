from __future__ import unicode_literals
from frappe import _

def get_data():
    return {
        'fieldname': 'statement_of_work',
        'transactions': [
            {
                'label': _('Change Order Request'),
                'items': ['Change Order Request']
            },   
        ]
    }