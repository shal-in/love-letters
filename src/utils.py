import datetime as dt
import uuid

from flask import Request


def new_uid(prefix: str):
    return f"{prefix}:{str(uuid.uuid4())[:8]}"


def dt_now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_request_ip(request: Request) -> str:
    forwarded_ip = request.headers.get("X-Forwarded-For", None)

    if not forwarded_ip:
        return request.remote_addr if request.remote_addr else "no-ip"

    return forwarded_ip
