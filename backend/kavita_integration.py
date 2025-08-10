"""
Kavita Integration: Functions to interact with the Kavita API for metadata updates.
"""

import os
import requests

KAVITA_API_URL = os.getenv("KAVITA_API_URL", "http://localhost:5000/api")
KAVITA_API_TOKEN = os.getenv("KAVITA_API_TOKEN")

def update_kavita_metadata(series_id, metadata):
    """
    Update Kavita metadata for a given series ID.
    """
    if not KAVITA_API_TOKEN:
        raise RuntimeError("KAVITA_API_TOKEN is not set")
    headers = {
        "Authorization": f"Bearer {KAVITA_API_TOKEN}",
        "Content-Type": "application/json"
    }
    url = f"{KAVITA_API_URL}/Series/{series_id}/metadata"
    response = requests.put(url, json=metadata, headers=headers)
    response.raise_for_status()
    return response.json()