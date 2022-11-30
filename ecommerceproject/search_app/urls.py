from search_app import views
from django.urls import path
app_name='search_app'
urlpatterns=[
    path('',views.SearchResults,name='SearchResults')
]