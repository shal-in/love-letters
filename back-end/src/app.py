import msgspec
import json
import os

from flask import Flask, render_template, redirect, request, jsonify
from firebase_admin import initialize_app

from letter import Letter, store_letter


initialize_app()

base_dir = os.path.abspath(os.path.dirname(__file__))

template_dir = os.path.join(base_dir, "../../templates")

app = Flask(__name__, template_folder=template_dir)


@app.route("/")
def index():
    return redirect("/coming-soon")


@app.route("/write")
def write():
    return render_template("write.html")


@app.route("/read")
def read():
    # GET RANDOM LETTER ID from db, redirect to letter id

    letter_id = 1234
    return redirect("/1234")


@app.route("/<letter_id>")
def letter(letter_id):
    # Check if letter_id in db (if not but letter is still a number, redirect to /read, else redirect to /)
    # get letter from db (HTML thing)
    # Return html (line below)
    # return render_template("letter.html", letter=letter, letter_id=1234)

    return (redirect("/"))


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

    return dict(
        id=new_id,
        created_at=created_at
    )

# # Catch-all route to redirect everything else to /coming-soon
# @app.route("/<path:path>")
# def catch_all(path):
#     return redirect("/coming-soon")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
