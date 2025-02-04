from firebase_admin import firestore  # type: ignore[import-untyped]
from google.cloud.firestore import DocumentSnapshot  # type: ignore[import-untyped]


def letter_exists(id: str) -> bool:
    fs_client = firestore.client()
    letter: DocumentSnapshot = fs_client.collection("letters").document(id).get()

    return letter.exists
