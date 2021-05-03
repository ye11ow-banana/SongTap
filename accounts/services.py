from .models import AppUser
from typing import Optional, Union
from validate_email import validate_email
from random import randint
from recomendations.models import MusicUserToken


def check_email_valid(email: str, current_user_email: str='email') -> Optional[str]:
    """Проверяет валидность почты"""
    if email:
        if validate_email(email):
            users = AppUser.objects.filter(email=email)
            if len(users) > 0 and email != current_user_email:
                return 'Пользователь с такой почтой уже существует'
        else:
            return 'Введите валидную почту'


def generate_username() -> str:
    """Генерирует логин"""
    while True:
        username = str(randint(10, 10000000))

        try:
            AppUser.objects.get(username=username)
        except AppUser.DoesNotExist:
            break

    return username


def update_user_data_if_email_valid(request, user: object) -> Optional[dict]:
    """"Обновляет данные юзера, если email валидный"""
    email = request.data['email']
    result = check_email_valid(email, user.email)

    if result:
        return {'result': False, 'msg': result}

    if email:
        user.email = email

    if request.data['first_name']:
        user.first_name = request.data['first_name']

    if request.data['last_name']:
        user.last_name = request.data['last_name']

    if request.data['gender']:
        user.gender = request.data['gender']

    if request.data['age']:
        user.age = request.data['age']

    user.save()


def get_user_or_error(apple_id: str) -> Union[object, dict]:
    """Возвращает юзера или ошибку"""
    try:
        return AppUser.objects.get(apple_id=apple_id)
    except AppUser.DoesNotExist:
        return {'result': False, 'msg': 'Нет такого apple_id'}


def get_error_if_username_not_valid(username: str, user: object) -> Optional[dict]:
    """Возвращает ошибку, если логин не валидный"""
    users = AppUser.objects.filter(username=username)

    if username != user.username and len(users) > 0:
        return {'result': False, 'msg': 'Такой логин уже существует'}

    if username == '':
        return {'result': False, 'msg': 'Вы ничего не ввели'}


def get_error_or_update_username(username: str, user: object) -> Optional[dict]:
    """Если логин валидный, обновляет его"""
    result = get_error_if_username_not_valid(username, user)

    if result:
        return result
    else:
        user.username = username
        user.save()


def get_error_or_create_or_update_account(request) -> Union[object, dict]:
    """Создает, обновляет данные юзера или вернет ошибку"""
    music_user_token = request.data['music_user_token']
    apple_id = request.data['apple_id']

    user, _ = AppUser.objects.get_or_create(apple_id=apple_id)

    if _:
        user.username = generate_username()
    else:
        old_music_user_token = MusicUserToken.objects.get(user=user).music_user_token

    result = update_user_data_if_email_valid(request, user)

    if music_user_token:
        m_u_t, _ = MusicUserToken.objects.update_or_create(
            user=user, defaults={'music_user_token': music_user_token}
        )

    if result:
        if _:
            user.delete()
            m_u_t.delete()

        elif music_user_token:
            m_u_t.music_user_token = old_music_user_token
            m_u_t.save()

        return result

    return user
