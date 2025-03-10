from django.dispatch import receiver
from django.template.loader import get_template
from django.urls import reverse
from pretalx.common.signals import auth_html, profile_bottom_html
from pretalx.orga.signals import nav_event_settings
from pretalx.person.signals import delete_user

from .utils import all_backends, backend_friendly_name, user_backends


@receiver(nav_event_settings)
def pretalx_social_auth_settings(sender, request, **kwargs):
    if not request.user.has_perm("orga.change_settings", request.event):
        return []
    return [
        {
            "label": "pretalx Social Auth plugin",
            "url": reverse(
                "plugins:pretalx_social_auth:settings",
                kwargs={"event": request.event.slug},
            ),
            "active": request.resolver_match.url_name
            == "plugins:pretalx_social_auth:settings",
        }
    ]


@receiver(auth_html)
def render_login_auth_options(sender, request, next_url=None, **kwargs):
    print("render_login_auth_options")
    context = {}
    context["url_params"] = ""
    context["backends"] = {
        class_name: backend_friendly_name(be_class)
        for class_name, be_class in all_backends().items()
    }

    next_path = request.GET.get("next", next_url)
    if next_path:
        context["url_params"] = f"?next={next_path}"

    template = get_template("pretalx_social_auth/login.html")
    html = template.render(context=context, request=request)
    return html


@receiver(profile_bottom_html)
def render_user_options_backends(sender, user, **kwargs):
    user_backend_data = user_backends(user)
    context = {}
    context["associated_accounts"] = [
        (backend_friendly_name(assoc.provider), assoc)
        for assoc in user_backend_data["associated"]
    ]
    template = get_template("pretalx_social_auth/profile_settings.html")
    html = template.render(context=context)
    return html


@receiver(delete_user)
def delete_user_data(sender, user, **kwargs):
    user.social_auth.all().delete()
