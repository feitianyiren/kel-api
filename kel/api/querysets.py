from django.db import models
from django.db.models import Q


class ResourceGroupQuerySet(models.QuerySet):

    def for_user(self, user):
        return self.filter(resourcegroupmembership__user=user)


class SiteQuerySet(models.QuerySet):

    def for_user(self, user):
        qs = self.filter(
            Q(sitemembership__user=user) | Q(resource_group__resourcegroupmembership__user=user)
        )
        qs = qs.distinct()
        return qs
