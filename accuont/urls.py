from django.urls import path
from .views import *
urlpatterns = [
    path('',index),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('accounts/create/',create_account,name='create_account'),
    path('accounts/',accounts,name='accounts'),
    path('accounts/edit/<int:id>',edit_account,name='edit_account'),
    path('accounts/delete/<int:id>',delete_accont,name='delete.account'),
    path('account/department/<int:id>',department,name='department'),
    path('account/department/delete/<int:id>',delete_dep,name='delete.department'),
    
]
