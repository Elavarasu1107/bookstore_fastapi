import logging
from datetime import datetime, timedelta
from enum import Enum

import jwt
from fastapi import HTTPException, Request, Response, status

from models import User
from settings import settings
from dagster import asset

from validators import BookValidator

logging.basicConfig(filename='book_store.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


class TokenRole(Enum):
    default = 'null'
    auth = 'Auth'
    verify_user = 'VerifyUser'
    forgot_password = 'ForgotPassword'


class JWT:

    def encode(self, payload, exp=None):
        """
        This method return encoded token for user data
        """
        try:
            if "role" not in payload.keys():
                payload.update(role=TokenRole.default.value)
            if not isinstance(payload, dict):
                raise Exception("Payload should be in dict")
            payload.update(exp=datetime.utcnow() + timedelta(minutes=60))
            if exp:
                payload.update({'exp': exp})
            return jwt.encode(payload, settings.jwt_key, algorithm=settings.algorithm)
        except Exception as ex:
            logger.exception(ex)

    def decode(self, token):
        """
        This method return decoded data from the token
        """
        try:
            payload = jwt.decode(token, settings.jwt_key, algorithms=[settings.algorithm])
            return payload
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(detail='Token Expired', status_code=status.HTTP_406_NOT_ACCEPTABLE)
        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(detail='Invalid Token', status_code=status.HTTP_403_FORBIDDEN)
        except Exception as ex:
            logger.exception(ex)


@asset
def request():
    return Request


@asset
def response():
    return Response


@asset
def payload():
    return BookValidator


def get_user(request):
    token = request.headers.get("token")
    if not token:
        raise HTTPException(detail='Auth token required', status_code=status.HTTP_404_NOT_FOUND)
    decode = JWT().decode(token)
    if decode.get('role') != TokenRole.auth.value:
        raise HTTPException(detail='Invalid Token Role', status_code=status.HTTP_406_NOT_ACCEPTABLE)
    user = User.objects.get(id=decode.get('user_id'))
    if not user:
        raise HTTPException(detail='User not found', status_code=404)
    return user


@asset
def verify_user(request):
    return get_user(request)


@asset
def verify_superuser(request):
    user = get_user(request)
    if not user.is_superuser:
        raise HTTPException(detail='User not authorized', status_code=404)
    return user
