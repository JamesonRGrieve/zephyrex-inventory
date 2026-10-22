import os
import requests


class ERPNextClient:
    def __init__(self):
        self.url = os.environ["ERP_URL"].rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": (
                f"token {os.environ['ERP_API_KEY']}:"
                f"{os.environ['ERP_API_SECRET']}"
            ),
            "Content-Type": "application/json"
        })

    def request(self, method, path, **kwargs):
        response = self.session.request(
            method,
            f"{self.url}{path}",
            timeout=20,
            **kwargs
        )
        response.raise_for_status()

        result = response.json()

        if result.get("exc_type") or result.get("exc"):
            raise RuntimeError(
                f"ERPNext error: {result}"
            )

        return result

    def get_item(self, item_code):
        from urllib.parse import quote

        code = quote(item_code, safe="")

        result = self.request(
            "GET",
            f"/api/resource/Item/{code}"
        )

        return result["data"]

    def get_stock_qty(self, item_code, warehouse):
        result = self.request(
            "GET",
            "/api/resource/Bin",
            params={
                "filters": __import__("json").dumps([
                    ["item_code", "=", item_code],
                    ["warehouse", "=", warehouse]
                ]),
                "fields": '["actual_qty"]',
                "limit_page_length": 1
            }
        )

        rows = result["data"]

        return rows[0]["actual_qty"] if rows else 0

    def create_transfer(
        self,
        item_code,
        source,
        destination,
        qty,
        company
    ):
        document = {
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Transfer",
            "company": company,
            "items": [
                {
                    "item_code": item_code,
                    "qty": qty,
                    "s_warehouse": source,
                    "t_warehouse": destination
                }
            ]
        }

        result = self.request(
            "POST",
            "/api/resource/Stock Entry",
            json=document
        )

        return result["data"]["name"]

    def submit_transfer(self, entry_name):
        result = self.request(
            "POST",
            "/api/method/frappe.client.submit",
            json={
                "doc": {
                    "doctype": "Stock Entry",
                    "name": entry_name
                }
            }
        )

        return result["message"]