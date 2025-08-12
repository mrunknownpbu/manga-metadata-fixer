"""
Main entry point for the Manga Metadata Fixer backend.

This Flask application provides REST API endpoints for updating manga metadata
in both Komga and Kavita systems.
"""

import os
import logging

from flask import Flask, request, jsonify

from komga_integration import update_komga_metadata, KomgaAPIError
from kavita_integration import update_kavita_metadata, KavitaAPIError


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "status": "error",
        "error": "Endpoint not found",
        "code": 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "status": "error",
        "error": "Internal server error",
        "code": 500
    }), 500


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "success",
        "message": "Manga Metadata Fixer API is running",
        "version": "1.0.0"
    })


@app.route("/update/komga", methods=["POST"])
def update_komga():
    """
    Update metadata for a series in Komga.

    Expected JSON payload:
    {
        "series_id": "string",
        "metadata": {
            "title": "string",
            "summary": "string",
            "status": "string",
            ...
        }
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "error": "No JSON data provided"
            }), 400

        series_id = data.get("series_id")
        metadata = data.get("metadata")

        if not series_id:
            return jsonify({
                "status": "error",
                "error": "series_id is required"
            }), 400

        if not metadata:
            return jsonify({
                "status": "error",
                "error": "metadata is required"
            }), 400

        logger.info(f"Received Komga update request for series: {series_id}")
        result = update_komga_metadata(series_id, metadata)

        return jsonify({
            "status": "success",
            "message": "Komga metadata updated successfully",
            "result": result
        })

    except KomgaAPIError as e:
        logger.error(f"Komga API error: {e}")
        return jsonify({
            "status": "error",
            "error": f"Komga API error: {str(e)}"
        }), 400

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({
            "status": "error",
            "error": f"Validation error: {str(e)}"
        }), 400

    except Exception as e:
        logger.error(f"Unexpected error in Komga update: {e}")
        return jsonify({
            "status": "error",
            "error": "An unexpected error occurred"
        }), 500


@app.route("/update/kavita", methods=["POST"])
def update_kavita():
    """
    Update metadata for a series in Kavita.

    Expected JSON payload:
    {
        "series_id": "string",
        "metadata": {
            "name": "string",
            "summary": "string",
            "publicationStatus": "string",
            ...
        }
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "error": "No JSON data provided"
            }), 400

        series_id = data.get("series_id")
        metadata = data.get("metadata")

        if not series_id:
            return jsonify({
                "status": "error",
                "error": "series_id is required"
            }), 400

        if not metadata:
            return jsonify({
                "status": "error",
                "error": "metadata is required"
            }), 400

        logger.info(f"Received Kavita update request for series: {series_id}")
        result = update_kavita_metadata(series_id, metadata)

        return jsonify({
            "status": "success",
            "message": "Kavita metadata updated successfully",
            "result": result
        })

    except KavitaAPIError as e:
        logger.error(f"Kavita API error: {e}")
        return jsonify({
            "status": "error",
            "error": f"Kavita API error: {str(e)}"
        }), 400

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({
            "status": "error",
            "error": f"Validation error: {str(e)}"
        }), 400

    except Exception as e:
        logger.error(f"Unexpected error in Kavita update: {e}")
        return jsonify({
            "status": "error",
            "error": "An unexpected error occurred"
        }), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 1996))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    logger.info(f"Starting Manga Metadata Fixer API on port {port}")
    logger.info(f"Debug mode: {debug}")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )
