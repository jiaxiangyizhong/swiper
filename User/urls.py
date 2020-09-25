from django.urls import path

from User import apis

urlpatterns = [
    path('vcode/fetch/', apis.fetch),
    path('vcode/submit/', apis.submit),
    path('profile/show/', apis.show),
    path('profile/update/', apis.update),
]
