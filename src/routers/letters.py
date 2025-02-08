import json

from firebase_admin import firestore  # type: ignore[import-untyped]
from flask import Blueprint, Response, jsonify, request
from google.cloud.firestore import (  # type: ignore[import-untyped]
    DocumentReference,
)

from src.letter import get_latest_letter
from src.utils import dt_now, get_request_ip

letters_bp = Blueprint("letters", __name__, url_prefix="/letters")


@letters_bp.post("/")
def create_letter() -> tuple[Response, int]:
    now = dt_now()
    ip = get_request_ip(request)
    raw_data = request.data

    db = firestore.client()

    latest_letter = get_latest_letter(db)
    new_id = str(int(latest_letter.id) + 1)

    new_letter_doc: DocumentReference = db.collection("letters").document(new_id)

    new_letter_doc.set(
        dict(
            created_at=now,
            raw=json.loads(raw_data.decode("utf-8")),
            ip=ip,
        )
    )

    return jsonify(dict(id=new_id, created_at=now)), 201
