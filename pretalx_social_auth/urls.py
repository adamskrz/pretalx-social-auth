from django.conf import settings
from django.urls import path, re_path
from pretalx.event.models.event import SLUG_REGEX
from social_core.utils import setting_name

from . import views
from .views import SocialAuthSettingsView

urlpatterns = [
    re_path(
        rf"^orga/event/(?P<event>{SLUG_REGEX})/settings/p/pretalx_social_auth/$",
        SocialAuthSettingsView.as_view(),
        name="settings",
    ),
]


extra = getattr(settings, setting_name("TRAILING_SLASH"), True) and "/" or ""

app_name = "social"

urlpatterns = [
    # authentication / association
    path(f"login/<str:backend>{extra}", views.auth, name="begin"),
    path(f"complete/<str:backend>{extra}", views.complete, name="complete"),
    # disconnection
    path(f"disconnect/<str:backend>{extra}", views.disconnect, name="disconnect"),
    path(
        f"disconnect/<str:backend>/<int:association_id>{extra}",
        views.disconnect,
        name="disconnect_individual",
    ),
]
