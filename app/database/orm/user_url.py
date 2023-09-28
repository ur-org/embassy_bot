from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, relationship

from .core import ORMModel, mixins
from .core.types import text

if TYPE_CHECKING:
    from .user import UserModel


class UserUrlModel(
    mixins.UserIDMixin, ORMModel,
):
    url: Mapped[text]

    user: Mapped[Optional[UserModel]] = relationship(back_populates="urls")
