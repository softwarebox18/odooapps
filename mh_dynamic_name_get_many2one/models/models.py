# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _

class many2one_name_search_and_get_config(models.Model):

    _name = 'many2one.name.search.and.get.config'
    _description = 'Name Search and Get Config'
    _rec_name = 'model_id'

    model_id = fields.Many2one('ir.model', string='Model')
    is_active = fields.Boolean(string="Active", default=False)
    fields_ids = fields.Many2many('ir.model.fields', string='Fields', domain="[('model_id', '=', model_id)]", required=True)
    code_html = fields.Html(string='Code', sanitize=False, strip_style=False, translate=False)

    @api.onchange('model_id')
    def _onchange_model_id(self):
        if self.model_id:
            model_name = self.model_id.model
            class_name = model_name.replace('.', '_').title().replace('_', '') + 'InheritNameSearch'
            inherit_line = f"_inherit = '{model_name}'"
            # Fetch all module names associated with the model
            module_records = self.env['ir.model.data'].search([('model', '=', 'ir.model'), ('res_id', '=', self.model_id.id)])
            module_names = [record.module for record in module_records]

            method_code = f'''<pre><code>
class {class_name}(models.Model):
    {inherit_line}

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        return self._search(domain, limit=limit, order=order)
            </code></pre>'''

            # Add modules to the HTML
            if module_names:
                module_list = ''.join([f'<li>{module_name}</li>' for module_name in module_names])
                method_code += f'<p>If after pasting the above code gives an error, make sure you have added one of the relevant modules to the dependencies of your module. Look at the manifest file of your module.</p>'
                method_code += f'<ul>{module_list}</ul>'

            self.code_html = method_code
        else:
            self.code_html = ''

    # Apply the unique constraint in the model definition
    _sql_constraints = [
        ('model_id_unique',
         'UNIQUE (model_id)',
         'A configuration with this model already exists. Please use a different model.')
    ]

    @api.onchange('model_id')
    def clear_fields(self):
        self.fields_ids = False
