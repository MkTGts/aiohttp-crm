from app.crm.models import User
from typing import Optional
from app.web.app import Application


class CrmAccessor:
    def __init__(self):
        self.app: Optional[Application] = None

    def add_user(self, user: User):
        self.app.database['users'].append(users)
