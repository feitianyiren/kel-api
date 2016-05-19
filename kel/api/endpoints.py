from pinax import api

from .authentication import KelIdentityAuthentication
from .models import Plugin
from .permissions import (
    ensure_token_match,
    ensure_user_belongs
)
from .resources import (
    BlobResource,
    PluginResource,
    ResourceGroupResource,
    SiteResource,
    ServiceResource,
    InstanceResource
)


@api.bind(resource=BlobResource)
class BlobEndpointSet(api.ResourceEndpointSet):

    url = api.url(
        base_name="blob",
        base_regex=r"blobs",
        lookup={
            "field": "blob",
            "regex": r"[a-f0-9]+"
        }
    )
    middleware = {
        "authentication": [
            api.authentication.Anonymous(),
        ]
    }

    def create(self, request, *args, **kwargs):
        with self.validate(self.resource_class) as resource:
            resource.save()
        return self.render_create(resource)


@api.bind(resource=PluginResource)
class PluginEndpointSet(api.ResourceEndpointSet):

    url = api.url(
        base_name="plugin",
        base_regex=r"plugins",
        lookup={
            "field": "plugin",
            "regex": r"\d+"
        }
    )
    middleware = {
        "authentication": [
            api.authentication.Anonymous(),
        ]
    }

    def get_queryset(self):
        return Plugin.objects.all()

    def prepare(self):
        if self.requested_method in ["retrieve", "update", "destroy"]:
            self.plugin = self.get_object_or_404(self.get_queryset(), pk=self.kwargs["plugin"])

    def list(self, request, *args, **kwargs):
        return self.render(self.resource_class.from_queryset(self.get_queryset()))

    def create(self, request, *args, **kwargs):
        with self.validate(self.resource_class) as resource:
            resource.save()
        return self.render_create(resource)

    def retrieve(self, request, *args, **kwargs):
        resource = self.resource_class(self.plugin)
        return self.render(resource)

    def update(self, request, *args, **kwargs):
        with self.validate(self.resource_class, obj=self.plugin) as resource:
            resource.save()
        return self.render(resource)

    def destroy(self, request, *args, **kwargs):
        self.plugin.delete()
        return self.render_delete()


@api.bind(resource=ResourceGroupResource)
class ScopedResourceGroupEndpointSet(api.ResourceEndpointSet):

    url = api.url(
        base_name="resource-group",
        base_regex=r"resource-groups",
        lookup={
            "field": "resource_group",
            "regex": r"[a-zA-Z0-9_-]+"
        }
    )
    middleware = {
        "authentication": [
            KelIdentityAuthentication(),
        ],
        "permissions": {
            ensure_token_match("abc", check_methods=["create"]),
            ensure_user_belongs("resource_group", check_methods=["retrieve", "update", "destroy"]),
        },
    }

    def get_queryset(self):
        return self.request.user.resource_groups()

    def prepare(self):
        if self.requested_method in ["retrieve", "update", "destroy"]:
            self.resource_group = self.get_object_or_404(
                self.get_queryset(),
                name=self.kwargs["resource_group"],
            )

    def list(self, request, *args, **kwargs):
        return self.render(self.resource_class.from_queryset(self.get_queryset()))

    def create(self, request, *args, **kwargs):
        with self.validate(self.resource_class) as resource:
            resource.save(
                create_kwargs={
                    "owner": request.user,
                }
            )
        return self.render_create(resource)

    def retrieve(self, request, *args, **kwargs):
        resource = self.resource_class(self.resource_group)
        return self.render(resource)

    def update(self, request, *args, **kwargs):
        with self.validate(self.resource_class, obj=self.resource_group) as resource:
            resource.save()
        return self.render(resource)

    def destroy(self, request, *args, **kwargs):
        self.resource_group.delete()
        return self.render_delete()


@api.bind(resource=SiteResource, parent=ScopedResourceGroupEndpointSet)
class ScopedSiteEndpointSet(api.ResourceEndpointSet):

    url = api.url(
        base_name="site",
        base_regex=r"sites",
        lookup={
            "field": "site",
            "regex": r"[a-zA-Z0-9_-]+"
        }
    )
    middleware = {
        "authentication": [
            KelIdentityAuthentication(),
        ],
        "permissions": {
            ensure_user_belongs("resource_group"),
        },
    }

    def get_queryset(self):
        return self.request.user.sites().filter(resource_group=self.resource_group)

    def prepare(self):
        self.resource_group = self.get_object_or_404(
            self.request.user.resource_groups(),
            name=self.kwargs["resource_group"],
        )
        if self.requested_method in ["retrieve", "update", "destroy"]:
            self.site = self.get_object_or_404(
                self.get_queryset().filter(resource_group=self.resource_group),
                name=self.kwargs["site"],
            )

    def list(self, request, *args, **kwargs):
        return self.render(self.resource_class.from_queryset(self.get_queryset()))

    def create(self, request, *args, **kwargs):
        with self.validate(self.resource_class) as resource:
            resource.save(
                create_kwargs={
                    "resource_group": self.resource_group,
                }
            )
        return self.render_create(resource)

    def retrieve(self, request, *args, **kwargs):
        resource = self.resource_class(self.site)
        return self.render(resource)

    def update(self, request, *args, **kwargs):
        with self.validate(self.resource_class, obj=self.site) as resource:
            resource.save()
        return self.render(resource)

    def destroy(self, request, *args, **kwargs):
        self.site.delete()
        return self.render_delete()


@api.bind(resource=ServiceResource, parent=ScopedSiteEndpointSet)
class ScopedServiceEndpointSet(api.ResourceEndpointSet):

    url = api.url(
        base_name="service",
        base_regex=r"services",
        lookup={
            "field": "service",
            "regex": r"[a-zA-Z0-9_-]+"
        }
    )
    middleware = {
        "authentication": [
            KelIdentityAuthentication(),
        ],
        "permissions": {
            ensure_user_belongs("site"),
        },
    }

    def get_queryset(self):
        return self.request.user.services().filter(site=self.site)

    def prepare(self):
        self.resource_group = self.get_object_or_404(
            self.request.user.resource_groups(),
            name=self.kwargs["resource_group"],
        )
        self.site = self.get_object_or_404(
            self.request.user.sites().filter(resource_group=self.resource_group),
            name=self.kwargs["site"],
        )
        if self.requested_method in ["retrieve", "update", "destroy"]:
            self.service = self.get_object_or_404(
                self.get_queryset().filter(site=self.site),
                name=self.kwargs["service"],
            )

    def list(self, request, *args, **kwargs):
        return self.render(self.resource_class.from_queryset(self.get_queryset()))

    def create(self, request, *args, **kwargs):
        with self.validate(self.resource_class) as resource:
            resource.save(
                create_kwargs={
                    "site": self.site,
                }
            )
        return self.render_create(resource)

    def retrieve(self, request, *args, **kwargs):
        resource = self.resource_class(self.service)
        return self.render(resource)

    def update(self, request, *args, **kwargs):
        with self.validate(self.resource_class, obj=self.service) as resource:
            resource.save()
        return self.render(resource)

    def destroy(self, request, *args, **kwargs):
        self.service.delete()
        return self.render_delete()


@api.bind(resource=InstanceResource, parent=ScopedSiteEndpointSet)
class ScopedInstanceEndpointSet(api.ResourceEndpointSet):

    url = api.url(
        base_name="instance",
        base_regex=r"instances",
        lookup={
            "field": "instance",
            "regex": r"[a-zA-Z0-9_-]+"
        }
    )
    middleware = {
        "authentication": [
            KelIdentityAuthentication(),
        ],
        "permissions": {
            ensure_user_belongs("site"),
        },
    }

    def get_queryset(self):
        return self.request.user.instances().filter(site=self.site)

    def prepare(self):
        self.resource_group = self.get_object_or_404(
            self.request.user.resource_groups(),
            name=self.kwargs["resource_group"],
        )
        self.site = self.get_object_or_404(
            self.request.user.sites().filter(resource_group=self.resource_group),
            name=self.kwargs["site"],
        )
        if self.requested_method in ["retrieve", "update", "destroy"]:
            self.instance = self.get_object_or_404(
                self.get_queryset().filter(site=self.site),
                name=self.kwargs["service"],
            )

    def list(self, request, *args, **kwargs):
        return self.render(self.resource_class.from_queryset(self.get_queryset()))

    def create(self, request, *args, **kwargs):
        with self.validate(self.resource_class) as resource:
            resource.save(
                create_kwargs={
                    "site": self.site,
                }
            )
        return self.render_create(resource)

    def retrieve(self, request, *args, **kwargs):
        resource = self.resource_class(self.instance)
        return self.render(resource)

    def update(self, request, *args, **kwargs):
        with self.validate(self.resource_class, obj=self.instance) as resource:
            resource.save()
        return self.render(resource)

    def destroy(self, request, *args, **kwargs):
        self.instance.delete()
        return self.render_delete()
