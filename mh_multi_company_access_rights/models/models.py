from odoo import models, fields, api

class ResUsersCompanyAccess(models.Model):
    _name = 'res.users.company.access'
    _description = 'User Company Access Rights'

    user_id = fields.Many2one('res.users', string='User', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', required=True, ondelete='cascade')
    group_ids = fields.Many2many('res.groups', string='Groups')

    _sql_constraints = [
        ('unique_user_company', 'unique(user_id, company_id)', 'A user can have only one access entry per company!')
    ]

class ResUsers(models.Model):
    _inherit = 'res.users'

    company_access_ids = fields.One2many('res.users.company.access', 'user_id', string='Company Access')

    @api.model
    def create(self, vals_list):
        users = super(ResUsers, self).create(vals_list)
        for user in users:
            if user.company_access_ids:
                if user.company_id:
                    user.with_context(skip_group_update=True).update_user_groups_for_company(user.id,user.company_id.id)
        return users

    def write(self, vals):
        if self.env.context.get('skip_group_update'):
            return super(ResUsers, self).write(vals)

        res = super(ResUsers, self).write(vals)
        for user in self:
            if user.company_access_ids:
                company_id = vals.get('company_id') or user.company_id.id
                if company_id:
                    user.with_context(skip_group_update=True).update_user_groups_for_company(user.id, company_id)
        return res

    @api.model
    def update_user_groups_for_company(self, user_id, company_id):
        user_obj = self.browse(user_id)
        # print('*********** method called from owl **************', self.env.user.id,user_obj)
        # Check if the current user is an administrator (base.group_system)
        admin_group = self.env.ref('base.group_erp_manager')

        # Skip the logic for admin users
        if admin_group in user_obj.groups_id:
            return

        if company_id:
            self._hide_specific_menus()
            """ Update user groups based on the selected company """
            access_rights = self.env['res.users.company.access'].search([('user_id', '=', user_obj.id), ('company_id', '=', company_id)])

            # Find the Internal User group (base.group_user)
            internal_user_group = self.env.ref('base.group_user')
            # Get the current groups the user is in
            current_groups = user_obj.groups_id
            # Remove all groups except the Internal User group
            groups_to_remove = current_groups - internal_user_group  # Remove all except Internal User group
            if groups_to_remove:
                user_obj.with_context(skip_group_update=True).sudo().write({
                    'groups_id': [(3, group.id) for group in groups_to_remove]
                })
            # user_obj.groups_id = [(3, group.id) for group in groups_to_remove]  # Remove specific groups

            # groups_to_keep = current_groups.filtered(lambda g: g.id == internal_user_group.id)
            # user_obj.groups_id = [(5, 0, 0)]  # Remove all groups
            # user_obj.groups_id = [(4, group.id) for group in groups_to_keep]  # Re-add the Internal User group

            if access_rights:
                # Ensure Internal User group is always included
                new_groups = access_rights.group_ids
                no_one_group = self.env.ref('base.group_no_one')
                if no_one_group in new_groups:
                    menus_to_show = no_one_group.mapped('menu_access')
                    if menus_to_show:
                        # Remove 'No One' group from all menus at once
                        menus_to_show.sudo().write({'groups_id': [(3, no_one_group.id)]})
                # user_obj.groups_id = [(4, group.id) for group in new_groups]
                user_obj.with_context(skip_group_update=True).sudo().write({
                    'groups_id': [(4, group.id) for group in new_groups]
                })

    def _hide_specific_menus(self):
        """Assign specific menus to 'No One' group to hide them from all users."""
        no_one_group = self.env.ref('base.group_no_one')  # Get 'No One' group

        menus_to_hide = [
            self.env.ref("mail.menu_root_discuss"),
            self.env.ref("calendar.mail_menu_calendar"),
            self.env.ref("appointment.main_menu_appointments"),
            self.env.ref("project_todo.menu_todo_todos"),
            self.env.ref("knowledge.knowledge_menu_root"),
            self.env.ref("spreadsheet_dashboard.spreadsheet_dashboard_menu_root"),
            self.env.ref("planning.planning_menu_root"),
            self.env.ref("utm.menu_link_tracker_root"),
            self.env.ref("base.menu_management"),
        ]

        menus_to_hide = [menu.id for menu in menus_to_hide if menu]  # Filter out None values

        if menus_to_hide:
            self.env['ir.ui.menu'].browse(menus_to_hide).sudo().write({'groups_id': [(6, 0, [no_one_group.id])]})
            # (6, 0, [group_id]) replaces all groups with 'No One' group


