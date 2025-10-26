from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('kyc/', views.kyc_submit, name='kyc_submit'),
    path("admin/users/", views.list_all_users,name='view_all_users'),
    path("admin/kyc/", views.list_all_kyc_submissions,name='admin_verify')
]

