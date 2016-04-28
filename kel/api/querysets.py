from django.db import models


class ResourceGroupQuerySet(models.QuerySet):

    def for_user(self, user):
        return self.filter(resourcegroupuser__user=user)
