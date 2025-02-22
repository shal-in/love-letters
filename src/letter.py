import random
from dataclasses import dataclass

from firebase_admin import firestore  # type: ignore[import-untyped]
from google.cloud.firestore import (  # type: ignore[import-untyped]
    Client as FirestoreClient,
)
from google.cloud.firestore import (  # type: ignore[import-untyped]
    DocumentSnapshot,
    Query,
)


@dataclass(frozen=True, kw_only=True)
class RawData:
    to: str | None = None
    from_: str | None = None
    text: str


@dataclass(frozen=True, kw_only=True)
class FsLetter:
    id: str
    raw: RawData


def get_latest_letter(db: FirestoreClient) -> DocumentSnapshot:
    query = db.collection("letters").order_by("created_at", direction=Query.DESCENDING).limit(1)
    return next(iter(query.stream()))


def get_random_letter_id() -> str:
    db = firestore.client()

    latest_letter = get_latest_letter(db)

    latest_id = int(latest_letter.id)
    random_id = random.randrange(1, latest_id + 1)

    return str(random_id)


def letter_exists(id: str) -> bool:
    db = firestore.client()
    letter: DocumentSnapshot = db.collection("letters").document(id).get()
    return letter.exists


def get_letter_data(id: str) -> FsLetter:
    db = firestore.client()
    letter: DocumentSnapshot = db.collection("letters").document(id).get()

    letter = letter.to_dict()
    raw = letter["raw"]

    return FsLetter(
        id=id,
        raw=RawData(
            to=raw["to"],
            from_=raw["from"],
            text=raw["text"],
        ),
    )


def text_to_html(raw_data: RawData) -> str:
    to = raw_data.to
    from_ = raw_data.from_
    text = raw_data.text

    if not to:
        to = "Anonymous"

    html = f'<div class="recipients">\n<p class="to">To: <span>{to}</span></p>'

    html += f'<p class="from">'
    if from_:
        html += f"From: <span>{from_}</span>"
    html += f"</p>\n</div>"

    html += f'<div class="letter">\n'

    parags: list = text.split("\n")

    for parag in parags:
        p = f"<p>{parag}</p>"

        html += "\n"
        html += p

    html += f"\n</div>"

    return html
