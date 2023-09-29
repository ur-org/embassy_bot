from __future__ import annotations

from typing import Optional

from .core import ORMSchema, mixins


class UserSchema(
    mixins.NameMixin, ORMSchema
):
    tg_id: int
    tg_username: Optional[str] = None
    is_admin: bool = False
