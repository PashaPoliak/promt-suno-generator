"""
src.py - Flask server that serves camera capture page and publishes screenshots.

Usage:
    python src.py

Opens a camera capture interface at http://localhost:3000
Captured images are saved and displayed in src.html.
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
SCREENSHOT_DIR = BASE_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)


@app.route("/")
def index():
    return send_from_directory(str(BASE_DIR), "src.html")


@app.route("/api/image", methods=["POST"])
def process_image():
    try:
        if "image" not in request.files:
            logger.warning("No image in request")
            return jsonify({"error": "No image"}), 400

        file = request.files["image"]
        img_data = file.read()

        logger.info(f"Image received: name={file.filename}, content_type={file.content_type}, size={len(img_data)} bytes")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{timestamp}.jpg"
        screenshot_path = SCREENSHOT_DIR / filename
        screenshot_path.write_bytes(img_data)

        logger.info(f"Image saved to {screenshot_path}")
        return jsonify({"status": "success", "url": f"/screenshots/{filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/image")
def get_image():
    """Return the most recently captured image."""
    files = sorted(
        [f for f in SCREENSHOT_DIR.iterdir() if f.suffix.lower() in (".jpg", ".jpeg", ".png")],
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not files:
        logger.warning("No image available yet")
        return jsonify({"error": "No image captured yet"}), 404
    latest = files[0]
    logger.info(f"Serving image: {latest}")
    return send_from_directory(str(SCREENSHOT_DIR), latest.name)


@app.route("/images")
def list_images():
    """Return a JSON list of all saved screenshots."""
    files = sorted(
        [f for f in SCREENSHOT_DIR.iterdir() if f.suffix.lower() in (".jpg", ".jpeg", ".png")],
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    images = [{"filename": f.name, "url": f"/screenshots/{f.name}"} for f in files]
    logger.info(f"Listing {len(images)} images")
    return jsonify(images)


@app.route("/screenshots/<path:filename>")
def serve_screenshot(filename):
    return send_from_directory(str(SCREENSHOT_DIR), filename)


if __name__ == "__main__":
    print("Starting server at http://localhost:3000")
    print("Open http://localhost:3000 in a browser to capture a screenshot.")
    app.run(host="0.0.0.0", port=3000, debug=True)
