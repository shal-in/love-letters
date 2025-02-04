import datetime
import json
import random

from flask import redirect, request, jsonify, Response, Blueprint, url_for
import firebase_admin  # type: ignore[import-untyped]
from firebase_admin import firestore

import errors  # type: ignore[import-not-found]

from google.cloud.firestore import (  # type: ignore[import-untyped]
    DocumentReference,
    Client as FirestoreClient,
    DocumentSnapshot,
    Query,
)


firebase_admin.initialize_app()

letters_bp = Blueprint("letters", __name__)


@letters_bp.post("/")
def create_letter() -> tuple[Response, int]:
    raw_data = request.data

    fs_client = firestore.client()

    latest_letter = _get_latest_letter(fs_client)
    new_id = str(int(latest_letter.id) + 1)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_letter_doc: DocumentReference = fs_client.collection("letters").document(new_id)

    new_letter_doc.set(
        dict(
            created_at=now,
            raw=json.loads(raw_data.decode("utf-8")),
            id=new_id,
            ip=request.remote_addr if request.remote_addr else "",
        )
    )

    return jsonify(dict(id=new_id, created_at=now)), 201


@letters_bp.get("/<letter_id>")
def get(letter_id: str):
    fs_client = firestore.client()
    letter: DocumentSnapshot = fs_client.collection("letters").document(letter_id).get()

    if not letter:
        raise errors.LetterNotfound

    letter = letter.to_dict()

    letter_data = {"id": letter_id, "raw": letter["raw"]}

    return jsonify(letter_data), 200


@letters_bp.get("/random")
def random_letter():
    fs_client = firestore.client()
    latest_letter = _get_latest_letter(fs_client)
    latest_id = int(latest_letter.id)
    random_letter_id = random.randrange(1, latest_id)

    return redirect(url_for("letters.get", letter_id=random_letter_id))


def _get_latest_letter(fs_client: FirestoreClient) -> DocumentSnapshot:
    query = fs_client.collection("letters").order_by("created_at", direction=Query.DESCENDING).limit(1)
    return next(iter(query.stream()))


# @app.route("/api/ping-image-share")
# def ping_image_share() -> None:
#     pass


# @app.route("/api/ping-text-share")
# def ping_text_share() -> None:
#     pass
