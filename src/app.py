import os

from flask import Flask, render_template, redirect

from routers.letters import letters_bp

from utils import letter_exists


app = Flask(__name__)

app.register_blueprint(letters_bp, url_prefix="/letters")


@app.route("/")
def index():
    # return redirect("/coming-soon")

    return render_template("index.html")


@app.route("/write")
def write():
    return render_template("write.html")


@app.route("/coming-soon")
def coming_soon():
    return render_template("coming-soon.html")


@app.route("/<letter_id>")
def letter(letter_id: str):
    if not letter_exists(letter_id):
        return redirect("/")

    return render_template("letter.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
