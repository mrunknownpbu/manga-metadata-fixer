"""
Kavita Integration: Functions to interact with the Kavita API for metadata updates.

This module provides functionality to update manga series metadata in Kavita
through its REST API.
"""

import os
import logging
from typing import Dict, Any, Optional

import requests
from requests.exceptions import RequestException, HTTPError, Timeout


logger = logging.getLogger(__name__)


class KavitaAPIError(Exception):
    """Custom exception for Kavita API related errors."""
    pass


class KavitaIntegration:
    """Handler for Kavita API interactions."""

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_token: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize Kavita integration.

        Args:
            api_url: Kavita API base URL
            api_token: Kavita API authentication token
            timeout: Request timeout in seconds
        """
        self.api_url = api_url or os.getenv(
            "KAVITA_API_URL",
            "http://localhost:5000/api"
        )
        self.api_token = api_token or os.getenv("KAVITA_API_TOKEN")
        self.timeout = timeout

        if not self.api_token:
            raise KavitaAPIError("KAVITA_API_TOKEN is not set")

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
        Update Kavita metadata for a given series ID.

        Args:
            series_id: The series ID in Kavita
            metadata: Metadata dictionary to update

        Returns:
            Response data from Kavita API

        Raises:
            KavitaAPIError: If the API request fails
        """
        if not series_id:
            raise ValueError("series_id cannot be empty")

        if not metadata:
            raise ValueError("metadata cannot be empty")

        url = f"{self.api_url}/Series/{series_id}/metadata"
        headers = self._get_headers()

        try:
            logger.info(f"Updating Kavita series metadata for ID: {series_id}")
            response = requests.put(
                url,
                json=metadata,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()

            logger.info(f"Successfully updated metadata for series: {series_id}")
            return response.json()

        except HTTPError as e:
            error_msg = f"HTTP error updating Kavita metadata: {e}"
            logger.error(error_msg)
            raise KavitaAPIError(error_msg) from e

        except Timeout as e:
            error_msg = f"Timeout updating Kavita metadata: {e}"
            logger.error(error_msg)
            raise KavitaAPIError(error_msg) from e

        except RequestException as e:
            error_msg = f"Request error updating Kavita metadata: {e}"
            logger.error(error_msg)
            raise KavitaAPIError(error_msg) from e


# Backward compatibility function
def update_kavita_metadata(series_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update Kavita metadata for a given series ID.

    This is a convenience function that creates a KavitaIntegration instance
    and calls update_series_metadata.

    Args:
        series_id: The series ID in Kavita
        metadata: Metadata dictionary to update

    Returns:
        Response data from Kavita API
    """
    integration = KavitaIntegration()
    return integration.update_series_metadata(series_id, metadata)
