import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel, UserDb, TokenModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)


    async def test_get_user_by_email_found(self):
        user = User(email="test_user@com.ua")
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(User.email=="test_user@com.ua", db=self.session)
        self.assertEqual(result, user)


    async def test_get_user_by_email_not_found(self):
        user = User(email="test_user@com.ua")
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(User.email=="test_user@com.ua", db=self.session)
        self.assertIsNone(result)


    async def test_create_user(self):
        body= UserModel(username="Pavlo", email="test_user@com.ua", password="password")
        user = User(**body.dict())
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))


    async def test_update_token(self):
        user = User(email="test_user@com.ua", refresh_token="old_token")
        new_token = "new_token"
        self.session.commit.return_value = None
        await update_token(user, new_token, db=self.session)
        self.assertEqual(user.refresh_token, new_token)


    async def test_confirmed_email(self):
        user = User(email="test_user@com.ua", confirmed=False)
        self.session.query(User).filter(User.email == "test_user@com.ua").first.return_value = user
        self.session.commit.return_value = None
        await confirmed_email("test_user@com.ua", db=self.session)
        self.assertTrue(user.confirmed)


if __name__ == '__main__':
    unittest.main()
