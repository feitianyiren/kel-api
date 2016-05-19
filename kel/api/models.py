import re

from django.core import validators
from django.db import models
from django.utils import timezone

from django.contrib.postgres.fields import JSONField

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

    def services(self):
        return Service.objects.filter(site__in=self.sites())

    def instances(self):
        return Instance.objects.filter(site__in=self.sites())


class Plugin(models.Model):

    domain_re = r"[a-z0-9]+([-._~][a-z0-9]+)*"
    name_re = r"[a-z0-9]+([-][a-z0-9]+)*"
    version_re = r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:(?:\d*[A-Za-z-][0-9A-Za-z-]*|(?:0|[1-9]\d*))\.)*(?:\d*[A-Za-z-][0-9A-Za-z-]*|(?:0|[1-9]\d*))))?(?:\+((?:(?:[0-9A-Za-z-]+)\.)*[0-9A-Za-z-]+))?"
    identifier_re = re.compile(
        r"(?P<domain>{domain})/(?P<name>{name}):v(?P<version>{version})".format(
            domain=domain_re,
            name=name_re,
            version=version_re,
        )
    )

    identifier = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            validators.RegexValidator(identifier_re, "Invalid identifier."),
        ]
    )
    manifest = JSONField(default=dict)


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


class Service(models.Model):

    site = models.ForeignKey(Site, related_name="services")
    name = models.CharField(
        max_length=50,
        validators=[
            validators.RegexValidator(
                validators._lazy_re_compile(r"^[a-zA-Z0-9-]+$"),
                "Invalid name. (hint: ^[a-zA-Z0-9-]+$)",
            ),
        ]
    )
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [("site", "name")]


class Instance(models.Model):

    site = models.ForeignKey(Site, related_name="instances")
    label = models.CharField(
        max_length=50,
        validators=[
            validators.RegexValidator(
                validators._lazy_re_compile(r"^[a-zA-Z0-9-]+$"),
                "Invalid label. (hint: ^[a-zA-Z0-9-]+$)",
            ),
        ]
    )
    kind = models.CharField(max_length=50)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [("site", "label")]
