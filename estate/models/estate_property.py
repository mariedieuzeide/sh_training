
from odoo import fields, models

from datetime import datetime, timedelta

from random import randint

def default_date_availability(self):
    return (datetime.today() + timedelta(days=90)).date()

def _get_default_color(self):
        return randint(1, 11)

class Property(models.Model):
    _name = "estate.property"
    _description = "Properties"
    _order = "sequence"

    name = fields.Char('Property Name', required=True, translate=True)
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)
    selling_price = fields.Float('Price', readonly=True, copy=False)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    bedrooms = fields.Integer('Bedroom',default=2)
    date_availability = fields.Date('Date available',default=default_date_availability, copy=False)
    garden_orientation = fields.Selection(string='Garden Orientation',
           selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')       
            ],default='north',help="What is the orientation of the garden?")
    state = fields.Selection(string='State',
           selection=[
            ('new', 'New'),
            ('received', 'Offer received'),
            ('accepted', 'Offer accepted'),
            ('sold', 'Sold'),
            ('canceled','Canceled') 
            ],default='new')
    partner_id = fields.Many2one(
        'res.partner', string='Buyer', help="Buyer of the property", default=lambda self: self.env.user.partner_id)
    employee_id = fields.Many2one(
        'hr.employee', string='Seller', help="Seller of the property", default=lambda self: self.env.user.employee_id)
    tag_ids = fields.Many2many('estate.property.tags', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Propertiy Types"
    _order = "sequence"

    name = fields.Char('Name', required=True, translate=True)
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)
 
class PropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Propertiy Tags"
    _order = "sequence"

    name = fields.Char('Name', required=True, translate=True)
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)
    color = fields.Integer('Color', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "A tag with the same name already exists."),
    ]

class PropertyTags(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "sequence"

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=10)
    amount = fields.Float('Offer')
    partner_id = fields.Many2one(
        'res.partner', string='Buyer', help="Buyer of the property", default=lambda self: self.env.user.partner_id)
    property_id = fields.Many2one(
        'estate.property', string='Property', help="Property for the offer")
    status = fields.Selection(string='Garden Orientation',
           selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
            ],default='accepted',help="What is the orientation of the garden?")