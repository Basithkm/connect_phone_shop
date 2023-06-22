from . import views
from django.urls import path

# app_name= 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    
    path('signin/', views.signin, name='signin'),
    path('get-my-account',views.get_my_account,name="get_my_account"),
    path('signout/', views.signout, name='signout'),
    # path('myorders/', views.myorders,name='myorders'),
  
]