from django.urls import path


from . import views

urlpatterns = [
     path('send_profile/', views.send_profile, name='send_profile'),
     path('download_resume/', views.download_resume, name='download_resume'),
]