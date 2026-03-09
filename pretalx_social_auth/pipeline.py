"""
Custom pipeline functions for pretalx social auth plugin.
"""

from django.contrib.auth import get_user_model
from social_core.exceptions import AuthForbidden


def associate_by_email_if_trusted(strategy, details, backend, user=None, *args, **kwargs):
    """
    Pipeline function to handle email-based account association.
    
    This function checks if a user is logging in via SSO for the first time,
    and if a user with the same email already exists in the database.
    
    The global TRUST_IDP_EMAILS setting controls whether existing accounts
    should be automatically linked. If disabled (default), the login will be rejected.
    
    This should be placed in the pipeline BEFORE the 'social_core.pipeline.user.create_user' step.
    """
    if user:
        # User is already associated or logged in, skip this check
        return
    
    # Get email from details
    email = details.get('email')
    if not email:
        # No email provided by the IDP, can't do email matching
        return
    
    # Check if a user with this email already exists
    User = get_user_model()
    email_field = getattr(User, 'EMAIL_FIELD', 'email')
    existing_users = User._default_manager.filter(**{email_field + '__iexact': email})
    
    if not existing_users.exists():
        # No existing user with this email, proceed with normal flow
        return
    
    # There is an existing user with this email
    # Check the global TRUST_IDP_EMAILS setting (default: False for security)
    # strategy.get_setting() returns None if not configured, so we default to False
    trust_idp_emails = strategy.get_setting('TRUST_IDP_EMAILS')
    if trust_idp_emails is None:
        trust_idp_emails = False
    
    if not trust_idp_emails:
        # Trust is not enabled, reject the login
        raise AuthForbidden(
            backend,
            f"An account with email {email} already exists. "
            "Please log in with your existing credentials first, "
            "then connect your social account from your profile settings."
        )
    
    # Trust is enabled, return the existing user to associate with this social auth
    existing_user = existing_users.first()
    return {
        'user': existing_user,
        'is_new': False
    }
