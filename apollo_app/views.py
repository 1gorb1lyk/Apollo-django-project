import requests
from .models import UserAccount
from .utils import validate_api_key
from ApolloDjangoTestProject.tokens import generate_access_token, token_decode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status


"""
------------------------------------------------------
 The UserLogin class implements the login functionality for users registered through the Django admin panel. 
 It allows users to enter their email address for authorization. If the user is registered in the database, the system 
 generates an access token (access token), in which the user identifier (ID) is encrypted, and stores it in the server 
 cookie. The user can then use the token to make requests to other API classes in the system.

 If the user is not registered, or does not enter the correct e-mail address, he will not be able to enter the system 
 and perform requests.
------------------------------------------------------
 Example of data for POST request:

{
"email": "your Apollo.io email"
}

"""


class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        print(email)
        if not email:
            raise AuthenticationFailed('Error, login requires an email address. Please enter your email address')

        try:
            user = UserAccount.objects.get(email=email)
            print(user)
        except UserAccount.DoesNotExist:
            return Response("You are not register in system! Please contact with Tech Support!",
                            status=status.HTTP_404_NOT_FOUND)

        try:
            user_access_token = generate_access_token(user)
            response = Response()
            response.set_cookie(key='access_token', value=user_access_token, httponly=True)
            response.data = {'message': 'You have successfully logged in'}
            return response
        except Exception as e:
            return Response(f"Something went wrong -> {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ----------------------------------------------------

"""
------------------------------------------------------
 ContactAPI class handles creating and retrieving contacts via Apollo.io API.

    Before making any API requests, it checks if the user is logged in. If not, 
    the request is denied. The user's API key is used to authenticate the requests 
    to Apollo.io.

    Methods:
    - post: Create a new contact in Apollo.io after user authentication.
    - get: Retrieve contact stages from Apollo.io after user authentication.
------------------------------------------------------
 Example of data for POST request:
{
    "first_name": "Michael",
    "last_name": "Brown",
    "title": "Software Engineer",
    "organization_name": "OpenAI",
}
"""


class ContactAPI(APIView):
    def post(self, request):
        user_id = token_decode(request=request)

        data = request.data

        if isinstance(user_id, Response):
            return user_id

        try:
            user = UserAccount.objects.get(id=user_id['id'])
        except UserAccount.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not validate_api_key(user_id['id']):
            return Response("API key has been expired")

        url = "https://api.apollo.io/v1/contacts"

        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'X-Api-Key': user.api_key
        }

        try:
            response = requests.request("POST", url, headers=headers, json=data)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to connect to Apollo API: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        if response.status_code == 200:
            return Response(f"New Contact has been created successfully!\n{response.text}",
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to create contact'}, status=response.status_code)

    def get(self, request):

        user_id = token_decode(request=request)

        if isinstance(user_id, Response):
            return user_id

        try:
            user = UserAccount.objects.get(id=user_id['id'])
        except UserAccount.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not validate_api_key(user_id['id']):
            return Response("API key has been expired")

        url = "https://api.apollo.io/v1/contact_stages"

        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'X-Api-Key': user.api_key
        }

        try:
            response = requests.request("GET", url, headers=headers)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to connect to Apollo API: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)

        return Response({'error': 'Failed to get contact'}, status=response.status_code)


#  ----------------------------------------------------
"""
GetListEmailAccounts class retrieves a list of email accounts from Apollo.io API.

    Before making the request, it checks if the user is logged in. If not, the request is denied.
    The user's API key is used to authenticate the request to Apollo.io.

    Method:
    - get: Retrieves the list of email accounts after user authentication.
"""


class GetListEmailAccounts(APIView):
    def get(self, request):
        user_id = token_decode(request=request)

        if isinstance(user_id, Response):
            return user_id

        try:
            user = UserAccount.objects.get(id=user_id['id'])
        except UserAccount.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not validate_api_key(user_id['id']):
            return Response("API key has been expired")

        url = "https://api.apollo.io/v1/email_accounts"

        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'X-Api-Key': user.api_key
        }

        try:
            response = requests.request("GET", url, headers=headers)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to connect to Apollo API: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)

        return Response({'error': 'Failed to get emails'}, status=response.status_code)


# ----------------------------------------------------

"""
----------------------------------------------------
AccountAPI class handles the creation of a new account via Apollo.io API.

    Before making the API request, it verifies if the user is logged in and has a valid API key.
    The user's API key is used to authenticate the request.

    Method:
    - post: Creates a new account (company) on Apollo.io after user authentication.
----------------------------------------------------
  Example of data for POST request:
{
    "name": "Google",
    "domain": "google.com",
    "phone_number": "1-866-246-6453",
    "raw_address": "1600 Amphitheatre Parkway"
}
"""


class AccountAPI(APIView):
    def post(self, request):
        user_id = token_decode(request=request)

        if isinstance(user_id, Response):
            return user_id

        try:
            user = UserAccount.objects.get(id=user_id['id'])
        except UserAccount.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not validate_api_key(user_id['id']):
            return Response("API key has been expired")

        data = request.data

        url = "https://api.apollo.io/v1/accounts"

        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'X-Api-Key': user.api_key
        }

        try:
            response = requests.request("POST", url, headers=headers, json=data)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to connect to Apollo API: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)

        return Response({'error': 'Failed to create an account'}, status=response.status_code)


# ----------------------------------------------------


"""
Below is an example of API functionality that uses a proxy.

----------------------------------------------------

AccountAPI is a class that implements APIView to interact with the Apollo.io API.
It handles POST requests to create accounts using active proxies to ensure confidentiality and connection continuity.
Before executing the request, the class checks the presence of the user, the validity of the API key
and the availability of proxies, guaranteeing the reliability of requests.
"""

"""
class AccountAPI(APIView):
    def post(self, request):
        user_id = token_decode(request=request)

        if isinstance(user_id, Response):
            return user_id

        try:
            user = UserAccount.objects.get(id=user_id['id'])
        except UserAccount.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not validate_api_key(user_id['id']):
            return Response("API key has been expired", status=status.HTTP_401_UNAUTHORIZED)

        proxies = get_available_proxy()

        if not proxies:
            return Response("No proxies available", status=status.HTTP_503_SERVICE_UNAVAILABLE)

        data = request.data

        url = "https://api.apollo.io/v1/accounts"

        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'X-Api-Key': user.api_key
        }

        try:
            response = requests.request("POST", url, headers=headers, proxies=proxies, json=data)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to connect to Apollo API: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)

        return Response({'error': 'Failed to create an account'}, status=response.status_code)
"""
