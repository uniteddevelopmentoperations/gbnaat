odoo.define('gbnaat_pos.PrintBillButton_extension', function (require) {
    'use strict';
    const PrintBillButton = require('pos_restaurant.PrintBillButton');
    const Registries = require('point_of_sale.Registries');
    const BillButton = PrintBillButton => class extends PrintBillButton {

        get enable_preimpresion() {
            if (this.env.pos.config.module_pos_hr) {
                const cashierId = this.env.pos.get_cashier().id;
                const sessionAccess = this.env.pos.session_access.find(access => access.id === cashierId);
                if (sessionAccess && sessionAccess.enable_preimpresion) {
                    self.$('#preimpresion_disable').css({ "display": "none" });
                }
                else {
                    self.$('#preimpresion_enable').css({ "display": "none" });
                }
                return sessionAccess ? sessionAccess.enable_preimpresion : false;
            }
            else { return false; }
        }

    };
    Registries.Component.extend(PrintBillButton, BillButton);
    return PrintBillButton;
});
