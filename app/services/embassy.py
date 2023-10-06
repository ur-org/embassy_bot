import httpx
from typing import Any

from app.logger import logger
from app.settings import application_settings


def get_schedule_update(tg_id: int, url: str) -> Any:
    try:
        response = httpx.post(
            f"{application_settings.embassy_service_url}/get_update",
            json={
                "tg_id": tg_id,
                "url": url,
            },
        )
        return response.json()
    except httpx.HTTPError as e:
        logger.critical(
            f"Critical error caused by {e.request.url} - {e}", exc_info=False
        )
