from django.urls import path

from . import views

app_name = 'user_page'
urlpatterns = [
    path('', views.index, name='index'),
    path('test2/<str:player>', views.to_MainWindow, name='to_MainWindow'),
    path('test/<str:player_nam>/', views.to_top_players, name='to_top_players'),
    path('test/', views.to_top_players, name='to_top_players'),
    path('test3/', views.to_personal_page, name='to_personal_page'),
    path('adminPage/', views.to_admin_page, name='to_admin_page'),
    path('testic/<str:play>/', views.next_step, name='next_step'),
    path('testic1/<str:player_name>/', views.make_choice, name='make_choice'),
    path('adminPage/<int:year>/', views.next_day_admin, name='next_day_admin'),
]
