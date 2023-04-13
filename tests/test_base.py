from sqlalchemy import select
from tests.models import User as UserModel
from tests.repositories import user_repository
from tests.settings import test_user


class TestBase:
    async def test_create(self, session):
        created_user = await user_repository.create(
            session=session, instance=UserModel(name=test_user.name)
        )
        assert created_user.name == test_user.name

    async def test_bulk_create(self, session):
        users = []
        for number in range(10):
            name = f"№{number} {test_user.name}"
            users.append(UserModel(name=name))
        created_users = await user_repository.bulk_create(
            session=session, instances=users
        )
        for user, created_user in zip(users, created_users):
            assert user.name == created_user.name

    def test_set_filters(self):
        query = select(UserModel)
        kwargs = {
            "id__gt": "0",
            "id__gte": "1",
            "id__lt": "2",
            "id__lte": "1",
            "id": "1",
            "name": test_user.name,
        }
        query = user_repository.set_filters(query=query, kwargs=kwargs)
        expected_filters = [
            f"{UserModel.__tablename__}.id > :id_1",
            f" {UserModel.__tablename__}.id >= :id_2",
            f" {UserModel.__tablename__}.id < :id_3",
            f" {UserModel.__tablename__}.id <= :id_4",
            f" {UserModel.__tablename__}.id = :id_5",
            f" {UserModel.__tablename__}.name = :name_1",
        ]
        for expected_filter in expected_filters:
            assert expected_filter in str(query)

    def test_set_order_by(self):
        query = select(UserModel)
        order_by = "-name"
        query = user_repository.set_order_by(query=query, order_by=order_by)
        expected_query = f"ORDER BY {UserModel.__tablename__}.name DESC"
        assert expected_query in str(query)
        query = select(UserModel)
        order_by = "name"

    async def test_get(self, session):
        got_user = await user_repository.get(name=test_user.name, session=session)
        assert got_user.id == 1
