from datetime import datetime, timedelta
from django.conf import settings
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
import jwt

"""
 Generates a short-lived JWT access token for a given user.

    The token contains the user's ID, an expiration time (1 day from creation), 
    and the issued time. It is encoded using the 'HS256' algorithm and the application's 
    secret key.

    Args:
        user (UserAccount): The user for whom the token is generated.

    Returns:
        str: The encoded JWT token.
"""


def generate_access_token(user):
    payload = {
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1, minutes=0),
        'iat': datetime.utcnow()
    }

    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token


# ----------------------------------------------------

"""
 Decodes and validates the JWT token from the request's cookies.

    Checks if the token exists and is valid. If the token is missing, expired, or invalid, 
    it returns an error response. Otherwise, it returns the decoded user data.

    Args:
        request (HttpRequest): The request containing the JWT token in cookies.

    Returns:
        dict: Decoded user data, or a Response with an error message if validation fails.

"""


def token_decode(request: HttpRequest) -> dict:
    jwt_token = request.COOKIES.get('access_token', None)

    if not jwt_token:
        return Response({"error": "Error, you cannot do this without logging in. Login first!"},
                        status=status.HTTP_401_UNAUTHORIZED)

    try:
        user_id = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError as e:
        return Response({"error": "Token has expired. Please log in again."}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError as e:
        return Response({"error": "Invalid token. Please log in again."}, status=status.HTTP_401_UNAUTHORIZED)

    return user_id
