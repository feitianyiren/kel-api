from django.db import models


class ActiveManagerMixin:

    def active(self):
        return self.filter(deleted__isnull=True)


class ResourceGroupQuerySet(models.QuerySet, ActiveManagerMixin):

    def for_user(self, user):
        return self.filter(resourcegroupuser__user=user)
