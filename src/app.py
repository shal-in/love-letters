import os

import firebase_admin  # type: ignore[import-untyped]
from firebase_admin import firestore  # type: ignore[import-untyped]
from flask import Flask, Request, redirect, render_template, request
from flask_cors import CORS
from google.cloud.firestore import DocumentReference  # type: ignore[import-untyped]

from src.ip import get_request_ip
from src.letter import get_letter_data, get_random_letter_id, letter_exists, text_to_html
from src.routers.dev import dev_bp
from src.routers.letters import letters_bp
from src.routers.shares import shares_bp
from src.utils import dt_now, new_uid

app = Flask(__name__)
app.register_blueprint(letters_bp)
app.register_blueprint(shares_bp)
app.register_blueprint(dev_bp)

CORS(app, origins=["https://iwroteyoualoveletter.com"])

firebase_admin.initialize_app()


def _create_view_log(page: str, request: Request) -> None:
    db = firestore.client()

    now = dt_now()
    ip = get_request_ip(request)

    view_log_id = new_uid("view_log")

    log_ref: DocumentReference = db.collection("view_logs").document(view_log_id)
    log_ref.set(dict(page=page, created_at=now, ip=ip))


@app.get("/")
def index():
    _create_view_log("/index", request)

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

    _create_view_log(f"/{letter_id}", request)

    return render_template("letter.html", letter=letter_html, letter_id=letter_id.zfill(4))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
