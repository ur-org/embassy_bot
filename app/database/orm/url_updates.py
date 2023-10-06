from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, relationship

from .core import ORMModel, mixins
from .core.types import bool_no_value, bool_false, int

if TYPE_CHECKING:
    from .user_url import UserUrlModel


class UrlUpdateModel(
    mixins.UrlIDMixin,
    ORMModel,
):
    status: Mapped[Optional[bool_no_value]]
    is_error: Mapped[bool_false]
    timestamp: Mapped[Optional[int]]

    url: Mapped[Optional[UserUrlModel]] = relationship(back_populates="statuses")
