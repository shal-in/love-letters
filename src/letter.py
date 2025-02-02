import random
import typing as t
import msgspec
import datetime

from google.cloud.firestore import (  # type: ignore[import-untyped]
    Query,
    Client as FirestoreClient,
    DocumentSnapshot,
    DocumentReference,
)
from firebase_admin import firestore  # type: ignore[import-untyped]


class Letter(msgspec.Struct, kw_only=True):
    to: str | None = None
    from_: str | None = None
    text: str


class FsLetter(msgspec.Struct, kw_only=True):
    id: int
    ip: str
    created_at: datetime.datetime
    html: str
    raw: dict[str, t.Any]


class LetterNotfound(Exception):
    pass


def get_html(letter: Letter):
    to_ = letter.to if letter.to else "Anonymous"
    from_ = letter.from_ if letter.from_ else "Anonymous"
    p_tags = [
        f'<p>To <span class="to">{to_}</span>, from <span class="from">{from_}</span></p>'
    ]

    stripped_text = letter.text.strip()
    p_tags.extend(
        [f"<p>{p.strip()}</p>" for p in stripped_text.split("\n") if p.strip()]
    )
    return "\n".join(p_tags)


def _get_latest_letter(fs_client: FirestoreClient) -> DocumentSnapshot:
    query = (
        fs_client.collection("letters")
        .order_by("__name__", direction=Query.DESCENDING)
        .limit(1)
    )
    return next(iter(query.stream()))


def store_letter(raw_data: bytes, letter: Letter, ip: str | None) -> tuple[str, str]:
    html = get_html(letter)

    fs_client = firestore.client()
    latest_letter = _get_latest_letter(fs_client)

    new_id = str(int(latest_letter.id) + 1)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_letter_doc: DocumentReference = fs_client.collection("letters").document(new_id)

    new_letter_doc.set(
        dict(
            created_at=now,
            raw=raw_data,
            html=html,
            ip=ip if ip else "",
        )
    )

    return new_id, now


def get_random_letter_id() -> str:
    fs_client = firestore.client()

    latest_letter = _get_latest_letter(fs_client)
    latest_id = int(latest_letter.id)
    random_id = random.randrange(1, latest_id)

    return str(random_id)


def get_letter_by_id(id: str) -> DocumentSnapshot:
    fs_client = firestore.client()
    letter: DocumentSnapshot = fs_client.collection("letters").document(id).get()

    if not letter.exists:
        raise LetterNotfound

    return letter
