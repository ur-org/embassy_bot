import httpx
from typing import Any

from app.logger import logger
from app.settings import application_settings


def get_schedule_update(tg_id: int, url: str) -> Any:
    try:
        response = httpx.post(
            url=f"{application_settings.embassy_service_url}/get_update",
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
    except Exception as e:
        logger.critical(
            f"Critical error - {e}",
            exc_info=False,
        )


def get_image(tg_id: int, timestamp: int) -> str:
    try:
        url = f"{application_settings.embassy_service_url}/images/{tg_id}/{timestamp}/final.png"
        response = httpx.get(url=url)
        return response.content
    except httpx.HTTPError as e:
        logger.critical(
            f"Critical error caused by {e.request.url} - {e}", exc_info=False
        )
