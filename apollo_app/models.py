from django.db import models


class UserAccount(models.Model):
    email = models.EmailField(unique=True)
    api_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    last_checked = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.email


class Proxies(models.Model):
    ip_address = models.CharField(max_length=255)
    port = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)

    def __repr__(self):
        return self.ip_address
