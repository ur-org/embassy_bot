from __future__ import annotations

from sqlalchemy.orm import Mapped

from ..constraints import url_id_fk
from ..types import url_id_fk_type


class UrlIDMixin:
    url_id: Mapped[url_id_fk_type] = url_id_fk
