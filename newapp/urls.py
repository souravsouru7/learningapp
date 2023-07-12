from django.urls import path
from .import views


urlpatterns = [
    path('',views.index,name="index"),
    path("courses/<int:pk>/",views.singlecourse_detail,name="single"),
    path("register",views.register,name="regi"),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

]