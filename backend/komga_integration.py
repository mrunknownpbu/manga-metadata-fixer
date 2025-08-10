"""
Komga Integration: Functions to interact with the Komga API for metadata updates.
"""

import os
import requests

KOMGA_API_URL = os.getenv("KOMGA_API_URL", "http://localhost:8080/api")
KOMGA_API_TOKEN = os.getenv("KOMGA_API_TOKEN")

def update_komga_metadata(series_id, metadata):
    """
    Update Komga metadata for a given series ID.
    """
    if not KOMGA_API_TOKEN:
        raise RuntimeError("KOMGA_API_TOKEN is not set")
    headers = {
        "Authorization": f"Bearer {KOMGA_API_TOKEN}",
        "Content-Type": "application/json"
    }
    url = f"{KOMGA_API_URL}/v1/series/{series_id}/metadata"
    response = requests.patch(url, json=metadata, headers=headers)
    response.raise_for_status()
    return response.json()