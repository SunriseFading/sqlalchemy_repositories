import pytest
from sqlalchemy import select
from tests.models import Instance as InstanceModel
from tests.repositories import instance_repository
from tests.settings import test_instance


class TestBase:
    async def test_create(self, session):
        created_instance = await instance_repository.create(
            instance=InstanceModel(name=test_instance.name), session=session
        )
        assert created_instance.name == test_instance.name

    async def test_bulk_create(self, session):
        instances_model = []
        for number in range(10):
            name = f"№{number} {test_instance.name}"
            instances_model.append(InstanceModel(name=name))
        created_users = await instance_repository.bulk_create(instances=instances_model, session=session)
        for instance_model, created_instance in zip(instances_model, created_users):
            assert instance_model.name == created_instance.name

    def test_set_filters(self):
        query = select(InstanceModel)
        filters = {
            "id__gt": "0",
            "id__gte": "1",
            "id__lt": "2",
            "id__lte": "1",
            "id": "1",
            "name": test_instance.name,
        }
        query = instance_repository.set_filters(query=query, kwargs=filters)
        expected_filters = [
            f"{InstanceModel.__tablename__}.id > :id_1",
            f" {InstanceModel.__tablename__}.id >= :id_2",
            f" {InstanceModel.__tablename__}.id < :id_3",
            f" {InstanceModel.__tablename__}.id <= :id_4",
            f" {InstanceModel.__tablename__}.id = :id_5",
            f" {InstanceModel.__tablename__}.name = :name_1",
        ]
        for expected_filter in expected_filters:
            assert expected_filter in str(query)

    @pytest.mark.parametrize(
        "order_by,params",
        [
            ("-name", "DESC"),
            ("name", ""),
        ],
    )
    def test_set_order_by(self, order_by, params):
        query = select(InstanceModel)
        query = instance_repository.set_order_by(query=query, order_by=order_by)
        expected_query = f"ORDER BY {InstanceModel.__tablename__}.name {params}"
        assert expected_query.rstrip() in str(query)

    async def test_get(self, session):
        got_instance = await instance_repository.get(name=test_instance.name, session=session)
        assert got_instance.name == test_instance.name

    async def test_get_or_create(self, session):
        instance_model = InstanceModel(name=test_instance.name)
        created_instance = await instance_repository.get_or_create(instance=instance_model, session=session)
        assert created_instance.id is not None
        got_instance = await instance_repository.get_or_create(instance=instance_model, session=session)
        assert created_instance.id == got_instance.id

    async def test_all(self, session):
        all_instances = await instance_repository.all(session=session)
        assert len(all_instances) == 11

    async def test_filter(self, session):
        filters = {
            "id__gt": "0",
            "id__gte": "1",
            "id__lt": "2",
            "id__lte": "1",
            "id": "1",
            "name": test_instance.name,
        }
        filtered_instances = await instance_repository.filter(session=session, **filters)
        assert len(filtered_instances) == 1
        assert filtered_instances[0].name == test_instance.name

    async def test_update(self, session):
        instance_model = InstanceModel(id=1, name=test_instance.updated_name)
        updated_instance = await instance_repository.update(instance=instance_model, session=session)
        assert test_instance.updated_name == updated_instance.name

    async def test_bulk_update(self, session):
        all_instances = await instance_repository.all(session=session)
        instances_model = []
        for number in range(len(all_instances)):
            id = all_instances[number].id
            name = f"№{number} {test_instance.updated_name}"
            instances_model.append(InstanceModel(id=id, name=name))
        updated_instances = await instance_repository.bulk_update(instances=instances_model, session=session)
        for instance_model, updated_instance in zip(instances_model, updated_instances):
            assert instance_model.name == updated_instance.name

    async def test_delete(self, session):
        got_instance = await instance_repository.get(id=1, session=session)
        await instance_repository.delete(instance=got_instance, session=session)
        assert not bool(await instance_repository.get(id=1, session=session))

    async def test_bulk_delete(self, session):
        all_instances = await instance_repository.all(session=session)
        await instance_repository.bulk_delete(instances=all_instances, session=session)
        assert not bool(await instance_repository.all(session=session))
