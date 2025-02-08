import datetime as dt
import uuid

from flask import Request


def new_uid(prefix: str):
    return f"{prefix}:{str(uuid.uuid4())[:8]}"


def dt_now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
