import typing as t
import msgspec
import json
import os

from flask import Flask, render_template, redirect, request, jsonify, Response
from firebase_admin import initialize_app  # type: ignore[import-untyped]

import errors as errors
from letter import (
    Letter,
    store_letter,
    get_random_letter_id,
    get_letter_by_id,
    get_letter_data_for_read,
    letter_exists,
)


initialize_app()

app = Flask(__name__)


@app.route("/")
def index():
    return redirect("/coming-soon")


@app.route("/write")
def write():
    return render_template("write.html")


@app.route("/read")
def read():
    random_letter_id = get_random_letter_id()
    return redirect(f"/{random_letter_id}")


@app.route("/coming-soon")
def coming_soon():
    return render_template("coming-soon.html")


@app.route("/<letter_id>")
def letter(letter_id: str):
    if not letter_exists(letter_id):
        return redirect("/")

    return render_template("letter.html")


# API
@app.route("/api/write", methods=["POST"])
def create_letter() -> tuple[Response, int]:
    raw_data = request.data

    try:
        letter_data = msgspec.json.decode(raw_data, type=Letter)
    except json.JSONDecodeError:
        raise errors.InvalidJson

    new_id, created_at = store_letter(raw_data, letter_data, request.remote_addr)

    return jsonify(dict(id=new_id, created_at=created_at)), 201


@app.route("/api/read", methods=["GET"])
def get_letter() -> tuple[Response, int]:
    letter_id = request.args.get("letter_id")

    letter_data = get_letter_data_for_read(letter_id)

    if not letter_data:
        return jsonify({"error": "Letter not found"}), 404

    return jsonify(letter_data), 200


# @app.route("/api/ping-image-share")
# def ping_image_share() -> None:
#     pass


# @app.route("/api/ping-text-share")
# def ping_text_share() -> None:
#     pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
