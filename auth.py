import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS =  [ os.environ.get('ALGORITHMS') ]
API_AUDIENCE = os.environ.get('API_AUDIENCE')

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
            print("not barear")
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
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    
    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

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
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def login(payload):

        from Models import UserAuthID_ID

        Auth_id = payload['sub']
        authID_to_ID = UserAuthID_ID.query.filter(UserAuthID_ID.auth_id == Auth_id).all()

        if not len(authID_to_ID):
            new_user = UserAuthID_ID(auth_id = Auth_id)
            new_user.insert()



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

            login(payload)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator