"""
Main entry point for the Manga Metadata Fixer backend.
Handles integration with Komga and Kavita.
"""

from flask import Flask, request, jsonify
import os

from komga_integration import update_komga_metadata
from kavita_integration import update_kavita_metadata

app = Flask(__name__)

@app.route("/update/komga", methods=["POST"])
def update_komga():
    data = request.json
    series_id = data.get("series_id")
    metadata = data.get("metadata")
    try:
        result = update_komga_metadata(series_id, metadata)
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400

@app.route("/update/kavita", methods=["POST"])
def update_kavita():
    data = request.json
    series_id = data.get("series_id")
    metadata = data.get("metadata")
    try:
        result = update_kavita_metadata(series_id, metadata)
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 1996)))