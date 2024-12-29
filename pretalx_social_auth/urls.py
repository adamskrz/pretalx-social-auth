from django.urls import path, re_path
from pretalx.event.models.event import SLUG_REGEX

from . import views
from .views import SocialAuthSettingsView

urlpatterns = [
    re_path(
        rf"^orga/event/(?P<event>{SLUG_REGEX})/settings/p/social_auth/$",
        SocialAuthSettingsView.as_view(),
        name="settings",
    ),
    # authentication / association
    path("p/social_auth/login/<str:backend>/", views.auth, name="begin"),
    path("p/social_auth/complete/<str:backend>/", views.complete, name="complete"),
    # disconnection
    path(
        "p/social_auth/disconnect/<str:backend>/",
        views.disconnect,
        name="disconnect",
    ),
    path(
        "p/social_auth/disconnect/<str:backend>/<int:association_id>/",
        views.disconnect,
        name="disconnect_individual",
    ),
]
