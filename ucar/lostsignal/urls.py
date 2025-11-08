from django.urls import path
from .views import allerts_view, AllertPingLossAPI

urlpatterns = [
    path('allerts/', allerts_view, name='allerts_view'),
    path('api/pingloss/', AllertPingLossAPI, name='api_pingloss')

]