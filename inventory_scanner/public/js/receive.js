frappe.ui.form.on("Item", {
	refresh(frm) {
		if (frm.is_new()) return;

		frm.add_custom_button(__("Receive"), () => {
			frappe.model.with_doctype("Purchase Receipt", () => {
				const pr = frappe.model.get_new_doc("Purchase Receipt");
				const row = frappe.model.add_child(pr, "items");
				row.item_code = frm.doc.name;
				row.qty = 1;
				frappe.set_route("Form", "Purchase Receipt", pr.name);
			});
		});
	},
});