odoo.define('gbnaat_pos.GuestsButton_extension', function (require) {
  'use strict';
  const TableGuestsButton = require('pos_restaurant.TableGuestsButton');
  const Registries = require('point_of_sale.Registries');
  const comensalesrights = TableGuestsButton => class extends TableGuestsButton {

    get disable_comensales() {
      if (this.env.pos.config.module_pos_hr) {
        const cashierId = this.env.pos.get_cashier().id;
        const sessionAccess = this.env.pos.session_access.find(access => access.id === cashierId);
        if (sessionAccess && sessionAccess.disable_comensales) {
          self.$('#comensales_disable').css({ "display": "none" });
        }
        return sessionAccess ? sessionAccess.disable_comensales : false;
      }
      else { return false; }
    }

  };
  Registries.Component.extend(TableGuestsButton, comensalesrights);
  return TableGuestsButton;
});
