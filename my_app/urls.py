from django.urls import path
from .views import home, new_search

appname = 'my_app'
urlpatterns = [
    path('', home, name='home_page'),
    path('new_search', new_search, name='new_search')
]