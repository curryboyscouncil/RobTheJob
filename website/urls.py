from django.urls import path


from . import views

urlpatterns = [
     path('', views.home_page, name='index'),
     path('download/', views.download_yaml, name='download_yaml'),
     path('download_resume/', views.download_resume, name='download_resume'),
     path('process_data/', views.process_data, name='process_data'),
     path('final_page/', views.final_page, name='final_page'),
]