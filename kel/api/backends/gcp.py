import base64
import datetime
import json
import time
import urllib.parse

from collections import namedtuple

import Crypto.Hash.SHA256 as SHA256
import Crypto.PublicKey.RSA as RSA
import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5


GCS_API_URL = "https://storage.googleapis.com"


class GoogleServiceAccount(namedtuple("GoogleServiceAccount", "key client_id_email")):

    @classmethod
    def from_data(cls, encoded):
        data = json.loads(base64.b64decode(encoded).decode("utf-8"))
        private_key = RSA.importKey(data["private_key"])
        return cls(key=private_key, client_id_email=data["client_email"])


def make_signature(verb, path, expiration, content_type=""):
    bits = [
        verb,
        "",  # @@@ content MD5
        content_type,
        str(expiration),
        path,
    ]
    return "\n".join(bits)


def sign(service_account, text):
    text_hash = SHA256.new(text.encode("utf-8"))
    signer = PKCS1_v1_5.new(service_account.key)
    return base64.b64encode(signer.sign(text_hash))


# public
def make_storage_signed_url(verb, path, expires, content_type="application/octet-stream", service_account=None, api_url=GCS_API_URL):
    if service_account is None:
        service_account = GoogleServiceAccount.from_env()
    url = "{}{}".format(api_url, path)
    expiration = int(time.mktime((datetime.datetime.utcnow() + expires).timetuple()))
    signature = make_signature(verb, path, expiration, content_type=content_type)
    signed = sign(service_account, signature)
    encoded = urllib.parse.urlencode({
        "GoogleAccessId": service_account.client_id_email,
        "Expires": str(expiration),
        "Signature": signed,
    })
    return "{}?{}".format(url, encoded)
