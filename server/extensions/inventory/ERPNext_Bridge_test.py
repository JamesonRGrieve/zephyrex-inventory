import os
import pytest
from fastapi import HTTPException
from .ERPNext_Bridge import ERPNextClient

pytestmark = pytest.mark.asyncio

async def test_env_file():
    url = os.getenv("ERPNEXT_URL")
    api_key = os.getenv("ERPNEXT_API_KEY")
    api_secret = os.getenv("ERPNEXT_API_SECRET")

    assert url is not None
    assert api_key is not None
    assert api_secret is not None
    assert len(url.strip()) > 0
    assert len(api_key.strip()) > 0
    assert len(api_secret.strip()) > 0

    print(f"\nERPNEXT_URL: {url}")
    print(f"ERPNEXT_API_KEY: {api_key}")
    print(f"ERPNEXT_API_SECRET KEY: {api_secret}")

async def test_item_find():
    item_code = "CMW16GX4M2C3200C16" 
    client = ERPNextClient()
    
    try:
        result = await client.searchItem(item_code)
        
        assert result is not None
        assert "item_name" in result
        assert "stock_uom" in result
        
        print(f"Item: {result['item_name']} ({result['stock_uom']})")

    except HTTPException as e:
        pytest.fail(f"API Connection error. Status code: {e.status_code}, Detail: {e.detail}")
    except Exception as e:
        pytest.fail(f"Failed to connect to ERPNext: {str(e)}")