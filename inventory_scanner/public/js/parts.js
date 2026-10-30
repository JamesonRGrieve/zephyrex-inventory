frappe.ui.form.on("Asset Capitalization", {
  refresh(frm) {
    if (frm.doc.docstatus === 0) {
      frm.add_custom_button(__("Add Parts"), () => {      
        let popup = new frappe.ui.Dialog({
          title: ("Add Parts"),
          fields: [
            {
              label: ("Item Code"),
              fieldname: "item_code",
              fieldtype: "Link",
              options: "Item",
              reqd: 1,
              get_query: function() {
                return {
                  filters: {
                    "is_stock_item": 1,
                    "is_fixed_asset": 0
                  }
                };
              }
            },
            {
              label: ("Warehouse"),
              fieldname: "warehouse",
              fieldtype: "Link",
              options: "Warehouse",
              reqd: 1
            },
            {
              label: ("Quantity"),
              fieldname: "qty",
              fieldtype: "Float",
              default: 1.0,
              reqd: 1
            }
          ],
          primary_action_label: ("Add Parts"),
          primary_action(values) {
              let new_row = frm.add_child("stock_items");
              new_row.item_code = values.item_code;
              new_row.warehouse = values.warehouse;
              new_row.qty = values.qty;
              
              frm.refresh_field("stock_items");
              popup.hide();
          }
        });
        popup.show();
      });
    }
  }
});


frappe.ui.form.on("Asset Capitalization", {
  refresh(frm) {
    if (frm.doc.docstatus === 0) { 
      frm.add_custom_button(("Remove Parts"), () => {
        let items_in_table = (frm.doc.stock_items || []).map(row => {
          return {
            label: `${row.item_code}`,
            value: row.name
          };
        });
        if (items_in_table.length === 0) {
          frappe.msgprint(("No Parts added."));
          return;
        }
        let popup = new frappe.ui.Dialog({
          title: ("Remove Parts"),
          fields: [
            {
              label: ("Select Part"),
              fieldname: "row_id",
              fieldtype: "Select",
              options: items_in_table,
              reqd: 1
            }
          ],
          primary_action_label: __("Remove Part"),
          primary_action(values) {
            frappe.model.clear_doc(frm.doc.stock_items.find(row => row.name === values.row_id).doctype, values.row_id);
            frm.refresh_field("stock_items");
            frm.dirty();
            popup.hide();
          }
        });
        popup.show();
      });
    }
  }
});