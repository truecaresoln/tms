from __future__ import unicode_literals
from frappe import _

def get_data():
    return {
        'fieldname': 'ion_number',
        'transactions': [
            {
                'label': _('Sales Invoice'),
                'items': ['Sales Invoice']
            },
        ]
    }    