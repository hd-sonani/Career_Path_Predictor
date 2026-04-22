from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('wizard/', views.wizard_view, name='wizard'),
    path('result/<int:prediction_id>/', views.result_view, name='result'),
    path('history/', views.history_view, name='history'),
    path('career/<int:career_id>/', views.career_detail, name='career_detail'),
    path('compare/', views.compare_view, name='compare'),
    path('roadmap/<int:career_id>/', views.roadmap_view, name='roadmap'),
]
