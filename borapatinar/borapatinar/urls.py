from django.urls import include, path
from app import views


urlpatterns = [
    path('rollerblade-weather', views.RollerbladeWeather.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]