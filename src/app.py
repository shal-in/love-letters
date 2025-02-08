import os

import firebase_admin  # type: ignore[import-untyped]
from flask import Flask, redirect, render_template

from src.letter import get_letter_data, get_random_letter_id, letter_exists, text_to_html
from src.routers.letters import letters_bp
from src.routers.shares import shares_bp

app = Flask(__name__)
app.register_blueprint(letters_bp)
app.register_blueprint(shares_bp)

firebase_admin.initialize_app()

# @app.after_request
# def log_details(response: Response) -> Response:
#     print(response)

#     return response


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/write")
def write():
    return render_template("write.html")


@app.get("/read")
def read():
    random_letter_id = get_random_letter_id()
    return redirect(f"/{random_letter_id}")


@app.get("/<letter_id>")
def letter(letter_id: str):
    if not letter_exists(letter_id):
        return redirect("/")

    letter_data = get_letter_data(letter_id)
    letter_html = text_to_html(letter_data.raw)

    return render_template("letter.html", letter=letter_html, letter_id=letter_id)


@app.get("/coming-soon")
def coming_soon():
    return render_template("coming-soon.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
