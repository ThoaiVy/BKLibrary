from django.urls import path
import library.views as views

app_name = 'library'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('loan/', views.loan_history, name='loan'),
]