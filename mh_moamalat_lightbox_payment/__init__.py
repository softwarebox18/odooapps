# Part of Odoo. See LICENSE file for full copyright and licensing details.

from . import controllers
from . import models

from odoo.addons.payment import setup_provider, reset_payment_provider


def post_init_hook(env):
    # Register Moamalat LightBox provider after module installation
    setup_provider(env, 'moamalat_lightbox')


def uninstall_hook(env):
    # Reset Moamalat LightBox provider when module is uninstalled
    reset_payment_provider(env, 'moamalat_lightbox')
