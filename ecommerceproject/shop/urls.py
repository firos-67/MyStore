from django.urls import path
from shop import views
app_name='shop'
urlpatterns = [
    path('',views.allProdCat,name='allProdCat'),
    path('<slug:c_slug>/',views.allProdCat,name='products_by_category'),
    path('<slug:cat_slug>/<slug:prod_slug>/',views.proDetail,name='product_details'),
]
