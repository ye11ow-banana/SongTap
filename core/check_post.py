from django.db import DataError
from rest_framework import status
from rest_framework.response import Response

from accounts.models import AppUser
from recomendations.models import MusicUserToken


def check_json(fn):
    """Декоратор для вьюшек. Обрабатывает исключения при неправильном json"""

    def inner(request, *args, **kwargs):
        try:
            return fn(request, *args, *kwargs)
        except KeyError:
            return Response({'result': False, 'msg': 'Не валидный json'}, status=status.HTTP_200_OK)
        except TypeError:
            return Response({'result': False, 'msg': 'Не тот тип данных в json'}, status=status.HTTP_200_OK)
        except AppUser.DoesNotExist:
            return Response({'result': False, 'msg': 'Нет пользователя с таким apple_id'},
                            status=status.HTTP_200_OK)
        except MusicUserToken.DoesNotExist:
            return Response({'result': False, 'msg': 'У пользователя нет music user token'},
                            status=status.HTTP_200_OK)
        except IndexError:
            return Response({'result': False, 'msg': 'Вы ввели данные несуществующего пользователя'},
                            status=status.HTTP_200_OK)
        except DataError:
            return Response({'result': False, 'msg': 'Вы ввели слишком длинные данные'},
                            status=status.HTTP_200_OK)

    return inner
