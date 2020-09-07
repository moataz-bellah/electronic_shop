from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from django.urls import re_path
from rest_framework.routers import DefaultRouter,SimpleRouter
from .views import CustomObtainAuthToken
from rest_framework.authtoken.views import obtain_auth_token
r=DefaultRouter()
r2=DefaultRouter()
r2.register('order_item',views.OrderItemApi)
r2.register('order',views.OrderApi)
app_name = "shop"
urlpatterns = [
    path('', views.home, name="home"),
    path('client/',views.client_data,name='client'),
    path('market/', views.market, name="market"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout',views.signout,name='signout'),
    path('MyCoins',views.coins_form,name='mycoins'),
    path('search/', views.search, name="search"),
    path('<int:product_id>/cart/', views.cart, name="cart"),
    path('mycart/', views.mycart, name="mycart"),
    path('checkout/', views.checkout, name="checkout"),
    path('<int:product_id>/', views.detail, name="detail"),
    path('categories/<slug>/', views.categories, name="categories"),
    path('bill',views.bill_page,name='bill'),
    path('message',views.message_view,name='message'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('update_page/<int:id>/',views.update_page,name='update_page'),
    path('update/<int:id>/',views.update,name='update'),
    path('create/',views.order_create,name='create'),
    path('remove/<int:product_id>/',views.cart_remove,name='remove'),
    path('add1/<int:product_id>/',views.cart_add,name='add1'),
    path('ali/',views.cart_detail,name='cart'),
    path('order/',views.create_order,name='order'),
    #path('api/',include(r.urls)),
    path('clientdata/',views.client_data_page,name='clientdata'),
    path('updateclientp/',views.update_client_page,name='updateclientp'),
    path('updateclient/',views.update_client,name='updateclient'),
    path('data/',views.data_client,name='data'),
    path('test_filter/',views.testFilter,name = 'test_filter'),
    path('category_products/<str:name>/',views.categoryProducts,name = 'category_products'),
    path('update_quantity_plus/<int:product_id>/',views.updateQuantityPlus,name='update_quantity_plus'),
    path('update_quantity_minus/<int:product_id>/',views.updateQuantityMinus,name='update_quantity_minus'),
    ##################### API URLS ####################################
    path('api/login', CustomObtainAuthToken.as_view()),
    path('api/products/', views.api_products, name="api_products"),
    #path('api/login/',obtain_auth_token,name='api_login'),
    path('api/',include(r2.urls)),
    path('api/logout', views.Logout.as_view()),

]
