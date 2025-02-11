import requests
from flask import Request

IP_API_URL = "http://ip-api.com"


def get_request_ip(request: Request) -> str:
    forwarded_ip = request.headers.get("X-Forwarded-For", None)

    if not forwarded_ip:
        return request.remote_addr if request.remote_addr else "no-ip"

    return forwarded_ip


def get_ip_country_code(ip: str) -> str:
    response = requests.request(
        "GET",
        url=f"{IP_API_URL}/json/{ip}",
    )

    if response.status_code != 200:
        return "failed-to-obtain-country_code"

    if response.json()["status"] != "success":
        return response.json()["message"]

    return response.json()["countryCode"]
