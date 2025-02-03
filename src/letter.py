import random
import typing as t
import msgspec
import datetime
import json

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
    raw: dict[str, t.Any]


def _get_latest_letter(fs_client: FirestoreClient) -> DocumentSnapshot:
    query = (
        fs_client.collection("letters")
        .order_by("created_at", direction=Query.DESCENDING)
        .limit(1)
    )
    return next(iter(query.stream()))


def store_letter(raw_data: bytes, letter: Letter, ip: str | None) -> tuple[str, str]:
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


def get_letter_by_id(id: str) -> DocumentSnapshot | None:
    fs_client = firestore.client()
    letter: DocumentSnapshot = fs_client.collection("letters").document(id).get()

    if not letter.exists:
        return None

    return letter


def letter_exists(id: str) -> bool:
    fs_client = firestore.client()
    letter: DocumentSnapshot = fs_client.collection("letters").document(id).get()

    return letter.exists


def get_letter_data_for_read(id: str) -> dict | None:
    letter = get_letter_by_id(id)

    if not letter:
        return None

    letter = letter.to_dict()

    letter_data = {"id": id, "raw": letter["raw"]}

    return letter_data
