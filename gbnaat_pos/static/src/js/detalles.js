odoo.define('gbnaat_pos.OrderlineCustomerNoteButton_extension', function (require) {
    'use strict';
    const OrderlineCustomerNoteButton = require('point_of_sale.OrderlineCustomerNoteButton');
    const Registries = require('point_of_sale.Registries');
    const CustomerNoteButton = OrderlineCustomerNoteButton => class extends OrderlineCustomerNoteButton {

        get enable_detalles() {
            if (this.env.pos.config.module_pos_hr) {
                const cashierId = this.env.pos.get_cashier().id;
                const sessionAccess = this.env.pos.session_access.find(access => access.id === cashierId);
                if (sessionAccess && sessionAccess.enable_detalles) {
                    self.$('#detalles_disable').css({ "display": "none" });
                }
                else {
                    self.$('#detalles_enable').css({ "display": "none" });
                }
                return sessionAccess ? sessionAccess.enable_detalles : false;
            }
            else { return false; }
        }

    };
    Registries.Component.extend(OrderlineCustomerNoteButton, CustomerNoteButton);
    return OrderlineCustomerNoteButton;
});
