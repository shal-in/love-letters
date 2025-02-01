import typing as t
import msgspec
import datetime

from google.cloud.firestore import Query
from firebase_admin import firestore
from google.cloud.firestore_v1.document import DocumentReference


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


def get_html(letter: Letter):
    to_ = letter.to if letter.to else "Anonymous"
    from_ = letter.from_ if letter.from_ else "Anonymous"
    p_tags = [
        f'<p>To <span class="to">{to_}</span>, from <span class="from">{from_}</span></p>'
    ]

    stripped_text = letter.text.strip()
    p_tags.extend([f"<p>{p.strip()}</p>" for p in stripped_text.split("\n") if p.strip()])
    return "\n".join(p_tags)


def store_letter(raw_data: bytes, letter: Letter, ip: str) -> tuple[int, datetime.datetime]:
    html = get_html(letter)

    fs_client = firestore.client()

    query = fs_client.collection("letters").order_by("__name__", direction=Query.DESCENDING).limit(1)
    letter = next(iter(query.stream()))


    new_id = str(int(letter.id) + 1)
    now = datetime.datetime.now()

    new_letter_doc: DocumentReference = fs_client.collection("letters").document(new_id)

    new_letter_doc.set(
        dict(
            created_at=now,
            raw=raw_data,
            html=html,
            ip=ip,
        )
    )

    return new_id, now
