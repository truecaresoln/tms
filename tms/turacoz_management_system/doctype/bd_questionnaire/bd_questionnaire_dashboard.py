from __future__ import unicode_literals
from frappe import _

def get_data():
    return {
        'fieldname': 'bd_questionnaire',
        'transactions': [
            {
                'label': _('Proposals'),
                'items': ['Proposals']
            },
        ]
    }    