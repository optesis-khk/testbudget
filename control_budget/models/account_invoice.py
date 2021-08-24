from odoo import fields, models, api, _

class AccountInvoice(models.Model):
    _inherit = "account.invoice.line"

    available =  fields.Float(string='Montant budget restant',compute="_get_available", digits=0 , default="0")

    planned =  fields.Float(string='Montant budget prevu',compute="_get_planned", digits=0 , default="0")

    @api.multi
    @api.depends('account_id','account_analytic_id')
    def _get_available(self):
        for record in self:
            if record.account_id and record.account_analytic_id:
                for line in record.account_analytic_id.crossovered_budget_line:
                    if record.account_id.id in line.general_budget_id.account_ids.ids:
                        record.available = line.available_amount
                        break

    @api.multi
    @api.depends('account_id','account_analytic_id')
    def _get_planned(self):
        for record in self:
            if record.account_id and record.account_analytic_id:
                for line in record.account_analytic_id.crossovered_budget_line:
                    if record.account_id.id in line.general_budget_id.account_ids.ids:
                        record.planned = line.planned_amount
                        break


    @api.onchange('price_subtotal','account_analytic_id')
    def _budget_control(self):
        if self.price_subtotal and self.account_analytic_id:
            ok = self.available - self.price_subtotal
            if ok < 0:
                message = _('Attention votre budget est insuffisant vour effectuer l\'achat')
                mess= {
                            'title': _('Budget insuffisant'),
                            'message' : message
                        }
                return {'warning': mess}
