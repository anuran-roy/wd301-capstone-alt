from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers
from rest_framework_nested.routers import NestedSimpleRouter

from course_api.tasks.views import BoardViewset, StatusViewset, TaskViewSet
from course_api.users.api.views import (
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
    UserViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


router.register("boards" , BoardViewset)

board_nested_router = NestedSimpleRouter(router, r"boards", lookup="boards")

board_nested_router.register("tasks",TaskViewSet)
board_nested_router.register("status" , StatusViewset)

status_nested_router = NestedSimpleRouter(board_nested_router, r"status", lookup="status")
status_nested_router.register("tasks", TaskViewSet)

app_name = "api"

urlpatterns = [
    # GET /api/test -> TestView.as_view()
    path(r"auth/", include("rest_auth.urls")),
    path(r"auth/registration/", include("rest_auth.registration.urls")),
    path(r"", include(router.urls)),
    path(r"", include(board_nested_router.urls)),
    path(r"", include(status_nested_router.urls)),
    path("token/", DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
]
