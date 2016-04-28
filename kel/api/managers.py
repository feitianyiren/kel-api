from django.db.models.manager import Manager

from .querysets import (
    ResourceGroupQuerySet,
    SiteQuerySet
)


class UserManager(Manager):

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class ResourceGroupManager(Manager.from_queryset(ResourceGroupQuerySet)):
    pass


class SiteManager(Manager.from_queryset(SiteQuerySet)):
    pass
