from django.urls import path

from . import views

app_name = 'user_page'
urlpatterns = [
    path('', views.index, name='index'),
    path('test2/', views.to_MainWindow, name='to_MainWindow'),
    path('test/', views.to_top_players, name='to_top_players'),
    path('test3/', views.to_personal_page, name='to_personal_page'),
    path('adminPage/', views.to_admin_page, name='to_admin_page'),
]