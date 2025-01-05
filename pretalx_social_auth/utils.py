from functools import wraps
from urllib.parse import quote

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import Http404
from django.http.multipartparser import MultiPartParserError
from django.urls import reverse
from django.views.decorators.http import require_POST
from social_core.backends import utils
from social_core.backends.base import BaseAuth
from social_core.exceptions import MissingBackend
from social_core.utils import get_strategy, module_member, setting_name

STRATEGY = getattr(
    settings, setting_name("STRATEGY"), "pretalx_social_auth.strategy.DjangoStrategy"
)
STORAGE = getattr(
    settings, setting_name("STORAGE"), "pretalx_social_auth.models.DjangoStorage"
)
REQUIRE_POST = setting_name("REQUIRE_POST")

Strategy = module_member(STRATEGY)
Storage = module_member(STORAGE)


def load_strategy(request=None):
    return get_strategy(STRATEGY, STORAGE, request)


def load_backend(strategy, name, redirect_uri):
    return strategy.get_backend(name, redirect_uri=redirect_uri)


def psa(redirect_uri=None, load_strategy=load_strategy):
    def decorator(func):
        @wraps(func)
        def wrapper(request, backend, *args, **kwargs):
            uri = redirect_uri
            if uri and not uri.startswith("/"):
                uri = reverse(redirect_uri, args=(backend,))
            request.social_strategy = load_strategy(request)
            # backward compatibility in attribute name, only if not already
            # defined
            if not hasattr(request, "strategy"):
                request.strategy = request.social_strategy

            try:
                request.backend = load_backend(
                    request.social_strategy, backend, redirect_uri=uri
                )
            except MissingBackend:
                raise Http404("Backend not found")
            return func(request, backend, *args, **kwargs)

        return wrapper

    return decorator


def maybe_require_post(func):
    @wraps(func)
    def wrapper(request, backend, *args, **kwargs):
        require_post = getattr(settings, REQUIRE_POST, False)
        if require_post:
            return require_POST(func)(request, backend, *args, **kwargs)

        return func(request, backend, *args, **kwargs)

    return wrapper


def backend_friendly_name(backend: BaseAuth | str) -> str:
    """Return the friendly name of a backend. If the friendly name is not known, return the name."""
    if isinstance(backend, str):
        backend = get_backend(backend)
    name_mapping = load_strategy().get_setting("BACKEND_NAME_MAPPING")
    class_name = backend.name
    return getattr(backend, "friendly_name", name_mapping.get(class_name, class_name))


def get_backend(name):
    """Return a backend by name."""
    return utils.get_backend(settings.AUTHENTICATION_BACKENDS, name)


def user_backends(user):
    """
    Dictionary with the following keys:
        associated: UserSocialAuth model instances for currently associated
                    accounts
        not_associated: Not associated (yet) backend names
        backends: All backend names.

    Wrapper around social_core.backends.utils.user_backends_data.
    """
    return utils.user_backends_data(user, settings.AUTHENTICATION_BACKENDS, Storage)


def all_backends():
    """Return all configured backends. Dictionary with class name as key and backend class as value."""
    return utils.load_backends(settings.AUTHENTICATION_BACKENDS)


def login_redirect(request):
    """Load current redirect to context."""
    try:
        value = (
            request.method == "POST"
            and request.POST.get(REDIRECT_FIELD_NAME)
            or request.GET.get(REDIRECT_FIELD_NAME)
        )
    except MultiPartParserError:
        # request POST may be malformed
        value = None
    if value:
        value = quote(value)
        querystring = REDIRECT_FIELD_NAME + "=" + value
    else:
        querystring = ""

    return {
        "REDIRECT_FIELD_NAME": REDIRECT_FIELD_NAME,
        "REDIRECT_FIELD_VALUE": value,
        "REDIRECT_QUERYSTRING": querystring,
    }
