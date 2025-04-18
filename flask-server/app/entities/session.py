from dataclasses import dataclass
from datetime import datetime


@dataclass
class Session:
    def __init__(
            self,
            user_id: int,
            role: str,
            token: str,
            expires_at: datetime,
            created_at: datetime | None = None,
            session_id: int | None = None
    ):
        self.session_id = session_id
        self.user_id = user_id
        self.role = role
        self.token = token
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.expires_at = expires_at

    def to_dict(self):
        """Converts the session object to a dictionary representation."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "role": self.role,
            "token": self.token,
            # TODO All datetime instances need to have this check
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if isinstance(self.created_at, datetime) else self.created_at,
            "expires_at": self.expires_at.strftime("%Y-%m-%d %H:%M:%S")
        }