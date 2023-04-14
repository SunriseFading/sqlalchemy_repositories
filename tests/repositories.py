from src.base import BaseRepository
from tests.models import Instance as InstanceModel


class InstanceRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=InstanceModel)


instance_repository = InstanceRepository()
