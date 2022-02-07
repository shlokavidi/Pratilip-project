from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from proj1 import views

router = routers.DefaultRouter()
router.register(r'proj1s', views.Proj1View, 'proj1')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

