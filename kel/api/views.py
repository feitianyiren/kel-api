import os

from django.http import JsonResponse


def api_index(request):
    payload = {
        "name": os.environ["KEL_CLUSTER_NAME"],
        "identity-url": os.environ["KEL_IDENTITY_URL"],
    }
    if os.environ.get("KEL_IDENTITY_CLIENT_ID"):
        payload["kel-identity-client-id"] = os.environ.get("KEL_IDENTITY_CLIENT_ID")
    return JsonResponse(payload)
