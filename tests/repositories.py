from base import BaseRepository
from tests.models import User as UserModel


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=UserModel)


user_repository = UserRepository()
