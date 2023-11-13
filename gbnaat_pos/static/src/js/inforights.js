odoo.define('gbnaat_pos.InfoButton_extension', function (require) {
    'use strict';
    const ProductInfoButton = require('point_of_sale.ProductInfoButton');
    const Registries = require('point_of_sale.Registries');
    const inforights = ProductInfoButton => class extends ProductInfoButton {

        get disable_info() {
            if (this.env.pos.config.module_pos_hr) {
                const cashierId = this.env.pos.get_cashier().id;
                const sessionAccess = this.env.pos.session_access.find(access => access.id === cashierId);
                if (sessionAccess && sessionAccess.disable_info) {
                    self.$("#info_disable").css({ "display": "none" });
                }
                return sessionAccess ? sessionAccess.disable_info : false;
            }
            else { return false; }
        }
    };
    Registries.Component.extend(ProductInfoButton, inforights);
    return ProductInfoButton;
});
