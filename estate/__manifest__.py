# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'estate',
    'version': '1.0',
    'sequence': 15,
    'summary': 'Manage your estate',
    'description': "description dim",
    'website': 'https://www.odoo.com/page/crm',
    'depends': [
        'base','contacts','hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/estate_property_views.xml',
        'security/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}