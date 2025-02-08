from firebase_admin import firestore  # type: ignore[import-untyped]
from flask import Blueprint, Response, jsonify

dev_bp = Blueprint("dev", __name__, url_prefix="/dev")


@dev_bp.get("/all_views")
def all_views() -> tuple[Response, int]:
    db = firestore.client()
    all_views_count = db.collection("view_logs").count().get()
    return jsonify(dict(all_views=all_views_count[0][0].value if all_views_count else 0)), 200


@dev_bp.get("/index_views")
def index_views() -> tuple[Response, int]:
    db = firestore.client()
    index_views_count = db.collection("view_logs").where("page", "==", "/index").count().get()
    return jsonify(dict(index_views=index_views_count[0][0].value if index_views_count else 0)), 200


@dev_bp.get("/letter_views")
def letter_views() -> tuple[Response, int]:
    db = firestore.client()
    letter_views_count = db.collection("view_logs").where("page", "!=", "/index").count().get()
    return jsonify(dict(letter_views=letter_views_count[0][0].value if letter_views_count else 0)), 200


@dev_bp.get("/total_shares")
def total_shares() -> tuple[Response, int]:
    db = firestore.client()
    total_shares = db.collection("share_logs").count().get()
    return jsonify(dict(total_shares=total_shares[0][0].value if total_shares else 0)), 200
