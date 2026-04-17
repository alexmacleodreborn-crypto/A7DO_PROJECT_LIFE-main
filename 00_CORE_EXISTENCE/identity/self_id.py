from datetime import datetime, timezone
import uuid

class SelfIdentity:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc).isoformat()

    def as_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
        }
