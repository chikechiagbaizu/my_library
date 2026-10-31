from odoo import fields, models

class LibraryBookRent(models.Model):
    _name = 'library.book.rent'
    _description = 'Library Book Rent'

    name = fields.Char(string='Reference')
    book_id = fields.Many2one(comodel_name='library.book', string='Book', required=True)
    borrower_id = fields.Many2one(comodel_name='res.partner', string='Borrower', required=True)
    state = fields.Selection(selection=[
        ('ongoing','Ongoing'),
        ('returned','Returned'),
        ('lost','Lost'),
    ], string='State', default='ongoing', required=True)
    rent_date = fields.Date(string='Rent Date', default=fields.Date.context_today)
    return_date = fields.Date(string='Return Date')

    def book_lost(self):
        self.ensure_one()
        self.sudo().state = 'lost'
        new_context = self.env.context.copy()
        new_context.update({'avoid_deactivate':True})
        book_with_different_context = self.book_id.with_context(new_context)
        book_with_different_context.sudo().make_lost()
