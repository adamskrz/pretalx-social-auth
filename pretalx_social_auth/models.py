from django.db import models



class SocialAuthSettings(models.Model):
    event = models.OneToOneField(
        to="event.Event",
        on_delete=models.CASCADE,
        related_name="pretalx_social_auth_settings",
    )
    some_setting = models.CharField(max_length=10, default="A")
