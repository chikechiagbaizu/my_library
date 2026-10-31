from odoo import fields, models

class LibraryRentWizard(models.TransientModel):
    _name = 'library.rent.wizard'
    _description = 'Library Rent Wizard'

    borrower_id = fields.Many2one(comodel_name='res.partner', string='Borrower')
    books_id = fields.Many2many(comodel_name='library.book', string='Books')

    def add_book_rents(self):
        rentModel = self.env['library.book.rent']
        for record in self:
            for book in record.books_id:
                rentModel.create({
                    'borrower_id': record.borrower_id.id,
                    'book_id': book.id
                })