
import frappe


def get_employee():
    """Find the Employee linked to the logged-in ERPNext user."""

    employee = frappe.db.get_value(
        "Employee",
        {"user_id": frappe.session.user},
        "name"
    )

    if not employee:
        frappe.throw(
            "Your ERPNext user is not linked to an Employee."
        )

    return employee


# ==============================================
# PART 2: ASSET CHECK OUT
# ==============================================

@frappe.whitelist()
def checkout_asset(asset_id):
    """Issue an existing asset to the logged-in employee."""

    if frappe.session.user == "Guest":
        frappe.throw("Please log in first.")

    if not asset_id:
        frappe.throw("Asset ID is required.")

    if not frappe.db.exists("Asset", asset_id):
        frappe.throw("Asset does not exist.")

    asset = frappe.get_doc("Asset", asset_id)
    asset.check_permission("read")

    if asset.docstatus != 1:
        frappe.throw("Asset must be submitted first.")

    if asset.custodian:
        frappe.throw("Asset is already checked out.")

    if not asset.location:
        frappe.throw("Asset has no current location.")

    employee = get_employee()

    movement = frappe.get_doc({
        "doctype": "Asset Movement",
        "purpose": "Issue",
        "company": asset.company,
        "assets": [
            {
                "asset": asset.name,
                "source_location": asset.location,
                "to_employee": employee
            }
        ]
    })

    # Use ERPNext document permission checks.
    movement.insert()
    movement.submit()

    return {
        "success": True,
        "message": "Asset checked out successfully",
        "asset_id": asset.name,
        "employee": employee,
        "movement_id": movement.name,
        "operator": frappe.session.user
    }


# ==============================================
# PART 3: ASSET CHECK IN
# ==============================================

@frappe.whitelist()
def checkin_asset(asset_id):
    """Return an issued asset to the configured location."""

    if frappe.session.user == "Guest":
        frappe.throw("Please log in first.")

    if not asset_id:
        frappe.throw("Asset ID is required.")

    if not frappe.db.exists("Asset", asset_id):
        frappe.throw("Asset does not exist.")

    asset = frappe.get_doc("Asset", asset_id)
    asset.check_permission("read")

    if asset.docstatus != 1:
        frappe.throw("Asset must be submitted first.")

    if not asset.custodian:
        frappe.throw("Asset is not checked out to an employee.")

    location = frappe.conf.get(
        "inventory_scanner_checkin_location"
    )

    if not location:
        frappe.throw(
            "Check-in location is not configured."
        )

    if not frappe.db.exists("Asset Location", location):
        frappe.throw("Destination Asset Location does not exist.")

    movement = frappe.get_doc({
        "doctype": "Asset Movement",
        "purpose": "Receipt",
        "company": asset.company,
        "assets": [
            {
                "asset": asset.name,
                "from_employee": asset.custodian,
                "target_location": location
            }
        ]
    })

    movement.insert()
    movement.submit()

    return {
        "success": True,
        "message": "Asset checked in successfully",
        "asset_id": asset.name,
        "location": location,
        "movement_id": movement.name,
        "operator": frappe.session.user
    }
