import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


#AUTH0_DOMAIN = 'sersy.auth0.com'
#API_AUDIENCE = 'Asky'

algorithm = 'HS256'
secret = "Ft5TtPDEnbz5O7iFxOqfyYKfFrDGGpRf"



class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth = request.headers.get("Authorization",None)

    if not auth :
        raise AuthError({
            'code': 'not found authorization',
            'description': 'Authorization header not found'
        }, 401)


    auth_list = auth.split(" ")
    
    n = len(auth_list)
    
    if n == 2 :
        bearer = auth_list[0]
        if bearer.lower() != "bearer":
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header dosn`t have Bearer'
            }, 401)



        token  = auth_list[1]
        return token

    else:
        if n == 1:
            raise AuthError({
                'code': 'invalid header',
                'description': 'not found token'
            }, 401)
        elif n > 2 :
            raise AuthError({
                'code': 'invalid format',
                'description': 'Authorization header is not baearer token format'
            }, 401)



def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload["permissions"]:
        raise AuthError({
            "code" : "unauthorized",
            "description" : "Not Allowed Permession"
        } , 403 )

    return True

def verify_decode_jwt(token):
        try:
            global secret
            global algorithm

            payload = jwt.decode(token=token, key = secret, algorithms= algorithm)
            print(payload)
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)


            
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # get the token from "Bearer TOKEN"
            token = get_token_auth_header()
            # get the payload from the access token "HEADER.PAYLOAD.SIGNATURE"
            payload = verify_decode_jwt(token)
            # check the permission if only required
            if permission != '':
                check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator