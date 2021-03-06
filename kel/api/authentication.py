import logging

from django.conf import settings
from django.db import transaction
from django.utils import six, timezone

import requests

from pinax.api.exceptions import AuthenticationFailed

from .models import User


logger = logging.getLogger(__name__)


def get_authorization_header(request):
    auth = request.META.get("HTTP_AUTHORIZATION", b"")
    if isinstance(auth, six.string_types):
        auth = auth.encode("iso-8859-1")
    return auth


class KelIdentityAuthentication:

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b"bearer":
            return None
        if len(auth) == 1:
            msg = "Invalid bearer header. No credentials provided."
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "Invalid bearer header. Token string should not contain spaces."
            raise AuthenticationFailed(msg)
        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = "Invalid bearer header. Token string should not contain invalid characters."
            raise AuthenticationFailed(msg)
        return self.check_identity(token)

    def check_identity(self, token):
        """
        Lookup token on identity service and create/update local user.
        """
        logger.info("checking identity server {}".format(settings.KEL["IDENTITY_URL"]))
        params = {"access_token": token}
        resp = requests.get("{}/tokeninfo/".format(settings.KEL["IDENTITY_URL"]), params=params)
        if not resp.ok:
            return None
        payload = resp.json()
        with transaction.atomic():
            user = next(iter(User.objects.filter(username=payload["user"]["username"])), None)
            if user is None:
                user = User.objects.create(username=payload["user"]["username"])
            else:
                user.last_login = timezone.now()
                user.save()
        return user

    def authenticate_header(self, request):
        return "Bearer"
