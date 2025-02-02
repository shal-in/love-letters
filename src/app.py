import msgspec
import json
import os

from flask import Flask, render_template, redirect, request, jsonify
from firebase_admin import initialize_app

from letter import Letter, store_letter, get_random_letter_id, get_letter_by_id


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


@app.route("/<letter_id>")
def get(letter_id: str):
    # Check if letter_id in db (if not but letter is still a number, redirect to /read, else redirect to /)
    # get letter from db (HTML thing)
    # Return html (line below)
    # return render_template("letter.html", letter=letter, letter_id=1234)
    letter = get_letter_by_id(letter_id)
    return redirect("/")  # TODO: finish this


@app.route("/coming-soon")
def coming_soon():
    return render_template("coming-soon.html")


@app.route("/api/write", methods=["POST"])
def create_letter():
    raw_data = request.data

    try:
        letter_data = msgspec.json.decode(raw_data, type=Letter)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400

    new_id, created_at = store_letter(raw_data, letter_data, request.remote_addr)

    return dict(id=new_id, created_at=created_at)


@app.route("/api/ping-image-share")
def ping_image_share() -> None:
    pass


@app.route("/api/ping-text-share")
def ping_text_share() -> None:
    pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
