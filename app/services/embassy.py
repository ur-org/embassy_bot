import httpx
from typing import Any

from app.settings import application_settings


def get_schedule_update(tg_id: int, url: str) -> Any:
    response = httpx.post(
        f"{application_settings.embassy_service_url}/get_update",
        data={
            "tg_id": tg_id,
            "url": url,
        },
    )

    return response.json()
