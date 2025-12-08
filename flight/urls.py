from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AirplaneTypeViewSet,
    AirplaneViewSet,
    CrewViewSet,
    AirportViewSet,
    RouteViewSet,
    FlightViewSet,
    OrderViewSet,
    TicketViewSet
)


router = DefaultRouter()
router.register(r"airplane-types", AirplaneTypeViewSet)
router.register(r"airplanes", AirplaneViewSet)
router.register(r"crew", CrewViewSet)
router.register(r"airports", AirportViewSet)
router.register(r"routes", RouteViewSet)
router.register(r"flights", FlightViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"tickets", TicketViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "flight"
