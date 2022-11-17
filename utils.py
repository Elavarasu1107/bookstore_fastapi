import logging
from enum import Enum
from os import environ

import jwt
from dotenv import load_dotenv

load_dotenv()
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
            payload.update(exp=environ.get("TOKEN_EXPIRE_MINUTES"))
            if exp:
                payload.update({'exp': exp})
            return jwt.encode(payload, environ.get("JWT_SECRET_KEY"), algorithm=environ.get("ALGORITHM"))
        except Exception as ex:
            logger.exception(ex)

    def decode(self, token):
        """
        This method return decoded data from the token
        """
        try:
            return jwt.decode(token, environ.get("JWT_SECRET_KEY"), algorithms=[environ.get("ALGORITHM")])
        except jwt.PyJWTError as ex:
            raise Exception(ex)
        except Exception as ex:
            logger.exception(ex)
