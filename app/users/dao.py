from ..dao.base import BaseDAO
from .models import Users


class UsersDAO(BaseDAO):
    model = Users
