from pinax import api

from .models import Blob, ResourceGroup, Site, Service, Instance


@api.register
class BlobResource(api.Resource):

    api_type = "blobs"
    model = Blob
    attributes = [
        "name",
        "content_type",
        api.Attribute("url", scope="r"),
    ]

    @property
    def id(self):
        return self.obj.name

    def create(self, **kwargs):
        obj = super(BlobResource, self).create(**kwargs)
        self.meta["upload_url"] = obj.generate_signed_url()
        return obj


@api.register
class ResourceGroupResource(api.Resource):

    api_type = "resource-groups"
    model = ResourceGroup
    attributes = [
        "name",
        "created",
    ]
    relationships = {
        "sites": api.Relationship("sites", collection=True),
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
        "instances": api.Relationship("instances", collection=True),
        "services": api.Relationship("services", collection=True),
    }

    @property
    def id(self):
        return self.obj.name

    def create(self, **kwargs):
        resource_group = kwargs.pop("resource_group")
        self.obj.resource_group = resource_group
        return super(SiteResource, self).create(**kwargs)


@api.register
class ServiceResource(api.Resource):

    api_type = "services"
    model = Service
    attributes = [
        "name",
        "created",
    ]
    relationships = {
        "site": api.Relationship("sites"),
    }

    @property
    def id(self):
        return self.obj.name

    def create(self, **kwargs):
        site = kwargs.pop("site")
        self.obj.site = site
        return super(ServiceResource, self).create(**kwargs)


@api.register
class InstanceResource(api.Resource):

    api_type = "instances"
    model = Instance
    attributes = [
        "label",
        "created",
    ]
    relationships = {
        "site": api.Relationship("site"),
    }

    @property
    def id(self):
        return self.obj.label

    def create(self, **kwargs):
        site = kwargs.pop("site")
        self.obj.site = site
        return super(InstanceResource, self).create(**kwargs)
