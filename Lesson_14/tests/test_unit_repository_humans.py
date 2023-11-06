import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Human, User
from src.schemas import HumanModel
from src.repository.humans import (
    get_humans,
    get_human,
    get_human_name,
    get_human_surname,
    get_human_email,
    get_list_birthdays,
    create_human,
    update_human,
    remove_human,
)


class TestHumans(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)


    async def test_get_humans(self):
        humans = [Human(), Human(), Human()]
        self.session.query().filter().limit().offset().all.return_value = humans
        result = await get_humans(limit=10, offset=0, user=self.user, db=self.session)
        self.assertEqual(result, humans)


    async def test_get_human_found(self):
        human = Human()
        self.session.query().filter().first.return_value = human
        result = await get_human(human_id=1, user=self.user, db=self.session)
        self.assertEqual(result, human)


    async def test_get_human_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_human(human_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


    async def test_get_human_name(self):
        humans = [Human(), Human(), Human()]
        self.session.query().filter().all.return_value = humans
        result = await get_human_name(human_name="Hulk", user=self.user, db=self.session)
        self.assertEqual(result, humans)


    async def test_get_human_surname(self):
        humans = [Human(), Human(), Human()]
        self.session.query().filter().all.return_value = humans
        result = await get_human_surname(human_surname="Pupkin", user=self.user, db=self.session)
        self.assertEqual(result, humans)


    async def test_get_human_email(self):
        humans = [Human(), Human(), Human()]
        self.session.query().filter().all.return_value = humans
        result = await get_human_email(human_email="hulk_pupkin@com.ua", user=self.user, db=self.session)
        self.assertEqual(result, humans)


    async def test_get_list_birthdays(self):
        humans = [Human(), Human(), Human()]
        self.session.query().filter().all.return_value = humans
        result = await get_list_birthdays(user=self.user, db=self.session)
        self.assertEqual(result, humans)


    async def test_create_human(self):
        body = HumanModel(name="Hulk", surname="Pupkin", email="hulk_pupkin@com.ua",
                        phone="0671234567", birthday="2023-11-01", description="test human")
        result = await create_human(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "id"))


    async def test_update_human_found(self):
        body = HumanModel(name="Hulk", surname="Pupkin", email="hulk_pupkin@com.ua",
                        phone="0671234567", birthday="2023-11-01", description="test human", done=True)
        human = Human()
        self.session.query().filter().first.return_value = human
        self.session.commit.return_value = None
        result = await update_human(human_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, human)


    async def test_update_human_not_found(self):
        body = HumanModel(name="Hulk", surname="Pupkin", email="hulk_pupkin@com.ua",
                        phone="0671234567", birthday="2023-11-01", description="test human", done=True)
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_human(human_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


    async def test_remove_human_found(self):
        human = Human()
        self.session.query().filter().first.return_value = human
        result = await remove_human(human_id=1, user=self.user, db=self.session)
        self.assertEqual(result, human)


    async def test_remove_human_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_human(human_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
