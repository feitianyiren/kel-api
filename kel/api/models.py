from django.core import validators
from django.db import models
from django.utils import timezone

from .managers import (
    UserManager,
    ResourceGroupManager,
    SiteManager
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

    def resource_groups(self):
        return ResourceGroup.objects.for_user(self)

    def sites(self):
        return Site.objects.for_user(self)


class ResourceGroup(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            validators.RegexValidator(
                validators._lazy_re_compile(r"^[a-zA-Z0-9_-]+$"),
                "Invalid name. (hint: ^[a-zA-Z0-9_-]+$)",
            ),
        ]
    )
    created = models.DateTimeField(default=timezone.now)

    objects = ResourceGroupManager()

    def __str__(self):
        return self.name

    def set_owner(self, owner):
        ResourceGroupMembership.objects.get_or_create(
            resource_group=self,
            user=owner,
            defaults={
                "role": "admin",
            },
        )

    def members(self):
        member_set = set()
        for membership in ResourceGroupMembership.objects.filter(resource_group=self):
            member = membership.user
            member.role = membership.role
            member_set.add(member)
        return member_set


class ResourceGroupMembership(models.Model):

    resource_group = models.ForeignKey(ResourceGroup)
    user = models.ForeignKey(User)
    role = models.CharField(max_length=50)

    class Meta:
        unique_together = [("resource_group", "user")]


class Site(models.Model):

    resource_group = models.ForeignKey(ResourceGroup, related_name="sites")
    name = models.CharField(
        max_length=100,
        validators=[
            validators.RegexValidator(
                validators._lazy_re_compile(r"^[a-zA-Z0-9_-]+$"),
                "Invalid name. (hint: ^[a-zA-Z0-9_-]+$)",
            ),
        ]
    )
    created = models.DateTimeField(default=timezone.now)

    objects = SiteManager()

    class Meta:
        unique_together = [("resource_group", "name")]

    def members(self):
        member_set = set()
        for member in self.resource_group.members():
            member.role = {
                "admin": "admin",
                "technical": "ops",
            }[member.role]
            member_set.add(member)
        for membership in SiteMembership.objects.filter(site=self):
            member = membership.user
            member.role = membership.role
            member_set.add(member)
        return member_set


class SiteMembership(models.Model):

    site = models.ForeignKey(Site)
    user = models.ForeignKey(User)
    role = models.CharField(max_length=50)

    class Meta:
        unique_together = [("site", "user")]
