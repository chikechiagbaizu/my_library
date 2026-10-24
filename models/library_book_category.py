from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'
    _parent_store = True
    _parent_name = 'parent_id'

    name = fields.Char(string='Category')
    parent_id = fields.Many2one(comodel_name='library.book.category', string='Parent Category', ondelete='restrict', index=True)
    child_ids = fields.One2many(comodel_name='library.book.category', string='Child Category', inverse_name='parent_id')
    parent_path = fields.Char(index=True)

    @api.constrains
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise ValidationError(_('Error! You cannot create recursive categories.'))