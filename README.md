# Apollo.io API Django project
## Description
This project was built on Django (Django REST Framework), MySQL, Docker and Apollo.io API .

The main functionality is user interaction with the Apollo.io functionality through its API. To interact, the user must be registered in the system and have his own Apollo.io API key, which he enters during registration.

## Structure
```
ApolloDjangoTestProject/
│
├── apollo_app/                        
│   ├── migrations/                    
│   ├── __init__.py                    
│   ├── admin.py                       
│   ├── apps.py                        
│   ├── models.py                      
│   ├── tests.py                       
│   ├── utils.py                       
│   ├── views.py                       
│
├── ApolloDjangoTestProject/           
│   ├── __init__.py                    
│   ├── asgi.py                        
│   ├── settings.py                    
│   ├── tokens.py                      
│   ├── urls.py                        
│   ├── wsgi.py                        
│
├── templates/                         
├── venv/                              
├── docker-compose.yml                 
├── Dockerfile                         
├── manage.py                          
├── README.md                          
├── requirements.txt
```

## Necessary Tools and Technology
To start and run the project, you need the following tools:
- Docker;
- MySQL;
- Django;
- Apollo.io account.

## Build and Run
First of all, clone the project from GitHub:
```
git clone https://github.com/1gorb1lyk/Apollo-django-project.git
```
Then in your project terminal, run this command for building docker-compose:
```
docker-compose up --build
```
To declare the DB tables, you need to perform migrations further.
```
docker-compose exec web python manage.py makemigration
```
And then
```
docker-compose exec web python manage.py migrate
```
After that, you need to create a superuser for an admin panel and add your user/users into User table.

## Apollo.io API
For the correct operation of the service, it is necessary that you have an account on the Apollo.io service to have access to the API of the service.

Then you need to create an API key, which should be stored in the UserAccount database table, along with your email.

#### Warning!
For better interaction when registering a user, it is better to use the same email used when registering an account on Apollo.io

## Requests for a test project
```
admin/  - request to the admin panel.
login/  - A registered user is logging in.
create-contact/ - GET request to get all contact data.
                  POST request to create new contact in Apollo.io
emails/ - Get a list email accounts.
create-account/ - Request to create company account.
```