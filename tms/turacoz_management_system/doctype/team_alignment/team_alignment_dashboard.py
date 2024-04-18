from __future__ import unicode_literals
from frappe import _

def get_data():
    return {
        'fieldname': 'project',
        'transactions': [
            {
                'label': _('Challenges and Commitments'),
                'items': ['Challenges and Commitments']
            },
            {
                'label': _('Project Updates'),
                'items': ['Project New Update']
            },
        ]
    }    