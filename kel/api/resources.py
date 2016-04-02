from pinax import api

from .models import ResourceGroup


@api.register
class ResourceGroupResource(api.Resource):

    api_type = "resource-group"
    model = ResourceGroup
    attributes = [
        "name",
        "personal",
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
