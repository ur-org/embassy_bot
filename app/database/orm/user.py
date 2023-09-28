from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from .core.types import bool_false, str_36, int

from sqlalchemy.orm import Mapped, relationship

from .core import ORMModel, mixins

if TYPE_CHECKING:
    from .user_url import UserUrlModel


class UserModel(
    mixins.NameMixin, ORMModel,
):
    tg_id: Mapped[int]
    tg_username: Mapped[Optional[str_36]]
    is_admin: Mapped[bool_false]
    is_member: Mapped[bool_false]

    urls: Mapped[Optional[List[UserUrlModel]]] = relationship(back_populates='user')
