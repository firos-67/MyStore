from django.urls import path

from credentials import views
app_name='credentials'
urlpatterns=[
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('confirm/<username>',views.confirm,name='confirm'),
]