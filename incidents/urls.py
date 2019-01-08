from incidents import views
from django.urls import path
from rest_framework import routers
from django.conf.urls import include

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'incident', views.IncidentViewSet, 'incident')
router.register(r'site', views.SiteViewSet, 'site')
router.register(r'update', views.UpdateViewSet, 'update')

urlpatterns = [
    path('', include(router.urls)),
    path('subscribe', views.SubscriberView.as_view()),
]