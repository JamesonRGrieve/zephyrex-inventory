frappe.ui.form.on("Asset", {
  refresh(frm) {
    if (frm.is_new()) return;
     
    frm.add_custom_button(__("Install Parts"), () => {
      frappe.model.with_doctype("Asset Capitalization", () => {
        const ip = frappe.model.get_new_doc("Asset Capitalization");
        ip.target_asset = frm.doc.name;
        ip.company = frm.doc.company;
        frappe.set_route("Form", "Asset Capitalization", ip.name);
      });
    });
  },
});