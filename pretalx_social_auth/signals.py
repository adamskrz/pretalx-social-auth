from django.dispatch import receiver
from django.template.loader import get_template
from django.urls import reverse
from pretalx.common.signals import auth_html
from pretalx.orga.signals import nav_event_settings


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
def render_login_auth_options(sender, **kwargs):
    template = get_template("pretalx_social_auth/login.html")
    html = template.render()
    return html
