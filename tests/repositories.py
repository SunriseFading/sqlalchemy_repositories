from src.base import BaseRepository
from tests.models import Instance as InstanceModel


class InstanceRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model=model)


instance_repository = InstanceRepository(model=InstanceModel)
