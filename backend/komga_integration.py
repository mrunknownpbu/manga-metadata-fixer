"""
Komga Integration: Functions to interact with the Komga API for metadata updates.

This module provides functionality to update manga series metadata in Komga
through its REST API.
"""

import os
import logging
from typing import Dict, Any, Optional

import requests
from requests.exceptions import RequestException, HTTPError, Timeout


logger = logging.getLogger(__name__)


class KomgaAPIError(Exception):
    """Custom exception for Komga API related errors."""
    pass


class KomgaIntegration:
    """Handler for Komga API interactions."""

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_token: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize Komga integration.

        Args:
            api_url: Komga API base URL
            api_token: Komga API authentication token
            timeout: Request timeout in seconds
        """
        self.api_url = api_url or os.getenv(
            "KOMGA_API_URL",
            "http://localhost:8080/api"
        )
        self.api_token = api_token or os.getenv("KOMGA_API_TOKEN")
        self.timeout = timeout

        if not self.api_token:
            raise KomgaAPIError("KOMGA_API_TOKEN is not set")

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "User-Agent": "manga-metadata-fixer/1.0"
        }

    def update_series_metadata(
        self,
        series_id: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update Komga metadata for a given series ID.

        Args:
            series_id: The series ID in Komga
            metadata: Metadata dictionary to update

        Returns:
            Response data from Komga API

        Raises:
            KomgaAPIError: If the API request fails
        """
        if not series_id:
            raise ValueError("series_id cannot be empty")

        if not metadata:
            raise ValueError("metadata cannot be empty")

        url = f"{self.api_url}/v1/series/{series_id}/metadata"
        headers = self._get_headers()

        try:
            logger.info(f"Updating Komga series metadata for ID: {series_id}")
            response = requests.patch(
                url,
                json=metadata,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()

            logger.info(f"Successfully updated metadata for series: {series_id}")
            return response.json()

        except HTTPError as e:
            error_msg = f"HTTP error updating Komga metadata: {e}"
            logger.error(error_msg)
            raise KomgaAPIError(error_msg) from e

        except Timeout as e:
            error_msg = f"Timeout updating Komga metadata: {e}"
            logger.error(error_msg)
            raise KomgaAPIError(error_msg) from e

        except RequestException as e:
            error_msg = f"Request error updating Komga metadata: {e}"
            logger.error(error_msg)
            raise KomgaAPIError(error_msg) from e


# Backward compatibility function
def update_komga_metadata(series_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update Komga metadata for a given series ID.

    This is a convenience function that creates a KomgaIntegration instance
    and calls update_series_metadata.

    Args:
        series_id: The series ID in Komga
        metadata: Metadata dictionary to update

    Returns:
        Response data from Komga API
    """
    integration = KomgaIntegration()
    return integration.update_series_metadata(series_id, metadata)
