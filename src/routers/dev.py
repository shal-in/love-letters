import collections

from firebase_admin import firestore  # type: ignore[import-untyped]
from flask import Blueprint, Response, jsonify

dev_bp = Blueprint("dev", __name__, url_prefix="/dev")


@dev_bp.get("/counts")
def counts() -> tuple[Response, int]:
    db = firestore.client()
    letter_views_count_results = db.collection("view_logs").where("page", "!=", "/index").count().get()
    letter_views = letter_views_count_results[0][0].value if letter_views_count_results else 0

    letter_submissions_count_results = db.collection("letters").count().get()
    letters_count = letter_submissions_count_results[0][0].value if letter_submissions_count_results else 0

    shares_count_results = db.collection("share_logs").count().get()
    shares_count = shares_count_results[0][0].value if shares_count_results else 0

    return jsonify(
        dict(
            letter_views=letter_views,
            letters_count=letters_count,
            shares_count=shares_count,
        )
    ), 200


@dev_bp.get("/details")
def details() -> tuple[Response, int]:
    db = firestore.client()

    letter_view_logs_ref = db.collection("view_logs").where("page", "!=", "/index")
    letter_view_logs = letter_view_logs_ref.stream()

    views_by_letter: dict[str, int] = collections.defaultdict(int)
    for view_log in letter_view_logs:
        dict_ = view_log.to_dict()
        views_by_letter[dict_["page"]] += 1

    letter_share_logs_ref = db.collection("share_logs")
    letter_share_logs = letter_share_logs_ref.stream()

    shares_by_letter: dict[str, int] = collections.defaultdict(int)
    for letter in letter_share_logs:
        dict_ = letter.to_dict()
        shares_by_letter[dict_["letter_id"]] += 1

    return jsonify(dict(views=views_by_letter, shares=shares_by_letter)), 200
