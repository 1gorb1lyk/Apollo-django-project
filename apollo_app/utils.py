import requests
from .models import UserAccount, Proxies
from django.utils import timezone
import random


"""
    check_api_key(api_key) - checks the validity of the provided API key, by sending a request to the Apollo.io health 
    endpoint. The function forms an HTTP GET request with the API key in the headers and returns True if the key is 
    valid and the user is authorized, otherwise returns False.
"""
def check_api_key(api_key):
    url = "https://api.apollo.io/v1/auth/health"
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200 and response.json().get("is_logged_in"):
        return True
    return False


# ----------------------------------------------------------

"""
    validate_api_key(user_id) - checks the API status of the user's key by its ID. The function gets the user from the 
    database, checks the validity of his API key using the check_api_key function. If the key is valid, the user is 
    marked as active, otherwise - as inactive. The function returns a boolean value indicating the activity of the user.
"""


def validate_api_key(user_id):
    user = UserAccount.objects.get(id=user_id)
    if check_api_key(user.api_key):
        user.is_active = True
    else:
        user.is_active = False
    user.save()
    return user.is_active


# ----------------------------------------------------------

"""
This function returns an available proxy from the database for making requests.

    The function works by:
    1. Fetching all active proxies from the database.
    2. Filtering out the proxies that have been recently used (within the last 5 minutes).
    3. Randomly selecting a proxy from the remaining available ones.
    4. Updating the 'last_used' timestamp for the selected proxy.
    5. Returning the IP address and port of the chosen proxy.

    If no available proxies are found, it returns None.


    Warning! 
    
    This function do not work, because there are no proxies in DB! 
    This is just an example of a simple function that works with PROXY.

"""


def get_available_proxy():
    proxies = Proxies.objects.filter(is_active=True)
    available_proxies = [proxy for proxy in proxies if proxy.last_used is None or
                         (timezone.now() - proxy.last_used).total_seconds() > 300]
    if available_proxies:
        proxy = random.choice(available_proxies)
        proxy.last_used = timezone.now()
        proxy.save()

        if not proxy.ip_address:
            return None

        proxies = {
            'http': f'http://{proxy.ip_address}:{proxy.port}',
            'https': f'https://{proxy.ip_address}:{proxy.port}'
        }

        return proxies
    else:
        return None

