from django.contrib import admin
from django.urls import path
from apollo_app.views import UserLogin, ContactAPI, GetListEmailAccounts, AccountAPI
# from apollo_app.views import login_app
# from apollo_app.views import check_apollo_health, get_people_contact, create_contact, get_all_contacts


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('check-apollo-health/', check_apollo_health, name='check_apollo_health'),
    # path('get-person/', get_people_contact, name='get_people_contact'),
    # path('create-contact/', create_contact, name='create-contact'),
    # path('get-all-contact/', get_all_contacts, name='get-all-contact'),
    # path('login-app/', login_app, name='login-app'),
    path('login/', UserLogin.as_view(), name='login'),
    path('create-contact/', ContactAPI.as_view(), name='create-contact'),
    path('emails/', GetListEmailAccounts.as_view(), name='get-emails'),
    path('create-account/', AccountAPI.as_view(), name='create-account'),
]
