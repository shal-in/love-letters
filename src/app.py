import os
from flask import Flask, render_template, redirect

from src.letter import get_random_letter_id, letter_exists, get_letter_data, text_to_html

from src.routers.letters import letters_bp

app = Flask(__name__)
app.register_blueprint(letters_bp)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/write")
def write():
    return render_template("write.html")


@app.route("/read")
def read():
    random_letter_id = get_random_letter_id()
    return redirect(f"/{random_letter_id}")


@app.route("/<letter_id>")
def letter(letter_id: str):
    if not letter_exists(letter_id):
        return redirect("/")

    letter_data = get_letter_data(letter_id)
    letter_html = text_to_html(letter_data.raw)

    return render_template("letter.html", letter=letter_html, letter_id=letter_id)


@app.route("/coming-soon")
def coming_soon():
    return render_template("coming-soon.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
