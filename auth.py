import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-o1fi8lp1.us.auth0.com'   #updated this to reflect my auth0 domain
ALGORITHMS = ['RS256']
API_AUDIENCE = 'castingagency3'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if auth_header == None:
        
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header was expected.'
        }, 401)

    parts = auth_header.split()
    if parts[0].lower() != 'bearer':
        
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    elif len(parts) == 1:
        
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token was not found.'
        }, 401)

    elif len(parts) > 2:
        
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def verify_decode_jwt(token):   #the input is a JWT token
    
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')  #collects the public key from Auth0
    
    jwks = json.loads(jsonurl.read())                                   #gives us the key/s in a readable dict format, including 'kid'
    
    unverified_header = jwt.get_unverified_header(token)                #Uses jwt's get_unverified_header to get the header from the token
    
    if 'kid' not in unverified_header:  #double-checks that the JWT header actually contains a key ID for us to verify
        
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)  
    
    rsa_key = {} #empty dictionary to be populated later if the unverified_header key ID matches Auth0's public key ID
    for key in jwks['keys']:   
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    if rsa_key:   #if rsa_key is populated, try to validate/decode the token with the key
        try:
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
    else:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 400)


def check_permissions(permission, payload):
    
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'unavailable_permission',
            'description': 'No permissions were found in JWT.'
        }, 400)
    elif permission not in payload['permissions']:  
        raise AuthError({
            'code': 'invalid_permission',
            'description': 'Permission was invalid.'
        }, 403)
    
    return True


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()

            try:
                payload = verify_decode_jwt(token)
            except Exception as e:
                print(e)
                
                abort(401)

            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator