from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_released desc, name'
    _rec_name = 'short_name'

    _unique_name_constraint = models.Constraint(
        'UNIQUE(name)',
        'Error! Book title must be unique.'
    )

    _book_page_constraint = models.Constraint(
        'CHECK(pages > 0)',
        'Error! Number of pages should be greater than 0.'
    )

    name = fields.Char(string='Title', required=True)
    date_released = fields.Date(string='Release Date')
    author_ids = fields.Many2many(comodel_name='res.partner', string='Authors')
    short_name = fields.Char(string='Short Title', required=True, translate=True, index=True)
    notes = fields.Text(string='Internal Notes')
    state = fields.Selection(selection=[
        ('draft', 'Not Available'),
        ('available', 'Available'),
        ('lost','Lost'),
    ],string='State', default='draft')
    description = fields.Html(string='Description', sanitize=True)
    cover = fields.Binary(string='Book Cover')
    out_of_print = fields.Boolean(string='Out of Print?')
    date_updated = fields.Datetime(string='Last Updated')
    pages = fields.Integer(string='Number of Pages')
    reader_rating = fields.Float(string='Readers Average Rating', digits=(14,4))
    active = fields.Boolean(string='Active', default=True)
    cost_price = fields.Monetary(string='Book Cost', currency_field='currency_id')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    retail_price = fields.Monetary(currency_field='currency_id', string='Retail Price')
    publisher_id = fields.Many2one(comodel_name='res.partner', string='Publisher', ondelete='set null')
    category_id = fields.Many2one(comodel_name='library.book.category', string='Category')

    @api.constrains('date_released')
    def _validate_release_date(self):
        today = fields.Date.today()
        for record in self:
            if record.date_released and record.date_released > today:
                    raise ValidationError(_("Error! Release date must be in the past."))