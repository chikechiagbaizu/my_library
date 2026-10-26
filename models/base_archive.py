from odoo import fields, models

class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Base Archive'

    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active