from __future__ import unicode_literals
from frappe import _

def get_data():
    return {
        'heatmap': True,
        'heatmap_message': _('This is based on the Student Invoice created against this Student'),
        'fieldname': 'training_data',
        'transactions': [
            {
                'label': _('Student Invoice'),
                'items': ['Student Invoice', 'Fees Received', 'PCD Student']
            },
            
        ]
    }