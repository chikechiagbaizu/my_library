from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many(comodel_name='library.book', inverse_name='publisher_id', string='Published Books')
    author_book_ids = fields.Many2many(comodel_name='library.book', string='Authored Books')