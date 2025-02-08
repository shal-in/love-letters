import datetime as dt
import uuid

from firebase_admin import firestore  # type: ignore[import-untyped]
from flask import Blueprint, request
from google.cloud.firestore import (  # type: ignore[import-untyped]
    DocumentReference,
)

shares_bp = Blueprint("shares", __name__, url_prefix="/shares")


def _new_uid():
    return f"share_log:{str(uuid.uuid4())[:8]}"


@shares_bp.get("/<letter_id>")
def share(letter_id: str):
    fs_client = firestore.client()

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    uid = _new_uid()
    new_share_log: DocumentReference = fs_client.collection("share_logs").document(uid)

    new_share_log.set(dict(created_at=now, ip=request.remote_addr if request.remote_addr else "", letter_id=letter_id))

    return ("", 204)
