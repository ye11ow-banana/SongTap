from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import AppUser
from recomendations.models import MusicUserToken


class GetOrCreateOrUpdateAccountTestCase(APITestCase):
    """Тестирование вьюшки get_or_create_or_update_account"""
    url = reverse('get_or_create_or_update_account')

    def test_create_without_data(self):
        """Тестирует создание аккаунта без данных"""
        data = {
            'music_user_token': '1',
            'apple_id': '1',
            'email': '',
            'first_name': '',
            'last_name': '',
            'gender': '',
            'age': ''
        }

        self.client.post(path=self.url, data=data)

        try:
            user = AppUser.objects.get(apple_id='1')
            MusicUserToken.objects.get(music_user_token='1')
            if user.username:
                result = True
            else:
                result = False
        except (AppUser.DoesNotExist, MusicUserToken.DoesNotExist):
            result = False

        self.assertEqual(result, True)

    def test_create_with_data(self):
        """Тестирует создание аккаунта с данными"""
        data = {
            'music_user_token': '1',
            'apple_id': '1',
            'email': 'dima.petrov@gmail.com',
            'first_name': 'dima',
            'last_name': 'petrov',
            'gender': 'M',
            'age': '35'
        }
        self.client.post(path=self.url, data=data)

        try:
            user = AppUser.objects.get(apple_id='1')
            MusicUserToken.objects.get(music_user_token='1')
            if user.email == 'dima.petrov@gmail.com' and \
                    user.first_name == 'dima' and \
                    user.last_name == 'petrov' and \
                    user.gender == 'M' and \
                    user.age == '35' and \
                    user.username:
                result = True
            else:
                result = False
        except (AppUser.DoesNotExist, MusicUserToken.DoesNotExist):
            result = False

        self.assertEqual(result, True)

    def test_create_with_existing_email(self):
        """Тестирует создание аккаунта с существующей почтой"""
        AppUser.objects.create(
            apple_id='2',
            email='dima.petrov@gmail.com',
            username='123'
        )

        data = {
            'music_user_token': '1',
            'apple_id': '1',
            'email': 'dima.petrov@gmail.com',
            'first_name': 'dima',
            'last_name': 'petrov',
            'gender': 'M',
            'age': '35'
        }

        response = self.client.post(path=self.url, data=data)

        try:
            AppUser.objects.get(apple_id='1')
            MusicUserToken.objects.get(music_user_token='1')
            result = False
        except (AppUser.DoesNotExist, MusicUserToken.DoesNotExist):
            result = True

        self.assertEqual(response.json()['result'], False)
        self.assertEqual(result, True)

    def test_create_with_invalid_email(self):
        """Тестирует создание аккаунта с невалидной почтой"""
        data = {
            'music_user_token': '1',
            'apple_id': '1',
            'email': 'gg',
            'first_name': 'dima',
            'last_name': 'petrov',
            'gender': 'M',
            'age': '35'
        }

        response = self.client.post(path=self.url, data=data)

        try:
            AppUser.objects.get(apple_id='1')
            MusicUserToken.objects.get(music_user_token='1')
            result = False
        except (AppUser.DoesNotExist, MusicUserToken.DoesNotExist):
            result = True

        self.assertEqual(response.json()['result'], False)
        self.assertEqual(result, True)

    def test_create_with_invalid_json(self):
        """Тестирует создание аккаунта с невалидным json"""
        data = {
            'music_user_token': 1,
            'apple_id': 1,
            'email': 123,
            'first_name': 1.23,
            'last_name': 123,
            'gender': 123,
            'age': 123
        }

        response = self.client.post(path=self.url, data=data)

        try:
            AppUser.objects.get(apple_id='1')
            result = False
        except AppUser.DoesNotExist:
            result = True

        self.assertEqual(response.json()['result'], False)
        self.assertEqual(result, True)

    def test_update_with_invalid_json(self):
        """Тестирует обновление аккаунта с невалидным json"""
        user = AppUser.objects.create(apple_id='1')
        MusicUserToken.objects.create(user=user, music_user_token='1')

        data = {'apple_id': '1', 'music_user_token': '2'}

        response = self.client.post(path=self.url, data=data)

        try:
            AppUser.objects.get(apple_id='1')
            result_for_user = True
        except AppUser.DoesNotExist:
            result_for_user = False

        try:
            MusicUserToken.objects.get(music_user_token='2')
            result_for_m_u_t = False
        except MusicUserToken.DoesNotExist:
            result_for_m_u_t = True

        self.assertEqual(response.json()['result'], False)
        self.assertEqual(result_for_user, True)
        self.assertEqual(result_for_m_u_t, True)

    def test_update_with_data(self):
        """Тестирует обновления данных"""
        user = AppUser.objects.create(
            apple_id='1',
            email='dima.petrov@gmail.com',
            first_name='dima',
            last_name='petrov',
            gender='W',
            age='36',
            username='123'
        )
        MusicUserToken.objects.create(user=user, music_user_token='1')

        data = {
            'music_user_token': '2',
            'apple_id': '1',
            'email': 'michael_good@gmail.com',
            'first_name': 'michael',
            'last_name': 'good',
            'gender': 'M',
            'age': '19'
        }

        self.client.post(path=self.url, data=data)

        try:
            user = AppUser.objects.get(apple_id='1')
            MusicUserToken.objects.get(music_user_token='2')

            if user.email == 'michael_good@gmail.com' and \
                    user.first_name == 'michael' and \
                    user.last_name == 'good' and \
                    user.gender == 'M' and \
                    user.age == '19':
                result = True
            else:
                result = False
        except (AppUser.DoesNotExist, MusicUserToken.DoesNotExist):
            result = False

        self.assertEqual(result, True)

    def test_update_with_existing_email(self):
        """Тестирует обновления данных с существующей почтой"""
        AppUser.objects.create(
            apple_id='2',
            email='dima.petrov@gmail.com',
            username='123'
        )

        user = AppUser.objects.create(
            apple_id='1',
            email='michael_good@gmail.com',
            first_name='michael',
            last_name='good',
            gender='M',
            age='19',
            username='1234'
        )
        MusicUserToken.objects.create(user=user, music_user_token='1')

        data = {
            'music_user_token': '',
            'apple_id': '1',
            'email': 'dima.petrov@gmail.com',
            'first_name': 'dima',
            'last_name': 'petrov',
            'gender': 'W',
            'age': '35'
        }

        response = self.client.post(path=self.url, data=data)

        try:
            user = AppUser.objects.get(apple_id='1')
            MusicUserToken.objects.get(music_user_token='1')

            if user.email == 'michael_good@gmail.com' and \
                    user.first_name == 'michael' and \
                    user.last_name == 'good' and \
                    user.gender == 'M' and \
                    user.age == '19':
                result = True
            else:
                result = False
        except (AppUser.DoesNotExist, MusicUserToken.DoesNotExist):
            result = False

        self.assertEqual(response.json()['result'], False)
        self.assertEqual(result, True)

    def test_update_with_invalid_email(self):
        """Тестирует обновления данных с невалидной почтой"""
        user = AppUser.objects.create(
            apple_id='1',
            email='dima.petrov@gmail.com',
            first_name='dima',
            last_name='petrov',
            gender='W',
            age='36',
            username='123'
        )
        MusicUserToken.objects.create(user=user, music_user_token='1')

        data = {
            'music_user_token': '2',
            'apple_id': '1',
            'email': 'michael_goodgmail.com',
            'first_name': 'michael',
            'last_name': 'good',
            'gender': 'M',
            'age': '19'
        }

        response = self.client.post(path=self.url, data=data)

        try:
            user = AppUser.objects.get(apple_id='1')
            MusicUserToken.objects.get(music_user_token='1')

            if user.email == 'dima.petrov@gmail.com' and \
                    user.first_name == 'dima' and \
                    user.last_name == 'petrov' and \
                    user.gender == 'W' and \
                    user.age == '36':
                result = True
            else:
                result = False
        except (AppUser.DoesNotExist, MusicUserToken.DoesNotExist):
            result = False

        self.assertEqual(response.json()['result'], False)
        self.assertEqual(result, True)

    def test_get_account(self):
        """Тестирует получения данных аккаунта"""
        user = AppUser.objects.create(
            apple_id='1',
            email='michael_good@gmail.com',
            first_name='michael',
            last_name='good',
            gender='M',
            age='19',
            username='123'
        )
        MusicUserToken.objects.create(user=user, music_user_token='1')

        data = {
            'music_user_token': '',
            'apple_id': '1',
            'email': '',
            'first_name': '',
            'last_name': '',
            'gender': '',
            'age': ''
        }

        self.client.post(path=self.url, data=data)

        try:
            user = AppUser.objects.get(apple_id='1')
            MusicUserToken.objects.get(music_user_token='1')

            if user.email == 'michael_good@gmail.com' and \
                    user.first_name == 'michael' and \
                    user.last_name == 'good' and \
                    user.gender == 'M' and \
                    user.age == '19':
                result = True
            else:
                result = False
        except (AppUser.DoesNotExist, MusicUserToken.DoesNotExist):
            result = False

        self.assertEqual(result, True)


class UpdateLoginTestCase(APITestCase):
    """Тестирование вьюшки update_login"""
    url = reverse('update_login')

    def test_get_error_by_not_existing_apple_id(self):
        """Тестирует получение ошибки по несуществующему apple_id"""
        AppUser.objects.create(apple_id='1', username='123')

        data = {
            'apple_id': '2',
            'username': 'boss'
        }

        response = self.client.post(path=self.url, data=data)

        try:
            AppUser.objects.get(username='boss')
            result = False
        except AppUser.DoesNotExist:
            result = True

        self.assertEqual(response.json()['result'], False)
        self.assertEqual(result, True)

    def test_get_error_by_empty_username(self):
        """Тестирует получение ошибки по пустому username"""
        AppUser.objects.create(apple_id='2', username='123')

        data = {
            'apple_id': '1',
            'username': ''
        }

        response = self.client.post(path=self.url, data=data)

        try:
            AppUser.objects.get(username='')
            result = False
        except AppUser.DoesNotExist:
            result = True

        self.assertEqual(response.json()['result'], False)
        self.assertEqual(result, True)

    def test_get_error_by_existing_username(self):
        """Тестирует получение ошибки по существующему username"""
        AppUser.objects.create(apple_id='2', username='boss')

        user = AppUser.objects.create(apple_id='1')
        user.username = 'crazy'
        user.save()

        data = {
            'apple_id': '1',
            'username': 'boss'
        }

        response = self.client.post(path=self.url, data=data)

        try:
            AppUser.objects.get(username='crazy')
            result = True
        except AppUser.DoesNotExist:
            result = False

        self.assertEqual(response.json()['result'], False)
        self.assertEqual(result, True)

    def test_update_username(self):
        """Тестирует обновлеие username"""
        AppUser.objects.create(apple_id='1', username='crazy')

        data = {
            'apple_id': '1',
            'username': 'boss'
        }

        self.client.post(path=self.url, data=data)

        try:
            AppUser.objects.get(username='boss')
            result = True
        except AppUser.DoesNotExist:
            result = False

        self.assertEqual(result, True)

    def test_get_key_error_by_invalid_json(self):
        """Тестирует получение ошибки KeyError с невалидным json"""
        AppUser.objects.create(apple_id='1', username='123')

        data = {
            'apple_id': '1'
        }

        response = self.client.post(path=self.url, data=data)

        try:
            user = AppUser.objects.get(apple_id='1')
            if user.username is None:
                result = False
            else:
                result = True
        except AppUser.DoesNotExist:
            result = False

        self.assertEqual(response.json()['result'], False)
        self.assertEqual(result, True)
