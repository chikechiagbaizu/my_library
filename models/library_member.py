from odoo import fields, models

class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Members'
    _inherits = {'res.partner':'partner_id'}

    partner_id = fields.Many2one(comodel_name='res.partner', string='Member', ondelete='cascade', required=True)
    date_start = fields.Date(string='Member Since')
    date_end = fields.Date(string='Termination Date')
    member_number = fields.Char(string='Member Number')
    date_of_birth = fields.Date(string='Date of birth')