from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('kiongozi/', views.kiongozi_view, name='kiongozi_page'),
    path('post_tangazo/', views.post_announcement, name='post_announcement'),
    path('kusoma/', views.kusoma, name='kusoma'),
    path('edit/<int:id>/', views.edit_announcement, name='edit_announcement'),
    path('delete/<int:id>/', views.delete_announcement, name='delete_announcement'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('orodha/', views.registered_users_view, name='user_list'),
    path('orodha/export/',views.export_users_csv, name='export_users_csv'),
    path('tuma-sms/', views.send_sms_view, name='sms-page'),
    path('upload/', views.upload_document, name='upload_document'),
    path('documents/', views.document_list, name='document_list'),
     path('profile/', views.view_profile, name='view_profile'),
    path('logout/', views.logout_view, name='logout'),
    
]
