from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, relationship

from .core import ORMModel, mixins
from .core.types import bool_no_value

if TYPE_CHECKING:
    from .user_url import UserUrlModel


class UrlUpdateModel(
    mixins.UrlIDMixin, ORMModel,
):
    status: Mapped[bool_no_value]
    url: Mapped[Optional[UserUrlModel]] = relationship(back_populates="statuses")
