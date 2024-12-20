
from odoo import api, fields, models

from datetime import datetime, timedelta, date

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
    best_price = fields.Float(
        string="Best price",
        compute='_compute_best_price', store=True,
        copy=False,
        help="Best price in the offers"
    )
    garden=fields.Boolean('Garden')

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_orientation = 'north'

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            # Vérifie si des offres existent pour cette propriété
            if record.offer_ids:
            # Trouve le montant maximal des offres
                record.best_price = max(record.offer_ids.mapped('amount'))
            else:
            # Si aucune offre, définis le prix à 0
                record.best_price = 0
    
    def sell(self):
        for record in self:
            if record.state == "sold":
                raise UserError("This property is already sold!")
            record.state = "sold"
            return True
    # Ajouter l'effet Rainbow Man
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Property sold successfully!',
                'img_url': '/web/static/src/img/smile.svg',  # URL par défaut, modifiable
                'type': 'rainbow_man',
            },
        }




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

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "sequence"

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=10)
    amount = fields.Float('Offer')
    validity_days = fields.Integer('Validity Days')
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_deadline', store=True, readonly=False,
        copy=False,
        help="Date at which the offer is no longer valid!!"
    )
    partner_id = fields.Many2one(
        'res.partner', string='Buyer', help="Buyer of the property", default=lambda self: self.env.user.partner_id)
    property_id = fields.Many2one(
        'estate.property', string='Property', help="Property for the offer")
    status = fields.Selection(string='Garden Orientation',
           selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
            ],default='accepted',help="What is the orientation of the garden?")

    @api.depends('validity_days')
    def _compute_deadline(self):
            for record in self:
                if record.validity_days:
                    record.date_deadline = date.today() + timedelta(days=record.validity_days)
                else:
                    record.date_deadline = date.today()

    @api.onchange("amount")
    def _onchange_amount(self):
        # Si le mec t'offre plus de 15€ c'est d'office une scam frère
        if self.amount > 15 :
            return {'warning': {
                'title': ("Warning"),
                'message': ('This is a scam')}}
        return super()._onchange_amount()

