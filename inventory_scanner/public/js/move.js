frappe.ui.form.on("Warehouse", {
	refresh(frm) {
		if (frm.is_new()) return;
		if (frm.doc.is_group) return;

		frm.add_custom_button(__("Move items out"), () => {
			frappe.model.with_doctype("Stock Entry", () => {
				const se = frappe.model.get_new_doc("Stock Entry");
				se.stock_entry_type = "Material Transfer";
				se.from_warehouse = frm.doc.name;
				frappe.set_route("Form", "Stock Entry", se.name);
			});
		});

		frm.add_custom_button(__("Move items in"), () => {
			frappe.model.with_doctype("Stock Entry", () => {
				const se = frappe.model.get_new_doc("Stock Entry");
				se.stock_entry_type = "Material Transfer";
				se.to_warehouse = frm.doc.name;
				frappe.set_route("Form", "Stock Entry", se.name);
			});
		});
	},
});