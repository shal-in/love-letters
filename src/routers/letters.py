import datetime as dt
import json

from firebase_admin import firestore  # type: ignore[import-untyped]
from flask import Blueprint, Response, jsonify, request
from google.cloud.firestore import (  # type: ignore[import-untyped]
    DocumentReference,
)

from src.letter import get_latest_letter

letters_bp = Blueprint("letters", __name__, url_prefix="/letters")


@letters_bp.post("/")
def create_letter() -> tuple[Response, int]:
    forwarded_header = request.headers.get("X-Forwarded-For")
    print(forwarded_header)

    raw_data = request.data

    fs_client = firestore.client()

    latest_letter = get_latest_letter(fs_client)
    new_id = str(int(latest_letter.id) + 1)

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
