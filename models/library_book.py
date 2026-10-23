from odoo import _, api, fields, models

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True)
    date_released = fields.Date(string='Date Released')
    author_ids = fields.Many2many(comodel_name='res.partner', string='Authors')