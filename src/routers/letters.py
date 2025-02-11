import json
import time

from firebase_admin import firestore  # type: ignore[import-untyped]
from flask import Blueprint, Response, jsonify, request
from google.cloud.firestore import (  # type: ignore[import-untyped]
    DocumentReference,
)

from src.ip import get_request_ip
from src.letter import get_latest_letter
from src.utils import dt_now

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


@letters_bp.post("/test")
def test_create_letter() -> tuple[Response, int]:
    raw_data = request.data

    print(raw_data)

    time.sleep(3)

    return jsonify(dict(id=3)), 201
