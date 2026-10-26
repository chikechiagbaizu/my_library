from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['base.archive','mail.thread']
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
    short_name = fields.Char(string='Short Title', required=True, translate=True)
    notes = fields.Text(string='Internal Notes')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost','Lost'),
    ],string='State', default='draft', readonly=True)
    description = fields.Html(string='Description', sanitize=True)
    cover = fields.Binary(string='Book Cover')
    out_of_print = fields.Boolean(string='Out of Print?')
    date_updated = fields.Date(string='Last Updated')
    pages = fields.Integer(string='Number of Pages')
    reader_rating = fields.Float(string='Readers Average Rating', digits=(14,4))
    active = fields.Boolean(string='Active', default=True)
    cost_price = fields.Monetary(string='Book Cost', currency_field='currency_id')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    retail_price = fields.Monetary(currency_field='currency_id', string='Retail Price')
    publisher_id = fields.Many2one(comodel_name='res.partner', string='Publisher', ondelete='set null')
    category_id = fields.Many2one(comodel_name='library.book.category', string='Category')
    age_days = fields.Float(string='Days Since Release', compute='_compute_age')
    publisher_city = fields.Char(string='Publisher City', related='publisher_id.city', readonly=True)
    manager_remarks = fields.Text(string='Manager Remarks')

    @api.constrains('date_released')
    def _validate_release_date(self):
        today = fields.Date.today()
        for record in self:
            if record.date_released and record.date_released > today:
                    raise ValidationError(_("Error! Release date must be in the past."))
    
    @api.depends('date_released')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self:
            if book.date_released:
                delta = today - book.date_released
                book.age_days = delta.days
            else:
                book.age_days = 0
    
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [
            ('draft','available'),
            ('available','borrowed'),
            ('borrowed','available'),
            ('available','lost'),
            ('borrowed','lost'),
            ('lost','available'),
        ]
        return (old_state,new_state) in allowed

    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state,new_state):
                book.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (book.state, new_state)
                raise UserError(msg)
    
    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')
    
    def log_all_library_members(self):
        library_member_model = self.env['library.member']

        all_members = library_member_model.search([])
        _logger.info("--- ALL MEMBERS --- %s", all_members.name)
        return True

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.user.has_group('my_library.group_librarians'):
            for vals in vals_list:
                if 'manager_remarks' in vals:
                    msg = _("You are not allowed to create 'manager remarks")
                    raise UserError(msg)
        return super(LibraryBook,self).create(vals_list)

    def write(self, vals):
        if not self.env.user.has_group('my_library.group_librarians'):
            if 'manager_remarks' in vals:
                msg = _("You are not allowed to modify 'manager remarks'")
                raise UserError(msg)
        return super(LibraryBook,self).write(vals)
    
    def get_average_cost(self):
        grouped_result = self._read_group(
            domain = [('cost_price','!=',False)],
            aggregates=['cost_price:avg'],
            groupby = ['category_id']
            )
        return grouped_result