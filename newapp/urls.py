from django.urls import path
from . import views

app_name = 'newapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/<int:pk>/', views.singlecourse_detail, name='singlecourse_detail'),
    path('register/', views.register, name='regi'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('payment/<int:pk>/', views.payment, name='payment'),
    path('course/<int:pk>/video/', views.show_video, name='show_video'),
    path('payment/success/<int:pk>/', views.payment_success, name='payment_success'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
   
]
