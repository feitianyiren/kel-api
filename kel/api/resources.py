from pinax import api

from .models import ResourceGroup, Site


@api.register
class ResourceGroupResource(api.Resource):

    api_type = "resource-group"
    model = ResourceGroup
    attributes = [
        "name",
        "created",
    ]
    relationships = {
        "sites": api.Relationship("site", collection=True),
    }

    @property
    def id(self):
        return self.obj.name

    def create(self, **kwargs):
        owner = kwargs.pop("owner")
        obj = super(ResourceGroupResource, self).create(**kwargs)
        obj.set_owner(owner)
        return obj


@api.register
class SiteResource(api.Resource):

    api_type = "sites"
    model = Site
    attributes = [
        "name",
        "created",
    ]
    relationships = {
        "instances": api.Relationship("instance", collection=True),
        "services": api.Relationship("services", collection=True),
    }

    @property
    def id(self):
        return self.obj.name
