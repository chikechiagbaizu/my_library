from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many(comodel_name='library.book', inverse_name='publisher_id', string='Published Books')
    author_book_ids = fields.Many2many(comodel_name='library.book', string='Authored Books')
    count_books = fields.Integer(string='Number of Authored Books', compute='_compute_count_books')

    @api.depends('author_book_ids')
    def _compute_count_books(self):
        for book in self:
            if book.author_book_ids:
                book.count_books = len(book.author_book_ids)