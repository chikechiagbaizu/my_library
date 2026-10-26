from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'
    _parent_store = True
    _parent_name = 'parent_id'

    name = fields.Char(string='Category')
    description = fields.Text(string='Description')
    parent_id = fields.Many2one(comodel_name='library.book.category', string='Parent Category', ondelete='restrict', index=True)
    child_ids = fields.One2many(comodel_name='library.book.category', string='Child Category', inverse_name='parent_id')
    parent_path = fields.Char(index=True)

    @api.constrains
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise ValidationError(_('Error! You cannot create recursive categories.'))
    
    def create_categories(self):
        category1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }

        category2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }

        parent_category1 = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'child_ids': [
                (0,0,category1),
                (0,0,category2),
            ]
        }

        record = self.env['library.book.category'].create(parent_category1)
        return record