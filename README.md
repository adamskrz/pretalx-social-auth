# pretalx Social Auth plugin

> [!CAUTION]
> This plugin is still under development and not ready for production use. It also uses signals currently only existing in [my fork of pretalx](https://github.com/adamskrz/pretalx/tree/social-auth)

This is a plugin for [pretalx](https://github.com/pretalx/pretalx). It provides an integration with [Python Social Auth](https://github.com/python-social-auth/social-core), allowing users to log in with third-party services.

Originally based on [social_django](https://github.com/python-social-auth/social-app-django) from the Python Social Auth project, but with the removal of deprecated features and the addition of pretalx-specific settings.

## Screenshots

![Screenshots of pretalx orga login screen and CFP account step with extra providers](img/login_screenshots.png)

## Configuration

In your `pretalx.cfg` file, add all the auth backends you need as a comma-separated list. Then, add the backend-specific settings to the `[plugin:pretalx_social_auth]` section. You can find the backend name and required settings in the [python-social-auth documentation](https://python-social-auth.readthedocs.io/en/latest/backends/index.html).

Example:

```ini
[project.entry-points."pretalx.plugin"]
pretalx_social_auth = "pretalx_social_auth:PretalxPluginMeta"

[authentication]
additional_auth_backends=social_core.backends.microsoft.MicrosoftOAuth2,social_core.backends.open_id.OpenIdAuth

[plugin:pretalx_social_auth]
SOCIAL_AUTH_MICROSOFT_GRAPH_KEY=xxxxx-xxxxx-xxxxx-xxxxx-xxxxxxxxxx
SOCIAL_AUTH_MICROSOFT_GRAPH_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxx
```

Instructions on adding custom backends will be added in the future.

Due to how Social Auth is configured with API keys in `settings.py`, this doesn't support configuring providers (backends) on a per-event basis. This means particular care should be taken where custom event domains are in use, as some providers require a different API key per domain (or adding valid redirect URLs).

I initially looked into using [django-allauth](https://github.com/pennersr/django-allauth) instead, which allows configuring providers in the database on a per-site basis, but it also replaces the full auth model, so would be more difficult to make into a plugin!

## Email-based Account Linking

When a user attempts to log in via SSO for the first time, the plugin checks if a user with the same email address already exists in the database. The behavior in this situation is controlled by the **TRUST_IDP_EMAILS** global setting.

### TRUST_IDP_EMAILS Setting

This setting controls whether the operator trusts all configured identity providers (IDPs) to authenticate users:

- **Disabled (Default - Secure)**: Users logging in via SSO for the first time will be rejected if an account with that email already exists. The user will be shown an error message instructing them to log in with their existing credentials first, then connect their social account from their profile settings.

- **Enabled (Trust IDPs)**: Users logging in via SSO for the first time will be automatically linked to existing accounts with the same email address. This provides a seamless experience when users already have an account and want to use SSO.

### Security Considerations

The default is **disabled** for security reasons:

- It prevents unauthorized access if an attacker compromises an email account and creates a social login with a provider
- It ensures explicit user consent before linking accounts
- It's safer when you cannot fully trust all configured identity providers

Enable this setting only when:

- You fully trust all configured identity providers to properly verify email addresses
- Your IDPs enforce email verification
- You want to prioritize user convenience over strict account separation

### Configuration

This is a global setting configured in your `pretalx.cfg` file. Add it to the `[plugin:pretalx_social_auth]` section:

```ini
[plugin:pretalx_social_auth]
TRUST_IDP_EMAILS=true
```

The current configuration and list of enabled identity providers can be viewed in the organizer interface under "pretalx Social Auth plugin Settings".

## Development setup

1. Make sure that you have a working [pretalx development setup](https://docs.pretalx.org/en/latest/developer/setup.html).

2. Clone this repository, eg to `local/pretalx-social-auth`.

3. Activate the virtual environment you use for pretalx development.

4. Run `pip install -e .` within this directory to register this application with pretalx's plugin registry.

5. Run `make` within this directory to compile translations.

6. Restart your local pretalx server. This plugin should show up in the plugin list shown on startup in the console.
   You can now use the plugin from this repository for your events by enabling it in the 'plugins' tab in the settings.

This plugin has CI set up to enforce a few code style rules. To check locally, you need these packages installed::

    pip install flake8 flake8-bugbear isort black djhtml

To check your plugin for rule violations, run::

    black --check .
    isort -c .
    djhtml -c .
    flake8 .

You can auto-fix some of these issues by running::

    isort .
    black .
    djhtml .
