from django.urls import path

from User import views

urlpatterns = [
    path('index/', views.index),
    path('vcode/fetch/', views.fetch),
    path('vcode/submit/', views.submit),
    path('profile/show/', views.show),
    path('profile/update/', views.update),
]
