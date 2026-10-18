import os
import httpx
from fastapi import HTTPException

class ERPNextClient:
  def __init__(self):
    self.base_url = os.getenv("ERPNEXT_URL")
    api_key = os.getenv("ERPNEXT_API_KEY")
    api_secret = os.getenv("ERPNEXT_API_SECRET")
    
    if not all([self.base_url, api_key, api_secret]):
      raise RuntimeError(".env file not configured.")
        
    self.headers = {
      "Authorization": f"token {api_key}:{api_secret}",
      "Content-Type": "application/json",
      "Accept": "application/json"
    }

  async def searchItem(self, item_code: str):
    url = f"{self.base_url}/api/resource/Item/{item_code}"
    
    async with httpx.AsyncClient() as client:
      response = await client.get(url, headers=self.headers)
      
      if response.status_code == 200:
        return response.json().get("data")
      elif response.status_code == 404:
        return None
          
      raise HTTPException(
        status_code=response.status_code, 
        detail=f"ERPNext integration error: {response.text}"
      )