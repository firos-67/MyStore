from django.urls import path

from cart import views
app_name='cart'
urlpatterns=[
    path('add/<int:product_id>/',views.add_cart,name='add_cart'),
    path('minus/<int:product_id>/',views.cart_minus,name='cart_minus'),
    path('view',views.cart_details,name='cart_details'),
    path('remove/<int:product_id>/',views.cart_remove,name='cart_remove'),
]
