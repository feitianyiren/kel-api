import itertools

from django.conf.urls import include, url

from . import endpoints, views


handler404 = "pinax.api.handler404"

urlpatterns = [
    url(r"^$", views.api_index),
    url(r"^v1/", include(
        list(itertools.chain.from_iterable([
            endpoints.BlobEndpointSet.as_urls(),
            endpoints.PluginEndpointSet.as_urls(),
        ]))
    )),
    url(r"^v1/self/", include(
        list(itertools.chain.from_iterable([
            endpoints.ScopedResourceGroupEndpointSet.as_urls(),
            endpoints.ScopedSiteEndpointSet.as_urls(),
            endpoints.ScopedServiceEndpointSet.as_urls(),
            endpoints.ScopedInstanceEndpointSet.as_urls(),
        ]))
    ))
]
