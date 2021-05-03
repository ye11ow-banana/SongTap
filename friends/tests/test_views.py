from django.urls import reverse
from rest_framework.test import APITestCase
from friends.models import Friend
from friends.tests.utils import _create_default_2_users


class CreateFriendTestCase(APITestCase):
    """Тестирование вьюшки create_friend"""
    url = reverse('create_friend')

    def test_with_username(self):
        """Тестирует создание друга по username"""
        user_1, user_2 = _create_default_2_users()

        data = {
            'user_apple_id': '1',
            'friend_data': '2'
        }

        self.client.post(path=self.url, data=data)

        try:
            Friend.objects.get(user=user_1, friend=user_2)
            result = True
        except Friend.DoesNotExist:
            result = False

        self.assertEqual(result, True)

    def test_with_email(self):
        """Тестирует создание друга по email"""
        user_1, user_2 = _create_default_2_users()

        data = {
            'user_apple_id': '1',
            'friend_data': '2@2'
        }

        self.client.post(path=self.url, data=data)

        try:
            Friend.objects.get(user=user_1, friend=user_2)
            result = True
        except Friend.DoesNotExist:
            result = False

        self.assertEqual(result, True)

    def test_with_not_existing_user(self):
        """Тестирует получение ошибки из-за несуществующего юзера"""
        data = {
            'user_apple_id': '1',
            'friend_data': '2@2'
        }

        response = self.client.post(path=self.url, data=data)

        try:
            Friend.objects.get(user__apple_id='1', friend__email='2@2')
            result = False
        except Friend.DoesNotExist:
            result = True

        self.assertEqual(response.json()['result'], False)
        self.assertEqual(result, True)

    def test_with_not_existing_friend(self):
        """Тестирует получение ошибки из-за несуществующего юзера-друга"""
        user_1, user_2 = _create_default_2_users()

        data = {
            'user_apple_id': '1',
            'friend_data': '3@3'
        }

        response = self.client.post(path=self.url, data=data)

        try:
            Friend.objects.get(user=user_1, friend__email='3@3')
            result = False
        except Friend.DoesNotExist:
            result = True

        self.assertEqual(response.json()['result'], False)
        self.assertEqual(result, True)

    def test_get_key_error(self):
        """Тестирует получение ошибки из-за невалидного json"""
        data = {}

        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.json()['result'], False)

    def test_get_type_error(self):
        """Тестирует получение ошибки из-за невалидного json"""
        data = {
            'user_apple_id': 1,
            'friend_data': 2
        }

        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.json()['result'], False)


class ViewFriendsLikesTestCase(APITestCase):
    """Тестирование вьюшки view_friends_likes"""

    def test_with_not_existing_user(self):
        """Тестирует получение ошибки из-за несуществующего юзера"""
        url = reverse('view_friends_likes', args=('1',))

        response = self.client.get(path=url)

        self.assertEqual(response.json()['result'], False)

    def test_get_200(self):
        """Тестирует получение статуса 200"""
        url = reverse('view_friends_likes', args=('1',))

        _create_default_2_users()

        response = self.client.get(path=url)

        self.assertEqual(response.json(), [])
        self.assertEqual(response.status_code, 200)


class GetFriendsTestCase(APITestCase):
    """Тестирование вьюшки get_friends"""

    def test_with_not_existing_user(self):
        """Тестирует получение ошибки из-за несуществующего юзера"""
        url = reverse('get_friends', args=('1',))

        response = self.client.get(path=url)

        self.assertEqual(response.json()['result'], False)

    def test_get_200(self):
        """Тестирует получение статуса 200"""
        url = reverse('get_friends', args=('1',))

        _create_default_2_users()

        response = self.client.get(path=url)

        self.assertEqual(response.json(), [])
        self.assertEqual(response.status_code, 200)


class GetSimilarUsersTestCase(APITestCase):
    """Тестирование вьюшки get_similar_users"""

    def test_with_not_existing_user(self):
        """Тестирует получение ошибки из-за несуществующего юзера"""
        url = reverse('get_similar_users', args=('1',))

        response = self.client.get(path=url)

        self.assertEqual(response.json()['result'], False)

    def test_get_200(self):
        """Тестирует получение статуса 200"""
        url = reverse('get_friends', args=('1',))

        _create_default_2_users()

        response = self.client.get(path=url)

        self.assertEqual(response.json(), [])
        self.assertEqual(response.status_code, 200)


class GetFriendsSongsTestCase(APITestCase):
    """Тестирование вьюшки get_friends_songs"""
    def test_with_not_existing_user(self):
        """Тестирует получение ошибки из-за несуществующего юзера"""
        url = reverse('get_friends_songs', args=('1',))

        response = self.client.get(path=url)

        self.assertEqual(response.json()['result'], False)

    def test_get_200(self):
        """Тестирует получение статуса 200"""
        url = reverse('get_friends_songs', args=('1',))

        _create_default_2_users()

        response = self.client.get(path=url)

        self.assertEqual(response.json(), [])
        self.assertEqual(response.status_code, 200)


class DeleteFriendTestCase(APITestCase):
    """Тестирование вьюшки delete_friend"""
    url = reverse('delete_friend')

    def test_with_username(self):
        """Тестирует удаление друга по username"""
        user_1, user_2 = _create_default_2_users()
        Friend.objects.create(user=user_1, friend=user_2)

        data = {
            'user_apple_id': '1',
            'friend_data': '2'
        }

        self.client.post(path=self.url, data=data)

        try:
            Friend.objects.get(user=user_1, friend=user_2)
            result = False
        except Friend.DoesNotExist:
            result = True

        self.assertEqual(result, True)

    def test_with_email(self):
        """Тестирует удаление друга по email"""
        user_1, user_2 = _create_default_2_users()
        Friend.objects.create(user=user_1, friend=user_2)

        data = {
            'user_apple_id': '1',
            'friend_data': '2@2'
        }

        self.client.post(path=self.url, data=data)

        try:
            Friend.objects.get(user=user_1, friend=user_2)
            result = False
        except Friend.DoesNotExist:
            result = True

        self.assertEqual(result, True)

    def test_with_not_existing_user(self):
        """Тестирует получение ошибки из-за несуществующего юзера"""
        data = {
            'user_apple_id': '1',
            'friend_data': '2@2'
        }

        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.json()['result'], False)

    def test_with_not_existing_friend(self):
        """Тестирует получение ошибки из-за несуществующего юзера-друга"""
        _create_default_2_users()

        data = {
            'user_apple_id': '1',
            'friend_data': '3@3'
        }

        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.json()['result'], False)

    def test_get_key_error(self):
        """Тестирует получение ошибки из-за невалидного json"""
        data = {}

        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.json()['result'], False)

    def test_get_type_error(self):
        """Тестирует получение ошибки из-за невалидного json"""
        data = {
            'user_apple_id': 1,
            'friend_data': 2
        }

        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.json()['result'], False)
