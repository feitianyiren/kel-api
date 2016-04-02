from django.core import validators
from django.db import models
from django.utils import timezone

from .managers import (
    UserManager,
    ResourceGroupManager
)


class User(models.Model):

    username = models.CharField(max_length=100, unique=True)
    last_login = models.DateTimeField(blank=True, null=True)

    is_active = True

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @property
    def resource_group(self):
        qs = ResourceGroup.objects.active().filter(
            resourcegroupuser__user=self,
            personal=True,
        )
        return next(iter(qs), None)

    def resource_groups(self):
        return ResourceGroup.objects.active().for_user(self)


class ResourceGroup(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            validators.RegexValidator(
                validators._lazy_re_compile(r"^[a-zA-Z0-9_-]+$"),
                "Invaid name. (hint: ^[a-zA-Z0-9_-]+$)",
            ),
        ]
    )
    personal = models.BooleanField(default=False)

    created = models.DateTimeField(default=timezone.now)
    deleted = models.DateTimeField(null=True, blank=True)

    objects = ResourceGroupManager()

    def __str__(self):
        return self.name

    def delete(self, **kwargs):
        for site in self.site_set.active():
            site.delete()
        self.deleted = timezone.now()
        self.save()

    def set_owner(self, owner):
        ResourceGroupUser.objects.get_or_create(
            resource_group=self,
            user=owner,
            defaults={
                "role": "admin",
            },
        )

    def users(self):
        us = []
        for membership in ResourceGroupUser.objects.filter(resource_group=self, resource_group__deleted__isnull=True):
            user = membership.user
            user.role = membership.role
            us.append(user)
        return us


class ResourceGroupUser(models.Model):

    resource_group = models.ForeignKey(ResourceGroup)
    user = models.ForeignKey(User)
    role = models.CharField(max_length=50)

    class Meta:
        unique_together = [("resource_group", "user")]
