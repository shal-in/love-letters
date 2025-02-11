from firebase_admin import firestore  # type: ignore[import-untyped]
from flask import Blueprint, Response, request
from google.cloud.firestore import (  # type: ignore[import-untyped]
    DocumentReference,
)

from src.ip import get_request_ip
from src.utils import dt_now, new_uid

shares_bp = Blueprint("shares", __name__, url_prefix="/shares")


@shares_bp.get("/<letter_id>")
def create_share_log(letter_id: str) -> Response:
    db = firestore.client()

    now = dt_now()
    share_log_uid = new_uid("share_log")
    ip = get_request_ip(request)

    new_share_log: DocumentReference = db.collection("share_logs").document(share_log_uid)

    new_share_log.set(dict(created_at=now, ip=ip, letter_id=letter_id))

    return Response(status=204)
