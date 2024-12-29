from django.apps import AppConfig
from django.utils.translation import gettext_lazy

from . import __version__


class PluginApp(AppConfig):
    name = "pretalx_social_auth"
    verbose_name = "pretalx Social Auth plugin"

    class PretalxPluginMeta:
        name = gettext_lazy("pretalx Social Auth plugin")
        author = "Adam Skrzymowski"
        description = gettext_lazy("pretalx plugin for Python Social Auth")
        visible = True
        version = __version__
        category = "INTEGRATION"

    def ready(self):
        from . import signals  # NOQA
