odoo.define('gbnaat_pos.OrderlineNoteButton_extension', function (require) {
    'use strict';
    const OrderlineNoteButton = require('pos_restaurant.OrderlineNoteButton');
    const Registries = require('point_of_sale.Registries');
    const folioButton = OrderlineNoteButton => class extends OrderlineNoteButton {

        get enable_folio() {
            if (this.env.pos.config.module_pos_hr) {
                const cashierId = this.env.pos.get_cashier().id;
                const sessionAccess = this.env.pos.session_access.find(access => access.id === cashierId);
                if (sessionAccess && sessionAccess.enable_folio) {
                    self.$('#folio_disable').css({ "display": "none" });
                }
                else {
                    self.$('#folio_enable').css({ "display": "none" });
                }
                return sessionAccess ? sessionAccess.enable_folio : false;
            }
            else { return false; }
        }

    };
    Registries.Component.extend(OrderlineNoteButton, folioButton);
    return OrderlineNoteButton;
});
