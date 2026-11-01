import frappe

from .common import (
	create_asset_movement,
	get_asset,
)


@frappe.whitelist()
def checkout_asset(asset_id):
	asset = get_asset(asset_id)

	if asset.custodian:
		frappe.throw("Asset is already checked out.")

	if not asset.location:
		frappe.throw("Asset has no source location.")

	employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")

	if not employee:
		frappe.throw("Logged-in user is not linked to an Employee.")

	result = create_asset_movement(
		asset,
		"Issue",
		{
			"source_location": asset.location,
			"to_employee": employee,
		},
	)

	result["employee"] = employee
	result["message"] = "Asset checked out successfully"

	return result
