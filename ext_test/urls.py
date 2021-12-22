from django.urls import path
from . import views


urlpatterns = [
    path('', views.StartView.as_view(), name='start'),
    path('ps_results/', views.PsychicsResultView.as_view(), name='results'),
    path('total/', views.TotalView.as_view(), name='total'),
]
